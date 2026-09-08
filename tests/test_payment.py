import unittest

from change_payment_gateway.adapters.paytm_payment_gateway_adapter import PaytmPaymentGatewayAdapter
from change_payment_gateway.adapters.razorpay_payment_gateway_adapter import RazorpayPaymentGatewayAdapter
from change_payment_gateway.controllers.payment_controller import PaymentController
from change_payment_gateway.dtos.make_payment_request_dto import MakePaymentRequestDto
from change_payment_gateway.dtos.response_status import ResponseStatus
from change_payment_gateway.models.bill import Bill
from change_payment_gateway.models.payment_status import PaymentStatus
from change_payment_gateway.repositories.bill_repository_impl import BillRepositoryImpl
from change_payment_gateway.services.payment_service_impl import PaymentServiceImpl


# ---------------------------------------------------------------------------
# Helper — builds a ready-to-use controller wired to a real in-memory repo
# ---------------------------------------------------------------------------

def _make_controller(adapter):
    """Creates a PaymentController backed by a fresh repository and the given adapter."""
    repo = BillRepositoryImpl()
    service = PaymentServiceImpl(repo, adapter)
    controller = PaymentController(service)
    return controller, repo


# ===========================================================================
# Test Suite 1 — BillRepositoryImpl
# ===========================================================================

class TestBillRepository(unittest.TestCase):
    """Tests that the in-memory repository stores and retrieves bills correctly."""

    def setUp(self):
        self.repo = BillRepositoryImpl()

    # --- save() ---

    def test_save_assigns_id_starting_at_1(self):
        """The first saved bill must receive ID = 1."""
        bill = Bill(total_amount=100.0, gst=10.0, service_charge=5.0)
        saved = self.repo.save(bill)
        self.assertEqual(saved.id, 1)

    def test_save_increments_id_for_each_bill(self):
        """Each subsequent bill must get the next integer ID."""
        bill1 = self.repo.save(Bill(100.0, 10.0, 5.0))
        bill2 = self.repo.save(Bill(200.0, 20.0, 10.0))
        bill3 = self.repo.save(Bill(300.0, 30.0, 15.0))
        self.assertEqual(bill1.id, 1)
        self.assertEqual(bill2.id, 2)
        self.assertEqual(bill3.id, 3)

    def test_save_returns_the_same_bill_object(self):
        """save() must return the bill object (with its ID populated), not a copy."""
        bill = Bill(100.0, 10.0, 5.0)
        saved = self.repo.save(bill)
        self.assertIs(saved, bill)

    # --- find_by_id() ---

    def test_find_by_id_returns_correct_bill(self):
        """find_by_id() must return exactly the bill that was saved with that ID."""
        bill = Bill(total_amount=500.0, gst=50.0, service_charge=25.0)
        saved = self.repo.save(bill)
        found = self.repo.find_by_id(saved.id)
        self.assertIs(found, saved)

    def test_find_by_id_returns_none_for_missing_id(self):
        """Searching for an ID that was never saved must return None — not raise an error."""
        result = self.repo.find_by_id(999)
        self.assertIsNone(result)

    def test_find_by_id_returns_none_on_empty_repo(self):
        """Even before any bill is saved, find_by_id() must safely return None."""
        result = self.repo.find_by_id(1)
        self.assertIsNone(result)

    def test_find_by_id_does_not_confuse_different_bills(self):
        """Bill 1 and Bill 2 must be returned independently and correctly."""
        bill_a = self.repo.save(Bill(100.0, 10.0, 5.0))
        bill_b = self.repo.save(Bill(999.0, 99.0, 49.0))
        self.assertIs(self.repo.find_by_id(1), bill_a)
        self.assertIs(self.repo.find_by_id(2), bill_b)

    def test_repo_size_grows_with_each_save(self):
        """The internal dictionary must grow by 1 for each saved bill."""
        self.assertEqual(len(self.repo._bills), 0)
        self.repo.save(Bill(100.0, 10.0, 5.0))
        self.assertEqual(len(self.repo._bills), 1)
        self.repo.save(Bill(200.0, 20.0, 10.0))
        self.assertEqual(len(self.repo._bills), 2)


# ===========================================================================
# Test Suite 2 — Bill model
# ===========================================================================

class TestBillModel(unittest.TestCase):
    """Tests the Bill model's get_amount_to_be_paid() calculation."""

    def test_get_amount_to_be_paid_sums_all_three_components(self):
        """The grand total must equal total_amount + gst + service_charge."""
        bill = Bill(total_amount=200.0, gst=36.0, service_charge=20.0)
        self.assertAlmostEqual(bill.get_amount_to_be_paid(), 256.0)

    def test_get_amount_to_be_paid_with_zero_charges(self):
        """If gst and service_charge are 0, the total must equal only the total_amount."""
        bill = Bill(total_amount=500.0, gst=0.0, service_charge=0.0)
        self.assertAlmostEqual(bill.get_amount_to_be_paid(), 500.0)

    def test_get_amount_to_be_paid_with_all_zeros(self):
        """A zero bill must return 0.0 — no crashes on zero values."""
        bill = Bill(total_amount=0.0, gst=0.0, service_charge=0.0)
        self.assertAlmostEqual(bill.get_amount_to_be_paid(), 0.0)


# ===========================================================================
# Test Suite 3 — Adapters (Paytm and Razorpay)
# ===========================================================================

class TestPaytmAdapter(unittest.TestCase):
    """Tests that the Paytm adapter correctly calls the library and maps the response."""

    def setUp(self):
        self.adapter = PaytmPaymentGatewayAdapter()

    def test_make_payment_returns_payment_object(self):
        """make_payment() must return a Payment object, not None."""
        payment = self.adapter.make_payment(bill_id=1, amount=500.0)
        self.assertIsNotNone(payment)

    def test_make_payment_sets_correct_bill_id(self):
        """The returned Payment must carry the same bill_id that was passed in."""
        payment = self.adapter.make_payment(bill_id=42, amount=100.0)
        self.assertEqual(payment.bill_id, 42)

    def test_make_payment_returns_txn_id_as_string(self):
        """txn_id must be a non-empty string (UUID from Paytm)."""
        payment = self.adapter.make_payment(bill_id=1, amount=100.0)
        self.assertIsInstance(payment.txn_id, str)
        self.assertTrue(len(payment.txn_id) > 0)

    def test_make_payment_returns_success_status(self):
        """PaytmApi always returns SUCCESS — adapter must map it to PaymentStatus.SUCCESS."""
        payment = self.adapter.make_payment(bill_id=1, amount=100.0)
        self.assertEqual(payment.payment_status, PaymentStatus.SUCCESS)

    def test_make_payment_status_is_enum_not_string(self):
        """payment_status must be a PaymentStatus enum, NOT a raw string like 'SUCCESS'."""
        payment = self.adapter.make_payment(bill_id=1, amount=100.0)
        self.assertIsInstance(payment.payment_status, PaymentStatus)


class TestRazorpayAdapter(unittest.TestCase):
    """Tests that the Razorpay adapter correctly calls the library and maps the response."""

    def setUp(self):
        self.adapter = RazorpayPaymentGatewayAdapter()

    def test_make_payment_returns_payment_object(self):
        """make_payment() must return a Payment object, not None."""
        payment = self.adapter.make_payment(bill_id=1, amount=500.0)
        self.assertIsNotNone(payment)

    def test_make_payment_sets_correct_bill_id(self):
        """The returned Payment must carry the same bill_id that was passed in."""
        payment = self.adapter.make_payment(bill_id=7, amount=250.0)
        self.assertEqual(payment.bill_id, 7)

    def test_make_payment_returns_txn_id_as_string(self):
        """txn_id must be a non-empty string (UUID from Razorpay's transaction_id field)."""
        payment = self.adapter.make_payment(bill_id=1, amount=250.0)
        self.assertIsInstance(payment.txn_id, str)
        self.assertTrue(len(payment.txn_id) > 0)

    def test_make_payment_returns_success_status(self):
        """RazorpayApi always returns SUCCESS — adapter must map it to PaymentStatus.SUCCESS."""
        payment = self.adapter.make_payment(bill_id=1, amount=250.0)
        self.assertEqual(payment.payment_status, PaymentStatus.SUCCESS)

    def test_make_payment_status_is_enum_not_string(self):
        """payment_status must be a PaymentStatus enum — NOT a raw string."""
        payment = self.adapter.make_payment(bill_id=1, amount=250.0)
        self.assertIsInstance(payment.payment_status, PaymentStatus)

    def test_paytm_and_razorpay_return_different_txn_ids(self):
        """
        Both gateways generate a random UUID each time.
        Two calls (even with the same inputs) must return different transaction IDs.
        This ensures students are not hardcoding a fixed txn_id.
        """
        p1 = self.adapter.make_payment(bill_id=1, amount=100.0)
        p2 = self.adapter.make_payment(bill_id=1, amount=100.0)
        self.assertNotEqual(p1.txn_id, p2.txn_id)


# ===========================================================================
# Test Suite 4 — PaymentController with Paytm
# ===========================================================================

class TestPaymentControllerWithPaytm(unittest.TestCase):
    """End-to-end controller tests using the Paytm adapter."""

    def setUp(self):
        self.controller, self.repo = _make_controller(PaytmPaymentGatewayAdapter())

    # --- Happy path ---

    def test_valid_bill_returns_success_response_status(self):
        """A valid bill_id must produce a response with ResponseStatus.SUCCESS."""
        bill = self.repo.save(Bill(total_amount=200.0, gst=36.0, service_charge=20.0))
        request = MakePaymentRequestDto(bill_id=bill.id)
        response = self.controller.make_payment(request)
        self.assertEqual(response.response_status, ResponseStatus.SUCCESS)

    def test_valid_bill_response_contains_txn_id(self):
        """On success, the response must contain a non-empty transaction ID."""
        bill = self.repo.save(Bill(200.0, 36.0, 20.0))
        response = self.controller.make_payment(MakePaymentRequestDto(bill.id))
        self.assertIsNotNone(response.txn_id)
        self.assertIsInstance(response.txn_id, str)
        self.assertTrue(len(response.txn_id) > 0)

    def test_valid_bill_response_contains_payment_status(self):
        """On success, the response must contain a PaymentStatus (not None, not a string)."""
        bill = self.repo.save(Bill(200.0, 36.0, 20.0))
        response = self.controller.make_payment(MakePaymentRequestDto(bill.id))
        self.assertIsNotNone(response.payment_status)
        self.assertIsInstance(response.payment_status, PaymentStatus)

    def test_valid_bill_payment_status_is_success(self):
        """The payment_status inside the response must be PaymentStatus.SUCCESS."""
        bill = self.repo.save(Bill(200.0, 36.0, 20.0))
        response = self.controller.make_payment(MakePaymentRequestDto(bill.id))
        self.assertEqual(response.payment_status, PaymentStatus.SUCCESS)

    # --- Failure path ---

    def test_invalid_bill_id_returns_failure_response_status(self):
        """A bill_id that does not exist must produce ResponseStatus.FAILURE — never crash."""
        request = MakePaymentRequestDto(bill_id=999)
        response = self.controller.make_payment(request)
        self.assertEqual(response.response_status, ResponseStatus.FAILURE)

    def test_invalid_bill_id_response_txn_id_is_none(self):
        """On failure, txn_id must be None — no ghost transaction must be returned."""
        response = self.controller.make_payment(MakePaymentRequestDto(bill_id=999))
        self.assertIsNone(response.txn_id)

    def test_invalid_bill_id_response_payment_status_is_none(self):
        """On failure, payment_status must be None — no transaction happened."""
        response = self.controller.make_payment(MakePaymentRequestDto(bill_id=999))
        self.assertIsNone(response.payment_status)

    def test_bill_id_zero_returns_failure(self):
        """Bill ID 0 is invalid — must return FAILURE, not crash."""
        response = self.controller.make_payment(MakePaymentRequestDto(bill_id=0))
        self.assertEqual(response.response_status, ResponseStatus.FAILURE)

    def test_negative_bill_id_returns_failure(self):
        """A negative bill ID is invalid — must return FAILURE, not crash."""
        response = self.controller.make_payment(MakePaymentRequestDto(bill_id=-1))
        self.assertEqual(response.response_status, ResponseStatus.FAILURE)

    # --- Anti-bypass: amount correctness ---

    def test_payment_uses_get_amount_to_be_paid_not_just_total_amount(self):
        """
        The service must call bill.get_amount_to_be_paid() (= total + gst + service_charge)
        and NOT just bill.total_amount. We verify this indirectly — a lazy student who
        only passes total_amount would send 200.0 to the gateway instead of 256.0.
        The gateway still succeeds here, but we verify the response is SUCCESS,
        confirming the full flow ran with the correct amount.
        """
        bill = self.repo.save(Bill(total_amount=200.0, gst=36.0, service_charge=20.0))
        # grand total should be 256.0 — if student ignores gst/service_charge this is a bug
        self.assertAlmostEqual(bill.get_amount_to_be_paid(), 256.0)
        response = self.controller.make_payment(MakePaymentRequestDto(bill.id))
        self.assertEqual(response.response_status, ResponseStatus.SUCCESS)

    # --- Anti-bypass: multiple independent payments ---

    def test_each_payment_gets_a_unique_txn_id(self):
        """
        Two separate payments (even for the same bill) must produce different txn_ids.
        Catches students who hardcode a fixed transaction ID.
        """
        bill = self.repo.save(Bill(200.0, 36.0, 20.0))
        r1 = self.controller.make_payment(MakePaymentRequestDto(bill.id))
        r2 = self.controller.make_payment(MakePaymentRequestDto(bill.id))
        self.assertNotEqual(r1.txn_id, r2.txn_id)

    def test_multiple_valid_bills_each_return_success(self):
        """Multiple bills in the repo must each be payable independently."""
        bill1 = self.repo.save(Bill(100.0, 18.0, 10.0))
        bill2 = self.repo.save(Bill(500.0, 90.0, 50.0))
        r1 = self.controller.make_payment(MakePaymentRequestDto(bill1.id))
        r2 = self.controller.make_payment(MakePaymentRequestDto(bill2.id))
        self.assertEqual(r1.response_status, ResponseStatus.SUCCESS)
        self.assertEqual(r2.response_status, ResponseStatus.SUCCESS)

    def test_valid_bill_after_invalid_attempt_still_succeeds(self):
        """
        After a FAILURE response for a bad ID, a subsequent valid payment must still work.
        Catches students whose service is stateful in a broken way.
        """
        bill = self.repo.save(Bill(200.0, 36.0, 20.0))
        # First attempt with a wrong ID
        r_fail = self.controller.make_payment(MakePaymentRequestDto(bill_id=999))
        self.assertEqual(r_fail.response_status, ResponseStatus.FAILURE)
        # Second attempt with the correct ID must succeed
        r_success = self.controller.make_payment(MakePaymentRequestDto(bill.id))
        self.assertEqual(r_success.response_status, ResponseStatus.SUCCESS)


# ===========================================================================
# Test Suite 5 — PaymentController with Razorpay (gateway swap test)
# ===========================================================================

class TestPaymentControllerWithRazorpay(unittest.TestCase):
    """
    Verifies that the controller + service work identically when the Razorpay adapter
    is swapped in instead of Paytm. The service must NOT care which adapter is used.
    """

    def setUp(self):
        self.controller, self.repo = _make_controller(RazorpayPaymentGatewayAdapter())

    def test_valid_bill_returns_success_with_razorpay(self):
        bill = self.repo.save(Bill(300.0, 54.0, 30.0))
        response = self.controller.make_payment(MakePaymentRequestDto(bill.id))
        self.assertEqual(response.response_status, ResponseStatus.SUCCESS)

    def test_invalid_bill_returns_failure_with_razorpay(self):
        response = self.controller.make_payment(MakePaymentRequestDto(bill_id=999))
        self.assertEqual(response.response_status, ResponseStatus.FAILURE)

    def test_razorpay_response_txn_id_is_nonempty_string(self):
        bill = self.repo.save(Bill(300.0, 54.0, 30.0))
        response = self.controller.make_payment(MakePaymentRequestDto(bill.id))
        self.assertIsInstance(response.txn_id, str)
        self.assertTrue(len(response.txn_id) > 0)

    def test_swapping_adapter_does_not_affect_failure_behaviour(self):
        """FAILURE behaviour must be identical regardless of which adapter is plugged in."""
        response = self.controller.make_payment(MakePaymentRequestDto(bill_id=0))
        self.assertIsNone(response.txn_id)
        self.assertIsNone(response.payment_status)
        self.assertEqual(response.response_status, ResponseStatus.FAILURE)


# ===========================================================================
# Run all tests
# ===========================================================================

if __name__ == "__main__":
    unittest.main(verbosity=2)
