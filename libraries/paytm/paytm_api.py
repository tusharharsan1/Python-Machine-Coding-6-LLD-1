import uuid
from datetime import datetime
from change_payment_gateway.libraries.paytm.paytm_payment_response import PaytmPaymentResponse


class PaytmApi:
    """
    Simulates the Paytm payment gateway API.
    In a real system, this class would make HTTP calls to Paytm's servers.
    Here it is pre-built to simulate a successful payment response.

    You do NOT need to modify this class — just use it through the adapter.
    """

    def make_payment(self, order_id: int, amount: float) -> PaytmPaymentResponse:
        """
        Initiates a payment request to Paytm.

        Args:
            order_id : the bill ID being paid
            amount   : the total amount to charge

        Returns:
            A PaytmPaymentResponse containing the transaction details.
        """
        response = PaytmPaymentResponse()
        response.order_id = str(order_id)
        response.payment_status = "SUCCESS"
        response.txn_amount = amount
        response.txn_date = datetime.now()
        response.txn_id = str(uuid.uuid4())
        return response
