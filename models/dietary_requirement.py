from enum import Enum


class DietaryRequirement(Enum):
    """
    Categorises a menu item based on dietary preference.
    VEG     -> vegetarian
    NON_VEG -> contains meat/fish/poultry
    VEGAN   -> no animal products at all
    """
    VEG = "VEG"
    NON_VEG = "NON_VEG"
    VEGAN = "VEGAN"
