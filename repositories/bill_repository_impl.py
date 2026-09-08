from typing import Optional
from change_payment_gateway.repositories.bill_repository import BillRepository
from change_payment_gateway.models.bill import Bill


class BillRepositoryImpl(BillRepository):
    """
    The in-memory implementation of BillRepository.

    We store all bills in a Python dictionary where:
      key   = the bill's ID (an integer)
      value = the Bill object itself

    We also keep a counter (_current_id) that starts at 1 and increases by 1
    every time a new bill is saved. This gives each bill a unique ID automatically.
    """

    def __init__(self):
        # Our in-memory "database" — maps bill ID → Bill object
        self._bills: dict = {}
        # Auto-increment counter for assigning IDs
        self._current_id: int = 1

    def save(self, bill: Bill) -> Bill:
        # Assign the next available ID to this bill
        bill.id = self._current_id
        # Store it in the dictionary
        self._bills[bill.id] = bill
        # Increment the counter so the next bill gets a different ID
        self._current_id += 1
        return bill

    def find_by_id(self, bill_id: int) -> Optional[Bill]:
        # dict.get() returns None automatically if the key doesn't exist
        # This is cleaner than writing: if bill_id in self._bills: return self._bills[bill_id]
        return self._bills.get(bill_id)
