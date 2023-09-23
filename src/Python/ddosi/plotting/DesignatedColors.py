"""
Created on February 17, 2023
@author: Lance A. Endres
"""
import pandas                                                        as pd
from   PIL                                                           import ImageColor
import os


class DesignatedColors():
    # colors = pd.DataFrame(
    #     {
    #         "Acceleration X"         : ["dd8452"],
    #         "Acceleration Y"         : ["55a868"],
    #     },
    #     index=[0]
    # )

    colors = pd.DataFrame(
        {
            "Acceleration X"         : ["#dd8452"],
            "Acceleration Y"         : ["#55a868"],
            "Acceleration Z"         : ["#c44e52"],
            "Acceleration XY"        : ["#8172b3"],
            "Depth of Cut"           : ["#c44e52"],
            "Rotary Speed"           : ["#dd8452"],
            "Torque"                 : ["#55a868"],
            "Weight on Bit"          : ["#4c72b0"], #, bytes.fromhex("64b5cd")
        },
        index=[0]
    )

    # colors = pd.DataFrame(
    #     {
    #         "Weight on Bit"          : {bytes.fromhex("1f77b4"), bytes.fromhex("ff7f0e")},
    #         "Rotary Speed"           : {bytes.fromhex("2ca02c")},
    #     }
    # )

    def __init__(self):
        self.colors.to_csv("Colors.csv")

        #self.colors = pd.read_csv("Colors.csv")
        # print("\n\n\n\n")
        # print(self.colors)

        # self.colors.map(lambda x : ImageColor.getrgb(x))

        self.colors = pd.read_excel(os.path.join(os.path.dirname(__file__), "Colors.xlsx"), index_col=0)
        self._FillRows()

        # print(self.colors)
        # print(self.colors.info())
        # print("Cell type:", type(self.colors.iloc[0, 0]))

    def _FillRows(self):
        columnRange = range(1, len(self.colors.columns))

        for i in range(len(self.colors)):
            lastColor = 0

            for j in columnRange:
                if pd.isna(self.colors.iloc[i, j]):
                    self.colors.iloc[i, j] = self.colors.iloc[i, lastColor]
                else:
                    self.colors.iloc[i, j] =  ImageColor.getrgb(self.colors.iloc[i, j])
                    lastColor = j

        # Add a column to remember the active color.
        self.colors["Active"] = 0

    @classmethod
    def GetColor(cls, name):
        pass