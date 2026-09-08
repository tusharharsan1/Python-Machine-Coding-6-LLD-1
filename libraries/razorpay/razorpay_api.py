import uuid
from datetime import datetime
from change_payment_gateway.libraries.razorpay.razorpay_payment_response import RazorpayPaymentResponse


class RazorpayApi:
    """
    Simulates the Razorpay payment gateway API.
    In a real system, this class would make HTTP calls to Razorpay's servers.
    Here it is pre-built to simulate a successful payment response.

    You do NOT need to modify this class — just use it through the adapter.
    """

    def process_payment(self, order_id: int, transaction_amount: float) -> RazorpayPaymentResponse:
        """
        Initiates a payment request to Razorpay.

        Args:
            order_id           : the bill ID being paid
            transaction_amount : the total amount to charge

        Returns:
            A RazorpayPaymentResponse containing the transaction details.
        """
        response = RazorpayPaymentResponse()
        response.transaction_id = str(uuid.uuid4())
        response.payment_status = "SUCCESS"
        response.order_id = str(order_id)
        response.transaction_amount = transaction_amount
        response.transaction_date = datetime.now()
        return response
