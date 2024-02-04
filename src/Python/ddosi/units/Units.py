"""
Created on January 25, 2024
@author: Lance A. Endres
"""
import pandas                                                        as pd
import os

from   lendres.io.ConsoleHelper                                      import ConsoleHelper
from   lendres.io.IO                                                 import IO
from   lendres.path.Path                                             import Path
from   lendres.datatypes.ListTools                                   import ListTools

from   pint                                                          import UnitRegistry
import pint_pandas


class Units():
    unitsTypes     = None
    UnitRegistry   = None


    @classmethod
    def Initialize(cls, system:str="SI", file:str="Units.xlsx", definitionsfile:str="default_en.txt"):
        """
        Initializes the units types by reading them from a file.  Call this before attempting to use units.

        Parameters
        ----------
        system : str, optional
            The output units system.
        file : str, optional
            Excel file that contains the color map.  If none is supplied, it is assumed a file named "Units.xlsx" in the same directory as the source
            code file is the input.  If a file name (and no path) is supplied, it is assumed the file is in the same folder as the source code file.  The
            default is None.
        definitionsfile : str, options
            The Pint definitions file.

        Returns
        -------
        None.
        """
        if not Path.ContainsDirectory(definitionsfile):
            definitionsfile = os.path.join(Path.GetDirectory(__file__), definitionsfile)

        cls.UnitRegistry = UnitRegistry(definitionsfile)

        # Pint pandas setup.
        pint_pandas.PintType.ureg = cls.UnitRegistry
        pint_pandas.PintType.ureg.default_format = "P~"
        pint_pandas.PintType.ureg.setup_matplotlib(True)

        if not Path.ContainsDirectory(file):
            file = os.path.join(Path.GetDirectory(__file__), file)

        # The first column are row labels and we indicate that by using "indoex_col=0".
        cls.unitsTypes = pd.read_excel(file, sheet_name=system, index_col=0)


    @classmethod
    def ConvertOutput(cls, data:pd.DataFrame, independentAxisColumn:str, dependentAxisColumns:list):
        """
        Converts the specified columns to the output units and returns the data and labels with units applied.

        Parameters
        ----------
        data : pandas.DataFrame
            DESCRIPTION.
        independentAxisColumn : str
            The column name of the independent data.
        dependentAxisColumns : list of str
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
        columns = ListTools.Flatten([independentAxisColumn, dependentAxisColumns])

        # Convert the data to the output value and units.
        convertedData = [cls.ConvertSeriesUnits(data[column]) for column in columns]

        independentAxisUnits = cls.GetUnitsSuffix(independentAxisColumn, convertedData[0])
        dependentAxisUnits   = cls.GetUnitsSuffix(dependentAxisColumns, convertedData[1:])

        convertedData = [cls.GetSeriesMagnitudes(series) for series in convertedData]
        convertedData = pd.DataFrame(convertedData).T
        convertedData = convertedData.set_axis(columns, axis=1, copy=False)

        return convertedData, independentAxisUnits, dependentAxisUnits


    @classmethod
    def ConvertSeriesUnits(cls, series:pd.Series) -> pd.Series:
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
        IO.consoleHelper.Print("\nSeries: "+series.name, ConsoleHelper.VERBOSEDEBUG)

        if not cls._IsSeriesOfPintDType(series):
            IO.consoleHelper.PrintWarning("The series cannot be converted.  It does not contain Pint data.  Series: "+series.name)
            return series
        elif not "unitstype" in series.attrs:
            IO.consoleHelper.PrintWarning("The series cannot be converted.  It does not contain the units type metadata.  Series: "+series.name)
            return series

        toUnits = cls.unitsTypes.loc[series.attrs["unitstype"], "Unit"]

        IO.consoleHelper.Print("Units: "+toUnits, ConsoleHelper.VERBOSEDEBUG)

        return series.pint.to(toUnits)


    @classmethod
    def GetUnitsSuffix(cls, labels:str|list, data:pd.DataFrame|pd.core.series.Series|list) -> str|list:
        """
        Gets the units associated with each label.

        Parameters
        ----------
        labels : string or array like of strings
            Label(s).  If axeses is an array, labels can be an array of the same length.
        data : pd.DataFrame, pd.core.series.Series, or list of pd.core.series.Series where each series contains a pint_pandas.pint_array.PintArray
            Data to extract the units from.

        Returns
        -------
        units : string or list of strings
            The units for each label.
        """
        # Convert a DataFrame to a list of Series.
        if isinstance(data, pd.DataFrame):
            data = [data[column] for column in data]

        if isinstance(labels, list):
            # For a list of entries.
            if not isinstance(data, list):
                raise Exception("The x labels are a list and the x data type is not compatible.")

            if not all([cls._IsSeriesOfPintDType(item) for item in data]):
                # raise Exception("The x data must be PintArray(s).")
                IO.consoleHelper.PrintWarning("The labels cannot be extracted from the series.")
                units = ["" for label, entry in zip(labels, data)]
            else:
                units = [str(entry.values.quantity.units) for label, entry in zip(labels, data)]
        else:
            # For a single entry.
            if not cls._IsSeriesOfPintDType(data):
                # raise Exception("The x data must be PintArray(s).")
                IO.consoleHelper.PrintWarning("The labels cannot be extracted from the series.")
                units = ""
            else:
                units = str(data.values.quantity.units)

        return units



    @classmethod
    def CombineLabelsAndUnits(cls, labels:str|list, units:str|list) -> str|list:
        """
        Combines the axis label with the units (if provided).
        Example:
            In: ["Label 1", "Label 2"], ["A", "B"]
            Out: ["Label 1 (A)", "Label 2 (B)"]

        Parameters
        ----------
        labels : str or array like of str
            Label(s).  If axeses is an array, labels can be an array of the same length.
        units :str or array like of str.
            Units.

        Returns
        -------
        labels : str or list of str
            The labels with the units appended.
        """
        if isinstance(labels, list):
            # For a list of entries.
            if not isinstance(units, list):
                raise Exception("The x labels are a list and the units type is not compatible.")

            labels = [label if entry=="" else label+" ("+entry+")" for label, entry in zip(labels, units)]
        else:
            # For a single entry.
            labels = labels if units=="" else labels + " (" + units + ")"

        return labels


    @classmethod
    def AddUnitsSuffixToLabel(cls, label:str, data:pd.core.series.Series) -> str:
        """
        Creates an axis label with the unit appended based on the label provided and the data units.
        Combines the two functions of "GetUnitsSuffix" and "CombineLabelsAndUnits".

        Parameters
        ----------
        label : str
            The axis label.
        data : pandas.Series
            A series that has units meta data and pint data type.

        Returns
        -------
        labelWithUnits : str
            The axis label with the units appended.
        """
        # To make this work for a DataFrame, we would also have to pass the column names as we cannot assume the column
        # names and axis labels are the same.
        units           = cls.GetUnitsSuffix(label, data)
        labelsWithUnits = cls.CombineLabelsAndUnits(label, units)
        return labelsWithUnits


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


    @classmethod
    def AddUnitsToDataFrame(cls, dataFrame:pd.DataFrame, units:list, unitsTypes:list) -> pd.DataFrame:
        """
        Converts a DataFrame to a DataFrame with Units.

        Parameters
        ----------
        dataFrame : pandas.DataFrame
            The DataFrame to convert.
        units : list
            A list of the units.  There must be one entry in the list for every column.  The units must be
            valid Pint units.
        unitsTypes : list
            A list of the units types.  There must be one entry in the list for every column.  The type mus be
            registered in the "Units.xlsx" file.

        Returns
        -------
        dataFrame : pandas.DataFrame
            The converted DataFrame.
        """
        dataFrame.columns = pd.MultiIndex.from_tuples(list(zip(dataFrame.columns, units)))
        dataFrame         = dataFrame.pint.quantify(level=-1)

        for column, unitType in zip(dataFrame, unitsTypes):
            dataFrame[column].attrs["unitstype"] = unitType

        return dataFrame


    @classmethod
    def ToCsv(cls, dataFrame:pd.DataFrame, path:str, **kwargs):
        """
        Write the data, along with the units information to a CSV file.

        Parameters
        ----------
        dataFrame : pd.DataFrame
            The DataFrame to write.
        path : str
            The path to write the file to.
        **kwargs : kwargs
            Key word arguments passed to "to_csv".

        Returns
        -------
        None.
        """
        # Extract the units and units types from the data structures.  Need to get the attributes before dequantifiying.
        # The dequantifying process seems to strip the attributes.
        typesForHeaderInsert = []

        for column in dataFrame:
            typesForHeaderInsert.append(dataFrame[column].attrs["unitstype"])

        # Specify the output format as "compact" which uses full words wihtout spaces and no special formatting.
        # Avoiding abbreviations prevents confusion such as "g" for "gravity" or "gram".
        # No spaces keeps it shorter for output.
        # Removing special formation prevents using superscripts and uses "**2" instead.  The superscripts don't play well in CSV files.
        storeFormat = cls.UnitRegistry.default_format
        cls.UnitRegistry.default_format = "C"
        dataFrameForWriting = dataFrame.pint.dequantify()
        cls.UnitRegistry.default_format = storeFormat

        # Add the units types a new headers.
        mainHeaders  = dataFrameForWriting.columns.get_level_values(0)
        unitsHeaders = dataFrameForWriting.columns.get_level_values(1)
        dataFrameForWriting.columns = pd.MultiIndex.from_tuples(list(zip(mainHeaders, unitsHeaders, typesForHeaderInsert)))

        # Write the file.
        dataFrameForWriting.to_csv(path, index=False, **kwargs)


    @classmethod
    def FromCsv(cls, path:str, **kwargs) -> pd.DataFrame:
        """
        Reads the data from a file and converts it to a DataFrame with associated units information.

        Parameters
        ----------
        path : str
            The path to read the data from.
        **kwargs : kwargs
            Key word arguments passed to "read_csv".

        Returns
        -------
        dataFrame : TYPE
            A DataFrame with associated units data types and attributes.
        """
        # Read the file.
        dataFrame = pd.read_csv(path, header=[0, 1, 2], **kwargs)

        # Extract the units, then remove them from the DataFrame.  They get in the way of the convertion to Pint.
        unitsTypes = dataFrame.columns.get_level_values(2)
        dataFrame  = dataFrame.droplevel(2, axis=1)

        # Convert the data types to units.
        dataFrame = dataFrame.pint.quantify(level=-1)

        # Add the units types after convertion to Pint.  Do it before, and they get lost/dropped.
        for column, unitsType in zip(dataFrame, unitsTypes):
            dataFrame[column].attrs["unitstype"] = unitsType

        return dataFrame