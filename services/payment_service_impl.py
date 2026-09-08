from change_payment_gateway.services.payment_service import PaymentService
from change_payment_gateway.repositories.bill_repository import BillRepository
from change_payment_gateway.adapters.payment_gateway_adapter import PaymentGatewayAdapter
from change_payment_gateway.exceptions.invalid_bill_exception import InvalidBillException
from change_payment_gateway.models.payment import Payment


class PaymentServiceImpl(PaymentService):
    """
    The concrete implementation of the PaymentService.

    This class contains the core business logic for processing a payment:
      1. Check that the bill actually exists in the system
      2. Get the total amount from the bill
      3. Send the payment to the gateway via the adapter
      4. Return the result

    Notice that this class depends on:
      - A BillRepository  (to fetch bill data)
      - A PaymentGatewayAdapter (to process the payment)

    Both of these are INTERFACES (abstract classes). This means we can swap out
    the implementation (e.g., switch from Paytm to Razorpay) without changing
    a single line of this service. This is Dependency Injection + the Open/Closed principle.
    """

    def __init__(self, bill_repository: BillRepository, payment_gateway_adapter: PaymentGatewayAdapter):
        self._bill_repository = bill_repository
        self._payment_gateway_adapter = payment_gateway_adapter

    def make_payment(self, bill_id: int) -> Payment:
        # Step 1: Try to find the bill in the repository
        bill = self._bill_repository.find_by_id(bill_id)

        # Step 2: If the bill doesn't exist, raise our custom exception.
        # The controller will catch this and return a FAILURE response.
        if bill is None:
            raise InvalidBillException("Invalid bill id")

        # Step 3: The bill exists — calculate how much the customer needs to pay.
        # get_amount_to_be_paid() adds total_amount + gst + service_charge together.
        amount_to_be_paid = bill.get_amount_to_be_paid()

        # Step 4: Send the payment to whichever gateway is plugged in via the adapter.
        # We don't know (or care) if it's Paytm or Razorpay — the adapter handles that.
        payment = self._payment_gateway_adapter.make_payment(bill_id, amount_to_be_paid)

        # Step 5: Return the Payment result (contains txn_id and payment_status)
        return payment
