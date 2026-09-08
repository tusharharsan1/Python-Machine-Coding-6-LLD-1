# Integrate Payment Gateway — Restaurant Management System

## What is this problem about?

You are working on a **Restaurant Management System**. Customers order food, a bill is generated,
and when they are ready to leave, they pay their bill through a **payment gateway** (like Paytm or Razorpay).

Your job is to wire up the payment feature so that:
1. The system looks up the bill using the bill ID
2. It sends the total amount to the payment gateway to collect payment
3. It returns the transaction result to the caller

---

## The Big Picture — How the code is organised

```
change_payment_gateway/
│
├── libraries/          ← Pre-built (DO NOT modify these)
│   ├── paytm/          ← PaytmApi and its response class
│   └── razorpay/       ← RazorpayApi and its response class
│
├── models/             ← Data classes (Bill, Payment, enums, etc.)
├── dtos/               ← Input/Output objects for the controller
├── exceptions/         ← Custom exceptions you need to raise/catch
│
├── adapters/           ← ⭐ YOU implement the concrete adapter classes here
├── repositories/       ← ⭐ YOU implement BillRepositoryImpl here
├── services/           ← ⭐ YOU implement PaymentServiceImpl here
└── controllers/        ← ⭐ YOU complete the make_payment() method here
```

---

## What do Paytm and Razorpay look like?

Both are pre-built for you in the `libraries/` folder. Study them carefully before starting.

| | **Paytm** | **Razorpay** |
|---|---|---|
| Class | `PaytmApi` | `RazorpayApi` |
| Method to call | `make_payment(order_id, amount)` | `process_payment(order_id, transaction_amount)` |
| Response class | `PaytmPaymentResponse` | `RazorpayPaymentResponse` |
| Transaction ID field | `response.txn_id` | `response.transaction_id` |
| Status field | `response.payment_status` → `"SUCCESS"` or `"FAILURE"` (string) | same |

Notice that Paytm and Razorpay have **different method names** and **different field names** in
their responses. This is the exact problem the **Adapter pattern** solves.

---

## What you need to implement

### ⭐ Task 1 — Two Adapter Classes (in `adapters/`)

The abstract class `PaymentGatewayAdapter` defines a single method:
```python
def make_payment(self, bill_id: int, amount: float) -> Payment:
```

You must create **two concrete adapter classes** that each implement this method:

**`PaytmPaymentGatewayAdapter`**
- Create an instance of `PaytmApi` inside this class
- In `make_payment()`, call `paytm_api.make_payment(bill_id, amount)`
- Map the `PaytmPaymentResponse` fields to a `Payment` object and return it
- The `payment_status` from Paytm is a plain string (`"SUCCESS"`). You need to convert it
  to the `PaymentStatus` enum: `PaymentStatus["SUCCESS"]`

**`RazorpayPaymentGatewayAdapter`**
- Create an instance of `RazorpayApi` inside this class
- In `make_payment()`, call `razorpay_api.process_payment(bill_id, amount)`
- Map the `RazorpayPaymentResponse` fields to a `Payment` object and return it
- Same string-to-enum conversion for `payment_status`

> **Note:** The `Payment` model has three fields: `txn_id`, `payment_status`, and `bill_id`.

---

### ⭐ Task 2 — BillRepositoryImpl (in `repositories/`)

The abstract class `BillRepository` defines two methods: `save()` and `find_by_id()`.

Create a concrete class `BillRepositoryImpl` that implements these:

- Use a **Python dictionary** as your in-memory database: `self._bills = {}`
- Use an integer counter for auto-incrementing IDs: `self._current_id = 1`

**`save(bill)`**
- Assign the current `_current_id` to `bill.id`
- Store it: `self._bills[bill.id] = bill`
- Increment `_current_id`
- Return the bill

**`find_by_id(bill_id)`**
- Look up `self._bills.get(bill_id)`
- Return the `Bill` if found, or `None` if not found

---

### ⭐ Task 3 — PaymentServiceImpl (in `services/`)

The abstract class `PaymentService` defines one method: `make_payment(bill_id)`.

Create a concrete class `PaymentServiceImpl` that implements this:

- The constructor takes two arguments: a `BillRepository` and a `PaymentGatewayAdapter`
- In `make_payment(bill_id)`:
  1. Call `self.bill_repository.find_by_id(bill_id)` to fetch the bill
  2. If the result is `None`, raise `InvalidBillException("Invalid bill id")`
  3. Otherwise, call `bill.get_amount_to_be_paid()` to get the total amount
  4. Call `self.payment_gateway_adapter.make_payment(bill_id, amount)`
  5. Return the `Payment` object received from the adapter

---

### ⭐ Task 4 — Complete PaymentController (in `controllers/payment_controller.py`)

The `make_payment()` method in `PaymentController` is currently empty. Fill it in:

1. Extract `bill_id` from the request: `request.bill_id`
2. Call `self.payment_service.make_payment(bill_id)` inside a `try` block
3. **If successful**, return a `MakePaymentResponseDto` with:
   - `response_status = ResponseStatus.SUCCESS`
   - `txn_id` = the `txn_id` from the returned `Payment` object
   - `payment_status` = the `payment_status` from the returned `Payment` object
4. **In the `except` block**, catch `InvalidBillException`. Return a `MakePaymentResponseDto` with:
   - `response_status = ResponseStatus.FAILURE`
   - `txn_id = None`
   - `payment_status = None`

---

## Key concepts to remember

- **Abstract Base Class (ABC)**: A class with `@abstractmethod` methods that defines a contract.
  Any class that inherits from it **must** implement all the abstract methods.

- **Adapter Pattern**: A wrapper class that translates one interface into another.
  Here, both Paytm and Razorpay adapters translate their gateway-specific responses
  into our system's standard `Payment` object.

- **`PaymentStatus["SUCCESS"]`**: This is how you convert a string like `"SUCCESS"` into
  a Python Enum value. If an invalid string is passed, Python will raise a `KeyError` automatically.

- **`Optional[Bill]`**: This type hint means the function can return either a `Bill` or `None`.
  Always check for `None` before using the result.

---

## Files you should NOT modify

- Anything inside `libraries/` (Paytm and Razorpay APIs)
- `models/` (all model and enum files)
- `dtos/` (request/response DTOs)
- `exceptions/invalid_bill_exception.py`
- `adapters/payment_gateway_adapter.py` (the abstract interface)
- `repositories/bill_repository.py` (the abstract interface)
- `services/payment_service.py` (the abstract interface)
