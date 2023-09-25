"""
Created on February 17, 2023
@author: Lance A. Endres
"""
import pandas                                                        as pd
from   PIL                                                           import ImageColor
import os

from   lendres.path.File                                             import File
from   lendres.plotting.PlotHelper                                   import PlotHelper


class DesignatedColors():
    colors          = None
    usedColors      = None
    numberOfColors = 0


    @classmethod
    def Initialize(cls, file:str=None):
        if file is None:
            file = os.path.join(File.GetDirectory(__file__), "Colors.xlsx")

        if not File.ContainsDirectory(file):
            file = os.path.join(File.GetDirectory(__file__), file)

        cls.colors         = pd.read_excel(file, index_col=0)
        cls.numberOfColors = len(cls.colors.columns)
        # cls._FillRows()


    @classmethod
    def _FillRows(cls):
        columnRange = range(1, len(cls.colors.columns))

        for i in range(len(cls.colors)):
            lastColor = 0

            for j in columnRange:
                if pd.isna(cls.colors.iloc[i, j]):
                    cls.colors.iloc[i, j] = cls.colors.iloc[i, lastColor]
                else:
                    cls.colors.iloc[i, j] =  cls.colors.iloc[i, j]
                    lastColor = j


    @classmethod
    def GetColors(cls, names:list|tuple):
        # Add a column to remember the active color.
        cls.colors["Active"] = 0
        cls.usedColors       = []

        colors = []
        cls._GetNamedColors(colors, names)
        cls._FillRemainingColors(colors)
        return colors


    @classmethod
    def _GetNamedColors(cls, colors:list, item:str|list|tuple):

        match item:
            case str():
                # matches = []
                categories = cls.colors.index.values
                matches    = [category for category in categories if item.startswith(category)]
                if len(matches) > 0:
                    # Find the best match of the matches and return the color for that category.
                    category = max(matches, key=len)
                    colors.append(cls._GetCategoryColor(category))
                else:
                    colors.append("")

            case list() | tuple():
                for entry in item:
                    cls._GetNamedColors(colors, entry)

            case _:
                raise Exception("Unknown object type in input colors.")


    @classmethod
    def _GetCategoryColor(cls, category):
        column = cls.colors.loc[category, "Active"]

        if column == cls.numberOfColors or pd.isna(cls.colors.loc[category, column]):
            return ""
        else:
            cls.colors.loc[category, "Active"] = column + 1
            color                             = cls.colors.loc[category, column]
            cls.usedColors.append(color)
            return color


    @classmethod
    def _FillRemainingColors(cls, colors):
        for i in range(len(colors)):
            if colors[i] == "":
                colors[i] = cls._GetNextColor()


    @classmethod
    def _GetNextColor(cls):
        color = PlotHelper.NextColorAsHex()
        while color in cls.usedColors:
            color = PlotHelper.NextColorAsHex()
            pass
        return color