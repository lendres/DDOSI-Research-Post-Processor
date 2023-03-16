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
    def CreateMovingAverageOfData(cls, data, columns, numberOfPoints):
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
        """
        newNames = []
        for column in columns:
            movingAverage    = data[column].rolling(numberOfPoints).mean()

            # The front of the series gets filled with NaN until "numberOfPoints" entry is reached (that many points are needed
            # to start the moving avaerage calculation).  Because, NaNs cause a lot of problems in calculations/plotting/et cetera,
            # the NaNs are replaced with the first valid value.
            movingAverage.fillna(movingAverage[numberOfPoints], inplace=True)

            columnName       = column + " " + str(numberOfPoints) + " pt Moving Average"
            data[columnName] = movingAverage
            newNames.append(columnName)
        return newNames


    @classmethod
    def CreateLowPlassFilteredData(cls, data, columns, cutOff, samplingFrequency, order=2):
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
        """
        newNames = []
        for column in columns:
            filteredData, b, a = ButterworthLowPassFilter(data[column], cutOff, samplingFrequency, order)
            columnName         = column + " " + str(cutOff) + " Hz Lowpass Filtered"
            data[columnName]   = filteredData
            newNames.append(columnName)
        return newNames