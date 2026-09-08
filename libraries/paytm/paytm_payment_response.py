import uuid
from datetime import datetime


class PaytmPaymentResponse:
    """
    The response object that Paytm sends back after processing a payment.
    This is a pre-built library class — you do NOT need to modify this.

    Attributes:
        txn_id         : Paytm's unique transaction ID
        payment_status : "SUCCESS" or "FAILURE" as a plain string from Paytm
        order_id       : the bill ID we sent to Paytm (returned as a string)
        txn_amount     : the amount that was charged
        txn_date       : the date and time the transaction occurred
    """

    def __init__(self):
        self.txn_id: str = ""
        self.payment_status: str = ""
        self.order_id: str = ""
        self.txn_amount: float = 0.0
        self.txn_date: datetime = datetime.now()
