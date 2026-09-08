from change_payment_gateway.adapters.payment_gateway_adapter import PaymentGatewayAdapter
from change_payment_gateway.libraries.paytm.paytm_api import PaytmApi
from change_payment_gateway.models.payment import Payment
from change_payment_gateway.models.payment_status import PaymentStatus


class PaytmPaymentGatewayAdapter(PaymentGatewayAdapter):
    """
    Adapts the Paytm library to our system's standard PaymentGatewayAdapter interface.

    The Paytm library calls its method 'make_payment()' and returns a PaytmPaymentResponse.
    This adapter's job is to:
      1. Call the Paytm API using its own method name and argument style
      2. Convert the Paytm-specific response into our system's standard Payment object

    This means the rest of our system (the service) never needs to know it's talking to Paytm.
    """

    def __init__(self):
        # We create a PaytmApi instance here. The service only ever calls make_payment()
        # through the PaymentGatewayAdapter interface — it never touches PaytmApi directly.
        self._paytm_api = PaytmApi()

    def make_payment(self, bill_id: int, amount: float) -> Payment:
        # Call the Paytm library — Paytm names its method make_payment()
        paytm_response = self._paytm_api.make_payment(bill_id, amount)

        # Paytm returns payment_status as a plain string e.g. "SUCCESS".
        # We convert it to our PaymentStatus enum using dictionary-style lookup.
        # PaymentStatus["SUCCESS"] gives us PaymentStatus.SUCCESS
        payment_status = PaymentStatus[paytm_response.payment_status]

        # Build and return our standard Payment object
        return Payment(
            txn_id=paytm_response.txn_id,
            payment_status=payment_status,
            bill_id=bill_id,
        )
