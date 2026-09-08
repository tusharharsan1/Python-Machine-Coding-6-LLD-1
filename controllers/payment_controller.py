from change_payment_gateway.dtos.make_payment_request_dto import MakePaymentRequestDto
from change_payment_gateway.dtos.make_payment_response_dto import MakePaymentResponseDto
from change_payment_gateway.dtos.response_status import ResponseStatus
from change_payment_gateway.exceptions.invalid_bill_exception import InvalidBillException
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
        """
        try:
            # Step 1: Extract the bill_id from the incoming request
            bill_id = request.bill_id

            # Step 2: Delegate to the service — this is where the real work happens.
            # If the bill_id is invalid, the service will raise InvalidBillException.
            payment = self.payment_service.make_payment(bill_id)

            # Step 3: Payment succeeded — build a SUCCESS response with transaction details
            return MakePaymentResponseDto(
                response_status=ResponseStatus.SUCCESS,
                txn_id=payment.txn_id,
                payment_status=payment.payment_status,
            )

        except InvalidBillException:
            # Step 4: The bill_id did not exist — return a FAILURE response.
            # We set txn_id and payment_status to None because no transaction was made.
            return MakePaymentResponseDto(
                response_status=ResponseStatus.FAILURE,
                txn_id=None,
                payment_status=None,
            )
