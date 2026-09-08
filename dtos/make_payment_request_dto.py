class MakePaymentRequestDto:
    """
    The input object sent to the makePayment functionality.

    Attributes:
        bill_id : the ID of the bill the customer wants to pay
    """

    def __init__(self, bill_id: int):
        self.bill_id = bill_id
