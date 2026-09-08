from enum import Enum


class UserType(Enum):
    """
    Distinguishes the role of a user in the system.
    CUSTOMER -> a regular dining customer
    ADMIN    -> a staff member who manages the system
    """
    CUSTOMER = "CUSTOMER"
    ADMIN = "ADMIN"
