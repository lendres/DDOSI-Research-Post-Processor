"""
Created on February 17, 2023
@author: Lance A. Endres
"""
import pandas                                    as pd
class DesignatedColors():


    colors = pd.DataFrame(
        {
            "WOB"                    : {bytes.fromhex("1f77b4"), bytes.fromhex("ff7f0e")}
            "Corrected WOB"          : ,
            "Rotary Speed"           : bytes.fromhex("2ca02c"),
        }
    )

    @classmethod
    def GetColor(cls, name):
        pass