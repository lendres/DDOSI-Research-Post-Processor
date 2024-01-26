"""
Created on January 25, 2024
@author: Lance A. Endres
"""
import pandas                                                        as pd
import os

from   lendres.path.Path                                             import Path


class Units():
    unitTypes     = None


    @classmethod
    def Initialize(cls, system:str="SI", file:str="Units.xlsx"):
        """
        Initializes the units types by reading them from a file.  Call this before attempting to use units.

        Parameters
        ----------
        file : str, optional
            Excel file that contains the color map.  If none is supplied, it is assumed a file named "Units.xlsx" in the same directory as the source
            code file is the input.  If a file name (and no path) is supplied, it is assumed the file is in the same folder as the source code file.  The
            default is None.

        Returns
        -------
        None.
        """
        if not Path.ContainsDirectory(file):
            file = os.path.join(Path.GetDirectory(__file__), file)

        # The first column are row labels and we indicate that by using "indoex_col=0".
        cls.unitTypes = pd.read_excel(file, sheet_name=system, index_col=0)