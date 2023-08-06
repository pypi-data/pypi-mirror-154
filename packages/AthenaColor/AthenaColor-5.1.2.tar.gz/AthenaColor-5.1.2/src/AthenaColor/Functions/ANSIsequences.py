# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations

# Custom Library

# Custom Packages
from AthenaColor.InitClass import init

# ----------------------------------------------------------------------------------------------------------------------
# - All -
# ----------------------------------------------------------------------------------------------------------------------
__all__ = [
    "ColorSequence", "NestedColorSequence","NestedColorSequence_NoReset"
]

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def ColorSequence(control_code:int|str)->str:
    """
    Used for quick assembly of correct Ansi Escape functions
    Used the escape code defined in AthenaColor init
    """
    return f'{init.esc}[{control_code}m'

def NestedColorSequence(obj:tuple, color_code:str, reset_code:int|str, sep:str=" ") -> str:
    """
    Used by Nested Console StyleNest Makeup operations like ForeNest, BackNest, StyleNest.
    Function wraps every obj in the properly defined control- and reset codes.
    This is made to prevent style makeup bleed
    """

    # SHHH, don't touch this, this is speed 101
    text = ""
    for o in obj[:-1]:
        text += f"{color_code}{o}{sep}{reset_code}" # SEP moved to within the color - reset, as previously, it was color-reset anyway
    return text + f"{color_code}{obj[-1]}{reset_code}"

def NestedColorSequence_NoReset(obj:tuple, color_code:int|str, sep:str=" ") -> str:
    """
    Used by Nested Console StyleNest Makeup operations like ForeNest, BackNest, StyleNest.
    Function wraps every obj in the properly defined control- and reset codes.
    This is made to prevent style makeup bleed
    """

    # SHHH, don't touch this, this is speed 101
    text = ""
    for o in obj[:-1]:
        text += f"{color_code}{o}{sep}" # SEP moved to within the color - reset, as previously, it was color-reset anyway
    return text + f"{color_code}{obj[-1]}"