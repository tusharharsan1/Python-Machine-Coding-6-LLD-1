from abc import ABC, abstractmethod
from change_payment_gateway.exceptions.invalid_bill_exception import InvalidBillException
from change_payment_gateway.models.payment import Payment


class PaymentService(ABC):
    """
    Defines the contract for the payment service — the core business logic layer.

    The service is responsible for:
      1. Validating that the bill exists
      2. Fetching the amount to be paid
      3. Calling the payment gateway (through the adapter) to process the payment
      4. Returning the Payment result

    TODO (for student):
    -------------------
    Create a concrete class called PaymentServiceImpl that implements this ABC.
    The constructor of PaymentServiceImpl should accept TWO dependencies:
      - A BillRepository (to fetch the bill details)
      - A PaymentGatewayAdapter (to make the actual payment)

    Implement:
      1. make_payment(bill_id):
           Step 1 -> Use the repository to look up the bill by its ID.
           Step 2 -> If the bill is NOT found (repository returned None),
                     raise InvalidBillException("Invalid bill id").
           Step 3 -> If the bill IS found, call get_amount_to_be_paid() on the bill
                     to get the total amount.
           Step 4 -> Call make_payment() on the adapter, passing the bill_id and amount.
           Step 5 -> Return the Payment object you get back from the adapter.
    """

    @abstractmethod
    def make_payment(self, bill_id: int) -> Payment:
        """
        Processes the payment for a given bill.

        Args:
            bill_id : the ID of the bill to be paid

        Returns:
            A Payment object containing the transaction result.

        Raises:
            InvalidBillException: if the provided bill_id does not exist in the repository.
        """
        pass
