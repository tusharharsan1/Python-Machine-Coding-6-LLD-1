from enum import Enum


class ItemType(Enum):
    """
    Indicates whether a menu item is a regular offering or a special for the day.
    DAILY_SPECIAL -> only available today
    REGULAR       -> always on the menu
    """
    DAILY_SPECIAL = "DAILY_SPECIAL"
    REGULAR = "REGULAR"
