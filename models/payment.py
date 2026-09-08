from change_payment_gateway.models.payment_status import PaymentStatus


class Payment:
    """
    Stores the result of a completed payment transaction.

    Attributes:
        txn_id         : the unique transaction ID returned by the payment gateway
        payment_status : SUCCESS or FAILURE, indicating if the payment went through
        bill_id        : the ID of the bill this payment was made for
    """

    def __init__(self, txn_id: str, payment_status: PaymentStatus, bill_id: int):
        self.txn_id = txn_id
        self.payment_status = payment_status
        self.bill_id = bill_id
