from change_payment_gateway.dtos.make_payment_request_dto import MakePaymentRequestDto
from change_payment_gateway.dtos.make_payment_response_dto import MakePaymentResponseDto
from change_payment_gateway.dtos.response_status import ResponseStatus
from change_payment_gateway.services.payment_service import PaymentService


class PaymentController:
    """
    The controller acts as the entry point for the make payment feature.
    It receives a request, delegates the work to the service, and returns a response.

    The controller itself does NOT contain any business logic — it only:
      1. Passes the request data to the service
      2. Catches exceptions from the service
      3. Wraps the result (or error) into a response DTO
    """

    def __init__(self, payment_service: PaymentService):
        self.payment_service = payment_service

    def make_payment(self, request: MakePaymentRequestDto) -> MakePaymentResponseDto:
        """
        Handles a make payment request from end to end.

        Args:
            request : a MakePaymentRequestDto containing the bill_id to be paid

        Returns:
            A MakePaymentResponseDto with:
              - response_status = SUCCESS and the transaction details, if everything worked
              - response_status = FAILURE, if the bill_id was invalid

        TODO (Step 1):
            Extract the bill_id from the request object.
            Hint: request.bill_id

        TODO (Step 2):
            Call self.payment_service.make_payment(bill_id) inside a try block.
            This method can raise an InvalidBillException — make sure you handle it.

        TODO (Step 3):
            If the call succeeds, build and return a MakePaymentResponseDto with:
              - response_status = ResponseStatus.SUCCESS
              - txn_id          = the txn_id from the returned Payment object
              - payment_status  = the payment_status from the returned Payment object

        TODO (Step 4):
            In the except block, catch InvalidBillException.
            If it is raised, build and return a MakePaymentResponseDto with:
              - response_status = ResponseStatus.FAILURE
              - txn_id          = None  (no transaction happened)
              - payment_status  = None  (no transaction happened)

        NOTE:
            Import InvalidBillException from:
            change_payment_gateway.exceptions.invalid_bill_exception
        """
        # ↓↓↓ Write your code below this line ↓↓↓

        pass

        # ↑↑↑ Write your code above this line ↑↑↑
