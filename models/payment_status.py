from enum import Enum


class PaymentStatus(Enum):
    """
    Indicates the final result of a payment transaction.
    SUCCESS -> the payment was processed and money was collected
    FAILURE -> the payment did not go through
    """
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
