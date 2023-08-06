import json
import time

import elasticapm
from elasticapm.contrib.django.traces import apm_trace
from kafka import KafkaConsumer
from kafka.structs import TopicPartition

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.db.models import Q
from django.test import TestCase  # noqa F401

from core.consts import CONSUMER
from core.datahandler import DataHandlerFactory
from core.models import DataHandlersMap
from core.models import ErrorsRequest
from core.models import KafkaOffset

ENV_TYPE = getattr(settings, 'ENV_TYPE', 'prod')


class KafkaConsumerClass(KafkaConsumer):
    def __init__(self,
                 # topic,
                 bootstrap_servers,
                 enable_auto_commit,
                 **kwargs
                 ):
        super(KafkaConsumerClass, self).__init__(
            # topic,
            bootstrap_servers=bootstrap_servers,
            enable_auto_commit=enable_auto_commit,
            **kwargs
        )


class Consumer:
    topic = None

    def __init__(self, topic: str):
        self.command = BaseCommand()
        self.topic = topic

        kafka_settings_dict = getattr(settings, 'KAFKA_SETTINGS', [])

        self.sleep_seconds = kafka_settings_dict.get('SLEEP_SECONDS', 5)
        self.kafka_client = KafkaConsumerClass(
            # self.topic,
            bootstrap_servers=kafka_settings_dict.get('BOOTSTRAP_SERVERS', None),
            enable_auto_commit=kafka_settings_dict.get('AUTO_COMMIT', False),
            # default_offset_commit_callback=func_callback,
            # group_id=None,
            # auto_offset_reset='earliest',
            # TODO с offset разобраться
            # consumer_timeout_ms=1000,  # StopIteration if no message after 1sec А ЗАЧЕМ?
            # auto_offset_reset         CHECK
            # auto_commit_interval_ms   CHECK
        )
        self.mypartition = TopicPartition(self.topic, 0)
        self.kafka_client.assign([self.mypartition])

    # TODO обработка исключения и возврат None
    def deserialize(self, message: bytes):
        try:
            decoded = message.decode('utf-8')
            deserialized = json.loads(decoded)
        except Exception as e:
            # TODO log this situation
            print("Exception", e)
            return None
        return deserialized

    def get_topic_offset(self):
        topic_info = KafkaOffset.objects.filter(
            topic=self.topic,
            client_type=CONSUMER
        )
        if topic_info.exists():
            partition = topic_info.first().partition
            offset = topic_info.first().offset
        else:
            return None, None
        return partition, offset

    def start_consume(self):
        # TODO log this
        # subscription = self.kafka_client.subscription()
        partition, offset = self.get_topic_offset()
        if partition is not None and offset is not None:
            self.kafka_client.seek(self.mypartition, offset)  # указание начального смещения

        self.transaction_type = "kafka"
        self.transaction_name = f"consumer.{self.topic}"

        while True:
            for msg in self.kafka_client:  # НЕ ожидает при отсутствии сообщений,
                # выходит из цикла при отсутствии новых
                with apm_trace(self.transaction_type, self.transaction_name) as tracer:
                    if tracer.parent_transaction and getattr(
                            tracer.parent_transaction, "propagate_labels", False
                    ):
                        elasticapm.label(**tracer.parent_transaction.labels)

                    offset = msg.offset
                    partition = msg.partition
                    topic = msg.topic

                    elasticapm.label(message=str(msg)[:500])
                    elasticapm.label(offset=offset)
                    elasticapm.label(topic=partition)
                    elasticapm.label(partition=topic)

                    value = getattr(msg, 'value', None)
                    deserialized_object = self.deserialize(value)

                    elasticapm.label(deserialized_object=str(deserialized_object)[:500])
                    saved = False
                    try:
                        if deserialized_object:
                            handler = DataHandlerFactory.get_handler(deserialized_object, self.topic)
                            handler.save_data()
                            saved = True
                    except Exception as ex:
                        ErrorsRequest.objects.create(
                            error=str(ex)[:500],
                            status_code=offset,
                            request=self.transaction_name
                        )
                        self.command.stdout.write(self.command.style.ERROR(
                            f'Processing error topic: {topic}'
                            f' error: {ex}')
                        )
                    finally:
                        update_fields = dict(
                            offset=offset,
                            partition=partition
                        )
                        KafkaOffset.objects.update_or_create(
                            topic=topic,
                            client_type=CONSUMER,
                            defaults=update_fields,
                        )
                        if saved:
                            self.command.stdout.write(
                                self.command.style.SUCCESS(f'Successfully processing msg, topic: {topic}')
                            )

            if ENV_TYPE == 'test':
                # для тестового окружения, запускали чтение единожды для получения значения фикстур
                return

            # К данному моменту прочитали все сообщения, ждём новых, продолжая цикл.
            time.sleep(self.sleep_seconds)


class Command(BaseCommand):
    help = 'Start kafka client with specified topic for consuming messages'
    ARG_NAME = 'topic'

    def add_arguments(self, parser):
        parser.add_argument(self.ARG_NAME, nargs=1, default='', type=str)

    def validate_topic(self, options: dict):
        input_list = options.get(self.ARG_NAME, None)

        if input_list:
            topic = input_list[0]
            try:
                data_handler_map = DataHandlersMap.objects.get(Q(data_handler=topic) | Q(topic=topic))
                data_handler = data_handler_map.data_handler
                data_handler_topic = data_handler_map.topic
            except Exception as ex:
                self.stdout.write(self.style.ERROR(ex))
                raise CommandError(ex)
            finally:
                if topic != data_handler and topic != data_handler_topic:
                    raise CommandError(f'Specified topic will not be processed, topic: {topic}')
                topic = data_handler_topic
        else:
            raise CommandError('Topic does not defined')

        return topic

    def handle(self, *args, **options):
        topic = self.validate_topic(options)
        consumer = Consumer(topic=topic)
        self.stdout.write(self.style.SUCCESS(f'Successfully started consuming topic: {topic}'))
        consumer.start_consume()
