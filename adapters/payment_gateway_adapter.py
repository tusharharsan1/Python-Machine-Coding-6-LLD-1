from abc import ABC, abstractmethod
from change_payment_gateway.models.payment import Payment


class PaymentGatewayAdapter(ABC):
    """
    The common interface (contract) that every payment gateway adapter must follow.

    WHY DO WE NEED THIS?
    --------------------
    Paytm and Razorpay are completely different APIs with different method names
    and different response objects. Without this adapter, our service would need
    to know about the internals of each gateway — making it impossible to switch
    gateways without rewriting the service.

    With this adapter, the PaymentService only ever calls make_payment() through
    this interface. Switching from Paytm to Razorpay (or any future gateway)
    becomes a single-line change — just swap the adapter. This is the
    "Adapter" design pattern and one of the SOLID principles (Open/Closed).

    TODO (for student):
    -------------------
    You need to create TWO concrete classes that implement this abstract class:
      1. PaytmPaymentGatewayAdapter  -> wraps PaytmApi
      2. RazorpayPaymentGatewayAdapter -> wraps RazorpayApi

    Each class must implement the make_payment() method below, calling the
    respective library API and mapping its response to a Payment object.
    """

    @abstractmethod
    def make_payment(self, bill_id: int, amount: float) -> Payment:
        """
        Processes a payment through the gateway.

        Args:
            bill_id : the ID of the bill being paid (used as the order reference)
            amount  : the exact amount (in rupees) to charge

        Returns:
            A Payment object containing the txn_id, payment_status, and bill_id.
        """
        pass
