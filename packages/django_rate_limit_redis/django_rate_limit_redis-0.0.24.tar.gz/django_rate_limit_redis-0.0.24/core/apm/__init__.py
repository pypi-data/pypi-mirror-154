from functools import wraps
import json
import logging

import elasticapm
from elasticapm import set_custom_context
from elasticapm import set_user_context
from elasticapm.contrib.django.traces import apm_trace
from elasticapm.utils.logging import get_logger

from django.conf import settings

logger = get_logger("elasticapm.traces")
logging.getLogger("urllib3").setLevel(logging.ERROR)


# TODO Переделать
class ApiClientResponse:
    def __init__(self, response, status_code=None):
        self.response = response
        self._status_code = status_code

    def json(self, raise_exception=False):
        try:
            result = self.response.json()
        except ValueError:
            if raise_exception:
                raise
            result = None

        return result


# TODO Переделать
class ApiClientException(Exception):
    def __init__(self, *args, **kwargs):
        response = kwargs.pop("response", None)
        self.response = response
        self.request = kwargs.pop("request", None)
        if response is not None and not self.request and hasattr(response, "request"):
            self.request = self.response.request

        self.error = kwargs.pop("exc", None)
        if self.error:
            self.error_code = kwargs.pop("error_code", None)

        if response is not None:
            http_error_msg = ""
            if isinstance(response.reason, bytes):
                # We attempt to decode utf-8 first because some servers
                # choose to localize their reason strings. If the string
                # isn't utf-8, we fall back to iso-8859-1 for all other
                # encodings. (See PR #3538)
                try:
                    reason = response.reason.decode("utf-8")
                except UnicodeDecodeError:
                    reason = response.reason.decode("iso-8859-1")
            else:
                reason = response.reason

            if 400 <= response.status_code < 500:
                http_error_msg = "%s Client Error: %s for url: %s" % (
                    response.status_code,
                    reason,
                    response.url,
                )

            elif 500 <= response.status_code < 600:
                http_error_msg = "%s Server Error: %s for url: %s" % (
                    response.status_code,
                    reason,
                    response.url,
                )

            if http_error_msg:
                super().__init__(http_error_msg, *args, **kwargs)
        else:
            super().__init__(*args, **kwargs)


def request_apm_trace(func):
    if not settings.ELASTIC_APM_SERVER:
        return func

    @wraps(func)
    def request_log_wrapper(self, *args, **kwargs):
        transaction_type = "api.request"
        transaction_name = f"{'POST' if self.data else 'GET'} {self.base_url}"
        with apm_trace(transaction_type, transaction_name) as tracer:

            if tracer.parent_transaction and getattr(
                tracer.parent_transaction, "propagate_labels", False
            ):
                elasticapm.label(**tracer.parent_transaction.labels)

            set_user_context(user_id=self.user)
            elasticapm.label(base_url=self.base_url)
            elasticapm.label(url=args[0])
            elasticapm.label(headers=self.headers)

            response = func(self, *args, **kwargs)
            try:
                response_read = response.json()
            except json.decoder.JSONDecodeError as e:
                ApiClientException(response=response, exc=e)
                response_read = response

            set_custom_context(
                dict(
                    request_data=response.request.body,
                    response_content=str(response_read)[:500],
                )
            )
            elasticapm.set_transaction_result(response.status_code)
            return response

    return request_log_wrapper
