from abc import ABC, abstractmethod
from typing import Optional
from change_payment_gateway.models.bill import Bill


class BillRepository(ABC):
    """
    Defines the contract for how bills are stored and retrieved.

    The actual storage mechanism (in-memory dictionary, database, etc.)
    is decided by the concrete class that implements this interface.
    This separation means the service never needs to know HOW data is stored.

    TODO (for student):
    -------------------
    Create a concrete class called BillRepositoryImpl that implements this ABC.
    - Use a Python dictionary (e.g., self._bills = {}) as your in-memory database.
    - Use an integer counter (e.g., self._current_id = 1) to auto-assign IDs.

    Implement:
      1. save(bill)       -> assign an ID to the bill, store it in the dictionary,
                             and return the saved bill.
      2. find_by_id(id)   -> look up the dictionary for the given ID.
                             Return the Bill if found, or None if not found.
    """

    @abstractmethod
    def save(self, bill: Bill) -> Bill:
        """
        Saves a Bill object to the repository and returns it with its assigned ID.

        Args:
            bill : the Bill object to save

        Returns:
            The same Bill object, now with its id field populated.
        """
        pass

    @abstractmethod
    def find_by_id(self, bill_id: int) -> Optional[Bill]:
        """
        Looks up a bill by its unique ID.

        Args:
            bill_id : the ID of the bill to find

        Returns:
            The Bill object if it exists, or None if no bill with that ID is found.
        """
        pass
