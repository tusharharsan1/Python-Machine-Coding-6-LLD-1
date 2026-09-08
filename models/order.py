from typing import Dict
from change_payment_gateway.models.base_model import BaseModel
from change_payment_gateway.models.customer_session import CustomerSession
from change_payment_gateway.models.menu_item import MenuItem


class Order(BaseModel):
    """
    Represents a food order placed during a customer's session.
    It stores which session placed the order and a dictionary of
    {MenuItem: quantity} — i.e., which items were ordered and how many of each.
    """

    def __init__(self, customer_session: CustomerSession, ordered_items: Dict[MenuItem, int]):
        super().__init__()
        self.customer_session = customer_session
        self.ordered_items = ordered_items
