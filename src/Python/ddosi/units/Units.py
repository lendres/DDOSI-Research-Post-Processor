"""
Created on January 25, 2024
@author: Lance A. Endres
"""
import pandas                                                        as pd
import os

from   lendres.path.Path                                             import Path
from   lendres.datatypes.ListTools                                   import ListTools

import pint_pandas


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


    @classmethod
    def ConvertOutput(cls, data:pd.DataFrame, independentAxisColumn:str, dependentAxisColumn:list):
        """
        Converts the specified columns to the output units and returns the data and labels with units applied.

        Parameters
        ----------
        data : pandas.DataFrame
            DESCRIPTION.
        independentAxisColumn : str
            The column name of the independent data.
        dependentAxisColumn : list of str
            The column names for the dependent data.

        Returns
        -------
        convertedData : pandas.DataFrame
            The converted data.
        independentAxisUnits : str
            The dependent axis output units.
        dependentAxisUnits : list
            The dependent axis output units.
        """
        # Flatten the columns into a single list to make it easier to use.
        columns       = ListTools.Flatten([independentAxisColumn, dependentAxisColumn])

        # Convert the data to the output value and units.
        convertedData = [cls.ConvertSeries(data[column]) for column in columns]

        independentAxisUnits = cls.GetUnitsSuffix(independentAxisColumn, convertedData[0])
        dependentAxisUnits   = cls.GetUnitsSuffix(ListTools.Flatten(dependentAxisColumn), convertedData[1:])

        convertedData = [series.values.quantity.magnitude for series in convertedData]
        convertedData = pd.DataFrame(convertedData).T
        convertedData = convertedData.set_axis(columns, axis=1, copy=False)

        return convertedData, independentAxisUnits, dependentAxisUnits


    @classmethod
    def ConvertSeries(cls, series:pd.Series) -> pd.Series:
        """
        Converts a pandas.Series to the output units.

        Parameters
        ----------
        series : pandas.Series
            DESCRIPTION.

        Returns
        -------
        pandas.Series
            The values converted to the output units.
        """
        toUnits = cls.unitTypes.loc[series.attrs["unitstype"], "Unit"]
        # print("\nSeries:", series.name)
        # print("Units:", toUnits)
        return series.pint.to(toUnits)


    @classmethod
    def GetUnitsSuffix(cls, labels:str|list, data:pd.DataFrame|pd.core.series.Series|list):
        """
        Add title, x-axis label, and y-axis label.  Allows for multiple axes to be labeled at once.
        Extracts the units from PintArrays.

        Parameters
        ----------
        labels : string or array like of strings
            Label(s).  If axeses is an array, labels can be an array of the same length.
        data : pd.DataFrame, pd.core.series.Series, or list of pd.core.series.Series where each series contains a pint_pandas.pint_array.PintArray
            Data to extract the units from.

        Returns
        -------
        labels : string or list of strings
            The labels with the units appended.
        """
        # Convert a DataFrame to a list of Series.
        if isinstance(data, pd.DataFrame):
            data = [data[column] for column in data]

        if isinstance(labels, list):
            # For a list of entries.
            if not isinstance(data, list):
                raise Exception("The x labels are a list and the x data type is not compatible.")

            if not all([isinstance(item.values, pint_pandas.pint_array.PintArray) for item in data]):
                raise Exception("The x data must be PintArray(s).")

            labels = [str(entry.values.quantity.units) for label, entry in zip(labels, data)]
        else:
            # For a single entry.
            if not isinstance(data.values, pint_pandas.pint_array.PintArray):
                raise Exception("The x data must be PintArray(s).")

            labels = str(data.values.quantity.units)

        return labels



    @classmethod
    def CombineLabelsAndUnits(cls, labels:str|list, units:str|list):
        """
        Add title, x-axis label, and y-axis label.  Allows for multiple axes to be labeled at once.
        Extracts the units from PintArrays.

        Parameters
        ----------
        labels : str or array like of str
            Label(s).  If axeses is an array, labels can be an array of the same length.
        units :str or array like of str.
            Units.

        Returns
        -------
        labels : string or list of strings
            The labels with the units appended.
        """
        if isinstance(labels, list):
            # For a list of entries.
            if not isinstance(units, list):
                raise Exception("The x labels are a list and the units type is not compatible.")

            labels = [label+" ("+entry+")" for label, entry in zip(labels, units)]
        else:
            # For a single entry.
            labels = labels + " (" + units + ")"

        return labels



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
    def CopyMetaData(cls, toData:pd.Series|pd.DataFrame, fromData:pd.Series|pd.DataFrame):
        """
        Copies the "attrs" metadata from one Series or DataFrame to another.  The metadata is supposed to be carried with each Series
        or DataFrame, however, it currently has bugs and some functions drop the data.  Therefore, we need to manually copy it in
        some cases.

        Parameters
        ----------
        toData : pd.Series|pd.DataFrame
            Data to copy the attrs to.
        fromData : pd.Series|pd.DataFrame
            Data to copy the attrs from.

        Returns
        -------
        None.
        """
        match toData:
            case pd.Series():
                toData.attrs = fromData.attrs

            case pd.DataFrame():
                for column in toData:
                    toData[column].attrs = fromData[column].attrs


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
        return isinstance(series.values, pint_pandas.pint_array.PintArray)