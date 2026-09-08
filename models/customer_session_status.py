from enum import Enum


class CustomerSessionStatus(Enum):
    """
    Represents whether a customer's dining session is still ongoing or has ended.
    ACTIVE  -> the customer is currently at the restaurant
    ENDED   -> the customer has finished and left
    """
    ACTIVE = "ACTIVE"
    ENDED = "ENDED"
