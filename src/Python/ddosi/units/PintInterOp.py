"""
Created on January 25, 2024
@author: Lance A. Endres
"""
import os

from   lendres.path.Path                                             import Path

from   ddosi.units.Units                                             import Units


class PintInterOp(Units):


    @classmethod
    def ConvertOutput(cls, data, xAxisColumn, yDataColumns):
        columns = ListTools.Flatten([xAxisColumn, yDataColumns])
        for column in columns:
                PandasInterOp.GetSeriesMagnitudes(data[independentColumnName])
    dependentData   = cls.GetSeriesMagnitudes(data[column])
        convertedData = [ data[column] for column in columns]
        print("\n\nColumns:", columns)
        yColumn = (yDataColumns[0])[0]
        print("Y column 0:", yColumn)
        convertedData[yColumn] = convertedData[yColumn].pint.to("kg")
        return convertedData



    @classmethod
    def GetSeriesMagnitudes(cls, series):
        """
        Determines if a series contains data that is a pint data type.  If it is, it extracts the magnitudes and
        returns those.  Otherwise the original data is returned.

        Parameters
        ----------
        series : pandas.Series
            A Pandas series.

        Returns
        -------
        pandas.Series or numpy.ndarray
            The original data or the extract magnitudes.
        """
        if cls._IsSeriesOfPintDType(series):
            return series.values.quantity.magnitude
        else:
            return series


    @classmethod
    def _IsSeriesOfPintDType(cls, series):
        """
        Determines if a pandas.Series contains data that is Pint (Units library) data type.

        Parameters
        ----------
        series : pandas.Series
            A Pandas Series.

        Returns
        -------
        bool
            True if the series contain Pint data.
        """
        return str(series.dtype).startswith("pint"):