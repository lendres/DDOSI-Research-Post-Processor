"""
Created on March 15, 2023
@author: Lance A. Endres
"""
from   ddosi.signalprocessing.ButterworthLowPass                     import ButterworthLowPassFilter

class SignalProcessing():
    """
    A static class for applying signal processing algorithms to data.
    """

    @classmethod
    def MovingAverage(cls, data, columns, numberOfPoints):
        """
        Creates moving averages for each column specified in "columns".  The moving averae is added to the DataFrame as a new
        column.  The new column name is the original column name with a suffix added that indicates the number of points used.

        Parameters
        ----------
        data : pandas.DataFrame
            Data in a pandas.DataFrame
        columns : array like of strings
            The column names in a list.
        numberOfPoints : int
            The number of points to use for the moving average.

        Returns
        -------
        newNames : list of strings
            A list of the new column names.
        suffix : str
            The suffix added to the column names.
        """
        newNames = []
        suffix   = str(numberOfPoints) + " pt Moving Average"

        for column in columns:
            movingAverage    = data[column].rolling(numberOfPoints).mean()

            # The front of the series gets filled with NaN until "numberOfPoints" entry is reached (that many points are needed
            # to start the moving avaerage calculation).  Because, NaNs cause a lot of problems in calculations/plotting/et cetera,
            # the NaNs are replaced with the first valid value.
            movingAverage.fillna(movingAverage[numberOfPoints], inplace=True)

            columnName       = column + " " + suffix
            data[columnName] = movingAverage
            newNames.append(columnName)
        return newNames, suffix


    @classmethod
    def RootMeanSquare(cls, data, columns, numberOfPoints):
        """
        Creates a root mean square for each column specified in "columns".  The root mean square is added to the DataFrame as a new
        column.  The new column name is the original column name with a suffix added that indicates the number of points used.

        Parameters
        ----------
        data : pandas.DataFrame
            Data in a pandas.DataFrame
        columns : array like of strings
            The column names in a list.
        numberOfPoints : int
            The number of points to use for the moving average.

        Returns
        -------
        newNames : list of strings
            A list of the new column names.
        suffix : str
            The suffix added to the column names.
        """
        newNames = []
        suffix   = str(numberOfPoints) + " pt RMS"

        for column in columns:
            rootMeanSquare  = data[column].pow(2).rolling(numberOfPoints).mean().pow(0.5)

            # The front of the series gets filled with NaN until "numberOfPoints" entry is reached (that many points are needed
            # to start the moving avaerage calculation).  Because, NaNs cause a lot of problems in calculations/plotting/et cetera,
            # the NaNs are replaced with the first valid value.
            rootMeanSquare.fillna(rootMeanSquare[numberOfPoints], inplace=True)

            columnName       = column + " " + suffix
            data[columnName] = rootMeanSquare
            newNames.append(columnName)
        return newNames, suffix


    @classmethod
    def LowPassFilter(cls, data, columns, cutOff, samplingFrequency, order=2):
        """
        Creeates low pass output for each column specified in "columns".  The low pass data is added to the DataFrame as a new
        column.  The new column name is the original column name with a suffix added that indicates the cut off frequency.

        Parameters
        ----------
        data : pandas.DataFrame
            Data in a pandas.DataFrame
        columns : array like of strings
            The column names in a list.
        cutOff : float
            The cut off frequency used in the filter.
        samplingFrequency : float
            The sampling frequency of the source data.
        order : int, optional
            Order of the filter used.. The default is 2.

        Returns
        -------
        newNames : list of strings
            A list of the new column names.
        suffix : str
            The suffix added to the column names.
        """
        newNames = []
        suffix   = str(cutOff) + " Hz Lowpass Filtered"

        for column in columns:
            filteredData, b, a = ButterworthLowPassFilter(data[column], cutOff, samplingFrequency, order)
            columnName         = column + " " + suffix
            data[columnName]   = filteredData
            newNames.append(columnName)
        return newNames, suffix