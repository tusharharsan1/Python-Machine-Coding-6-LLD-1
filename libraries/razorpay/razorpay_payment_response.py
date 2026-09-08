import uuid
from datetime import datetime


class RazorpayPaymentResponse:
    """
    The response object that Razorpay sends back after processing a payment.
    This is a pre-built library class — you do NOT need to modify this.

    Note: Razorpay uses different field names than Paytm:
      - transaction_id     (not txn_id)
      - transaction_amount (not txn_amount)
      - transaction_date   (not txn_date)

    This difference in field names is exactly WHY we need an Adapter —
    so our system always works with a consistent interface regardless of the gateway.

    Attributes:
        transaction_id     : Razorpay's unique transaction ID
        payment_status     : "SUCCESS" or "FAILURE" as a plain string from Razorpay
        order_id           : the bill ID we sent (returned as a string)
        transaction_amount : the amount that was charged
        transaction_date   : the date and time the transaction occurred
    """

    def __init__(self):
        self.transaction_id: str = ""
        self.payment_status: str = ""
        self.order_id: str = ""
        self.transaction_amount: float = 0.0
        self.transaction_date: datetime = datetime.now()
