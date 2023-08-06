from io import BytesIO
import json

from rest_framework import status

from django.conf import settings

invalid_token_response = {
    "detail": "Given token not valid for any token type",
    "code": "token_not_valid",
    "messages": [
        {
            "tokenClass": "AccessToken",
            "tokenType": "access",
            "message": "Token is invalid or expired"
        }
    ]
}

token = f'Bearer {settings.PHARMZAKAZTOKEN}'

invalid_data_response = {
    "detail": "Error in received data",
    "code": "data_not_valid",
    "fields": ""
}


def sort_list_dict_in_data(key_field, data_dict: dict):
    if isinstance(data_dict, dict):
        for key in data_dict.keys():
            if isinstance(data_dict.get(key), list):
                value = sorted(data_dict.get(key), key=lambda x: x[key_field])
                data_dict.update({key: value})
    return data_dict


def verif_data_request(url, orig_data, verif_data, key_field):
    if key_field:
        orig_data = sort_list_dict_in_data(key_field, orig_data)
        verif_data = sort_list_dict_in_data(key_field, verif_data)

    if orig_data != verif_data:
        print(url)
        print("orig_data = ", orig_data)
        print("verif_data = ", verif_data)
        return


class Request:
    def __init__(self, body):
        self.body = body


class MockResponse:
    def __init__(self, json_data, status_code, body=None):
        self.json_data = json_data
        self.status_code = status_code
        self.request = Request(body)

    def json(self):
        return self.json_data

    def read(self):
        if self._content is None:
            response = self._request.read()
            self._content = BytesIO()
            self._content.write(response)
            self._content.seek(0)
            return response
        else:
            response = self._content.read()
            self._content.seek(0)
            return response


class MockRequests:

    def get_request(self, *args, **kwargs):
        self.mock_url = args[0]
        self.mock_headers = kwargs.get("headers")
        self.mock_Authorization = self.mock_headers.get("Authorization")
        self.mock_body = json.loads(kwargs.get("data"))
        if hasattr(self, "data_post"):
            key_field = None
            if hasattr(self, "key_field"):
                key_field = self.key_field
            self.mock_errors_fields = verif_data_request(self.mock_url, self.data_post, self.mock_body, key_field)

    def return_page_not_found(self):
        msg = "Page not found"
        print(msg, self.mock_url, self.url)
        return MockResponse(msg, status.HTTP_404_NOT_FOUND)

    # Этот метод будет использоваться макетом для замены request.get
    def mocked_requests_get(self, *args, **kwargs):
        self.get_request(*args, **kwargs)
        if self.mock_Authorization == token:
            if self.url == self.mock_url:
                return MockResponse(self.response_get, status.HTTP_200_OK)
            else:
                return self.return_page_not_found()
        else:
            return MockResponse(invalid_token_response, status.HTTP_401_UNAUTHORIZED)

    # Этот метод будет использоваться макетом для замены request.post
    def mocked_requests_post(self, *args, **kwargs):
        self.get_request(*args, **kwargs)
        if self.mock_Authorization == token and not self.mock_errors_fields:
            if self.url == self.mock_url:
                return MockResponse(self.response_post, status.HTTP_201_CREATED, body=self.mock_body)
            else:
                return self.return_page_not_found()
        elif self.mock_Authorization != token:
            return MockResponse(invalid_token_response, status.HTTP_401_UNAUTHORIZED)
        elif self.mock_errors_fields:
            return MockResponse(invalid_data_response.update({"fields": self.mock_errors_fields}),
                                status.HTTP_400_BAD_REQUEST)
        else:
            return MockResponse(None, status.HTTP_404_NOT_FOUND)

    # Этот метод будет использоваться макетом для замены request.patch
    def mocked_requests_patch(self, *args, **kwargs):
        self.get_request(*args, **kwargs)
        if self.mock_Authorization == token and not self.mock_errors_fields:
            if self.url == self.mock_url:
                return MockResponse(self.response_patch, status.HTTP_200_OK)
            else:
                return self.return_page_not_found()
        elif self.mock_Authorization != token:
            return MockResponse(invalid_token_response, status.HTTP_401_UNAUTHORIZED)
        elif self.mock_errors_fields:
            return MockResponse(invalid_data_response.update({"fields": self.mock_errors_fields}),
                                status.HTTP_400_BAD_REQUEST)
        else:
            return MockResponse(None, status.HTTP_404_NOT_FOUND)
