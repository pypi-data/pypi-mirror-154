import json
from types import SimpleNamespace

from requests import Response


class PaymentGatewayResponse:

    def __init__(self, response: Response):
        self.status = response.status_code
        # self.body = json.loads(
        #     response.text,
        #     object_hook=lambda data: SimpleNamespace(**data)
        # )
        self.body =  response.text
