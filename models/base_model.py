class BaseModel:
    """
    The parent class for all models in the system.
    Every model (Bill, User, etc.) will automatically get an 'id' field
    by inheriting from this class.
    """

    def __init__(self):
        self.id: int = 0
