from change_payment_gateway.models.base_model import BaseModel
from change_payment_gateway.models.user import User
from change_payment_gateway.models.customer_session_status import CustomerSessionStatus


class CustomerSession(BaseModel):
    """
    Represents one visit of a customer to the restaurant.
    A session is ACTIVE while the customer is dining and ENDED when they leave.
    The same customer can have multiple sessions over different visits.
    """

    def __init__(self, user: User, customer_session_status: CustomerSessionStatus):
        super().__init__()
        self.user = user
        self.customer_session_status = customer_session_status

    def is_active(self) -> bool:
        """Returns True if this session is currently active (customer is still dining)."""
        return self.customer_session_status == CustomerSessionStatus.ACTIVE
