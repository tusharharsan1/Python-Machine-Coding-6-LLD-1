class InvalidBillException(Exception):
    """
    Raised when a bill_id is provided that does not exist in the database.

    Example:
        raise InvalidBillException("Invalid bill id")
    """

    def __init__(self, message: str):
        super().__init__(message)
