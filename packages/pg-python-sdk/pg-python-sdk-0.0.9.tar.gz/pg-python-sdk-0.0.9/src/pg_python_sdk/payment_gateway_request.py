

import json
from requests import Response, Session, Request
from pg_python_sdk.payment_gateway_response import PaymentGatewayResponse
import urllib3
urllib3.disable_warnings()

class PaymentGatewayRequest:

    def __init__(self, key: str):
        self.key = key

    def send_request(self, method: str, uri: str, data: dict = None) -> Response:
        _session = Session()
        _request = Request(
            method,
            f'https://134.122.118.178/api/v1/{uri}',
            data=json.dumps(data),
            headers={
                'Authorization': f'Bearer {self.key}',
                'Content-Type': 'application/json'
            }
        )

        _prepared = _request.prepare()
        _response = _session.send(
            _prepared, verify=False, allow_redirects=False)

        return _response

    def get(self, uri: str, data: dict = None) -> Response:
        return PaymentGatewayResponse(self.send_request('GET', uri, data))

    def post(self, uri: str, data: dict = None) -> Response:
        return PaymentGatewayResponse(self.send_request('POST', uri, data))
