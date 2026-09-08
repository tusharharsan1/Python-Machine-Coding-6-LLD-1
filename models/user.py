from change_payment_gateway.models.base_model import BaseModel
from change_payment_gateway.models.user_type import UserType


class User(BaseModel):
    """
    Represents a person who uses the restaurant system.
    A user can be a Customer (someone dining) or an Admin (staff managing the system).
    """

    def __init__(self, name: str, password: str, phone: str, user_type: UserType):
        super().__init__()
        self.name = name
        self.password = password
        self.phone = phone
        self.user_type = user_type
