from change_payment_gateway.models.base_model import BaseModel
from change_payment_gateway.models.dietary_requirement import DietaryRequirement
from change_payment_gateway.models.item_type import ItemType


class MenuItem(BaseModel):
    """
    Represents a single food or drink item available on the restaurant menu.
    Each item has a name, a price, a dietary category (VEG/NON_VEG/VEGAN),
    and a type (REGULAR or DAILY_SPECIAL).
    """

    def __init__(
        self,
        name: str,
        price: float,
        dietary_requirement: DietaryRequirement,
        item_type: ItemType,
        description: str,
    ):
        super().__init__()
        self.name = name
        self.price = price
        self.dietary_requirement = dietary_requirement
        self.item_type = item_type
        self.description = description
