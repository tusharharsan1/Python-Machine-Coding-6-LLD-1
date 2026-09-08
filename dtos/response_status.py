from enum import Enum


class ResponseStatus(Enum):
    """
    Used by the controller to communicate the overall result of an operation
    back to the caller (e.g., the client/UI).

    SUCCESS -> the operation completed without any errors
    FAILURE -> something went wrong (e.g., invalid bill ID, payment error)
    """
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
