"""
Created on Februar 13, 2023
@author: Lance A. Endres
"""
from   enum                                      import IntEnum
from   enum                                      import auto

class NoiseVarianceEstimateMethod(IntEnum):
    # Point estimate.
    Point           = 0,

    # Smoothed estimate.
    Smoothed        = auto()

    # The number of types/items in the enumeration.
    Length          = auto()