from change_payment_gateway.models.base_model import BaseModel


class Bill(BaseModel):
    """
    Represents the final bill generated for a customer's session.

    The bill is made up of three parts:
      - total_amount    : the cost of all food items ordered
      - gst             : government tax applied on the total amount
      - service_charge  : the restaurant's service fee

    Use get_amount_to_be_paid() to get the grand total the customer must pay.
    This is the amount that will be sent to the payment gateway.
    """

    def __init__(self, total_amount: float, gst: float, service_charge: float):
        super().__init__()
        self.total_amount = total_amount
        self.gst = gst
        self.service_charge = service_charge

    def get_amount_to_be_paid(self) -> float:
        """Returns the grand total: food cost + GST + service charge."""
        return self.total_amount + self.gst + self.service_charge
