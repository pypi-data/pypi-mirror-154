import json

import elasticapm
from elasticapm.contrib.django.traces import apm_trace
from kafka import KafkaProducer

from django.conf import settings

from core.consts import PRODUCER
from core.models import KafkaOffset

kafka_settings_dict = getattr(settings, 'KAFKA_SETTINGS', [])
bootstrap_servers = kafka_settings_dict.get('BOOTSTRAP_SERVERS', None)


class PHKafkaProducer:

    topic = None
    data_key = None
    branch = None
    obj = None
    transaction_type = None
    transaction_name = None

    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

    def send(self, topic: str, msg, data_key, branch, obj):
        self.topic = topic
        self.data_key = data_key
        self.branch = branch
        self.obj = obj
        self.transaction_type = "kafka"
        self.transaction_name = f"produced.{self.topic}"
        self.kafka_send(msg)

    def on_send_error(self, excp):
        with apm_trace(self.transaction_type, self.transaction_name) as tracer:
            if tracer.parent_transaction and getattr(
                    tracer.parent_transaction, "propagate_labels", False
            ):
                elasticapm.label(**tracer.parent_transaction.labels)

            elasticapm.set_transaction_result(excp)
            raise Exception('Ошибка отправки сообщений в кафку ', excp)

    def on_send_success(self, record_metadata):
        with apm_trace(self.transaction_type, self.transaction_name) as tracer:
            if tracer.parent_transaction and getattr(
                    tracer.parent_transaction, "propagate_labels", False
            ):
                elasticapm.label(**tracer.parent_transaction.labels)
            update_fields = dict(
                offset=record_metadata.offset,
                partition=record_metadata.partition
            )
            KafkaOffset.objects.update_or_create(
                topic=record_metadata.topic,
                client_type=PRODUCER,
                defaults=update_fields,
            )

            elasticapm.label(topic=record_metadata.topic)
            elasticapm.label(partition=record_metadata.partition)
            elasticapm.label(offset=record_metadata.offset)

            elasticapm.label(data_key=self.data_key)
            elasticapm.label(branch=self.branch)
            elasticapm.label(message=str(self.msg)[:500])
            elasticapm.label(obj=str(self.obj))

            elasticapm.set_transaction_result("SUCCESS")

    def kafka_send(self, msg):
        self.producer.send(
            self.topic, json.dumps(msg).encode('utf-8')
        ).add_callback(
            self.on_send_success,
        ).add_errback(
            self.on_send_error
        )
        self.producer.flush()
