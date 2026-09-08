from change_payment_gateway.adapters.payment_gateway_adapter import PaymentGatewayAdapter
from change_payment_gateway.libraries.razorpay.razorpay_api import RazorpayApi
from change_payment_gateway.models.payment import Payment
from change_payment_gateway.models.payment_status import PaymentStatus


class RazorpayPaymentGatewayAdapter(PaymentGatewayAdapter):
    """
    Adapts the Razorpay library to our system's standard PaymentGatewayAdapter interface.

    Razorpay is different from Paytm in two important ways:
      1. Its method is called process_payment() instead of make_payment()
      2. Its transaction ID field is called transaction_id instead of txn_id

    This adapter hides those differences. Our service still just calls make_payment()
    on the adapter — it has no idea which gateway is actually being used underneath.
    """

    def __init__(self):
        # We create a RazorpayApi instance here — same pattern as the Paytm adapter.
        self._razorpay_api = RazorpayApi()

    def make_payment(self, bill_id: int, amount: float) -> Payment:
        # Call the Razorpay library — note: Razorpay calls its method process_payment()
        # and uses 'transaction_amount' as the parameter name (not 'amount')
        razorpay_response = self._razorpay_api.process_payment(bill_id, amount)

        # Convert the string status e.g. "SUCCESS" → PaymentStatus.SUCCESS (same as Paytm)
        payment_status = PaymentStatus[razorpay_response.payment_status]

        # Note: Razorpay uses transaction_id, not txn_id — the adapter handles this mapping
        return Payment(
            txn_id=razorpay_response.transaction_id,
            payment_status=payment_status,
            bill_id=bill_id,
        )
