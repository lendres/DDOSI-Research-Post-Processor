"""
Created on February 17, 2023
@author: Lance A. Endres
"""
import pandas                                                        as pd
import os

from   lendres.path.Path                                             import Path
from   lendres.plotting.PlotHelper                                   import PlotHelper


class DesignatedColors():
    colors          = None
    usedColors      = None
    numberOfColors  = 0


    @classmethod
    def Initialize(cls, file:str=None):
        """
        Initializes the color map by reading it from a file.  Call this before attempting to call "GetColors".

        Parameters
        ----------
        file : str, optional
            Excel file that contains the color map.  If none is supplied, it is assumed a file named "Colors.xlsx" in the same directory as the source
            code file is the input.  If a file name (and no path) is supplied, it is assumed the file is in the same folder as the source code file.  The
            default is None.

        Returns
        -------
        None.
        """
        if file is None:
            file = os.path.join(Path.GetDirectory(__file__), "Colors.xlsx")

        if not Path.ContainsDirectory(file):
            file = os.path.join(Path.GetDirectory(__file__), file)

        # The first column are row labels and we indicate that by using "indoex_col=0".
        cls.colors         = pd.read_excel(file, index_col=0)
        cls.numberOfColors = len(cls.colors.columns)


    @classmethod
    def GetColorsAsKeyWordArguments(cls, names:str|list|tuple):
        return {"color" : cls.GetColors(names)}


    @classmethod
    def ApplyKeyWordArgumentsToColors(cls, kwargs, names:str|list|tuple):
        defaultKwargs = cls.GetColorsAsKeyWordArguments(names)
        defaultKwargs.update(kwargs)
        return defaultKwargs


    @classmethod
    def GetColors(cls, names:str|list|tuple):
        """
        Takes a list/tuple (or list of lists) of named values and converts them to a list of colors.

        If any of the names are not found in the color map, a default color will be supplied.  The default colors are generated fromthe PlotHelper
        color cyle.

        Color map lookups are done on a closest match basis.
            Example:
                If name="Category A Sub 1 SubSub I"
                And the look up map had categories:
                    "Category A"
                    "Category A Sub 1"
                The name would match "Category A Sub 1" because "Category A Sub 1" is the longest string that matches the start of name.

        Parameters
        ----------
        names : str|list|tuple
            A list/tuple of named values.  The lists/tuples can be nested.
            Examples:
                ["Category A", "Category B", "Category C"]
                ["Category A", ["Category B", "Category C"]]

        Returns
        -------
        colors : list
            A list of colors.  The list is a flat list (no nested lists).
        """
        if cls.colors is None:
            raise Exception("The DesignatedColors class has not been properly initialized.")

        # Add a column to remember the active color.
        cls.colors["Active"] = 0
        cls.usedColors       = []

        colors = []
        cls._GetNamedColors(colors, names)
        cls._FillRemainingColors(colors)

        if type(names) is str:
            return colors[0]
        else:
            return colors


    @classmethod
    def _GetNamedColors(cls, colors:list, item:str|list|tuple):

        match item:
            case str():
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