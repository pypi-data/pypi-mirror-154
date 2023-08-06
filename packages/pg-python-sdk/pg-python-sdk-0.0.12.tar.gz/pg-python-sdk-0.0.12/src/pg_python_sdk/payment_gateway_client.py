from pg_python_sdk.payment_gateway_response import PaymentGatewayResponse
from pg_python_sdk.payment_gateway_request import PaymentGatewayRequest


class PaymentGatewayClient:

    def __init__(self, key: str):
        self.httpClient = PaymentGatewayRequest(key)

    def get_balance(self) -> PaymentGatewayResponse:
        """
        Get a balance for the app
        """
        return self.httpClient.get('balance')

    def get_transaction(self, transaction_uuid: str) -> PaymentGatewayResponse:
        """
        Get a specific transaction for the app
        """
        return self.httpClient.get(f'transactions/{transaction_uuid}')

    def get_transactions(self, from_date: str, to_date: str) -> PaymentGatewayResponse:
        """
        Get a list of transactions for the app
        """
        return self.httpClient.post('transactions', {
            'from_date': from_date,
            'to_date': to_date
        })

    def create_transaction(
            self,
            amount: float,
            success_redirect_url: str,
            error_redirect_url: str,
            cancel_redirect_url: str,
            notify_url: str
    ) -> PaymentGatewayResponse:
        """
        Create a pending transaction for the app
        """
        return self.httpClient.post('transactions/create', {
            'amount': amount,
            'success_redirect_url': success_redirect_url,
            'error_redirect_url': error_redirect_url,
            'cancel_redirect_url': cancel_redirect_url,
            'notify_url': notify_url
        })

    def refund(self, transaction_uuid: str, amount: float, reason: str) -> PaymentGatewayResponse:
        """
        Refund for previous transactions
        """
        return self.httpClient.post('transactions/refund', {
            'transaction_uuid': transaction_uuid,
            'amount': amount,
            'reason': reason
        })


    def transfer(self, phone_number: str, amount: float, reason: str) -> PaymentGatewayResponse:
        """
        Refund for previous transactions
        """
        return self.httpClient.post('transfer', {
            'phone_number': phone_number,
            'amount': amount,
            'reason': reason
        })
