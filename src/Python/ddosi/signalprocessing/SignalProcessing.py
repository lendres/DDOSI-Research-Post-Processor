"""
Created on March 15, 2023
@author: Lance A. Endres
"""
import pandas                                                        as pd
import numpy                                                         as np

import scipy.fft


import matplotlib.mlab as mlab

class SignalProcessing():
    """
    A static class for applying signal processing algorithms.
    """

    @classmethod
    def MovingAverage(cls, signal:pd.Series|list|tuple|np.ndarray, numberOfPoints:int) -> pd.Series:
        """
        Creates moving averages for each column specified in "columns".  The moving averae is added to the DataFrame as a new
        column.  The new column name is the original column name with a suffix added that indicates the number of points used.

        Parameters
        ----------
        signal : array like of floats
            The column names in a list.
        numberOfPoints : int
            The number of points to use for the moving average.

        Returns
        -------
        movingAverage : pandas.Series
            Moving averages.
        """
        if not isinstance(signal, pd.core.series.Series):
            signal = pd.Series(signal)

        movingAverage = signal.rolling(numberOfPoints).mean()

        # The front of the series gets filled with NaN until "numberOfPoints" entry is reached (that many points are needed
        # to start the moving avaerage calculation).  Because, NaNs cause a lot of problems in calculations/plotting/et cetera,
        # the NaNs are replaced with the first valid value.
        movingAverage.fillna(movingAverage[numberOfPoints], inplace=True)

        return movingAverage


    @classmethod
    def RootMeanSquare(cls, signal:pd.Series|list|tuple|np.ndarray, numberOfPoints:int) -> pd.Series:
        """
        Creates a root mean square for each column specified in "columns".  The root mean square is added to the DataFrame as a new
        column.  The new column name is the original column name with a suffix added that indicates the number of points used.

        Parameters
        ----------
        signal : array like of floats
            The column names in a list.
        numberOfPoints : int
            The number of points to use for the moving average.

        Returns
        -------
        rootMeanSquare : pandas.Series
            Root mean squares.
        """
        if not isinstance(signal, pd.core.series.Series):
            signal = pd.Series(signal)

        rootMeanSquare  = signal.pow(2).rolling(numberOfPoints).mean().pow(0.5)

        # The front of the series gets filled with NaN until "numberOfPoints" entry is reached (that many points are needed
        # to start the moving avaerage calculation).  Because, NaNs cause a lot of problems in calculations/plotting/et cetera,
        # the NaNs are replaced with the first valid value.
        rootMeanSquare.fillna(rootMeanSquare[numberOfPoints], inplace=True)

        return rootMeanSquare


    @classmethod
    def PowerSpectralDensity(cls, signal:pd.Series|list|tuple|np.ndarray, samplingFrequency:int, **kwargs) -> tuple[np.ndarray, np.ndarray]:
        # This method will also work, but it will return the signal as positive and not the
        # from scipy import signal as SciPySignal
        # frequencies, psd = SciPySignal.welch(signal, axis=0)

        psd, frequencies = mlab.psd(signal, Fs=samplingFrequency)
        psd = 10*np.log10(psd)

        return frequencies, psd


    @classmethod
    def RealFFT(cls, signal:pd.Series|list|tuple|np.ndarray, samplingFrequency:int, **kwargs) -> tuple[np.ndarray, np.ndarray]:
        """
        Performs an FFT on real data and returns the frequencies and FFT values.

        Parameters
        ----------
        signal : pd.Series|list|tuple|np.array
            Signal to calculate the FFT for.
        samplingFrequency : int
            Samplling frequency/rate.
        kwargs : keyword arguments
            Keyword arguments passed to the FFT function.

        Returns
        -------
        frequencies : np.array
            The frequencies associated with each FFT value.
        fft : np.array
            The FFT values.
        """
        if isinstance(signal, pd.core.series.Series):
            signal = signal.values

        numberOfPoints = len(signal)

        frequencies = scipy.fft.rfftfreq(numberOfPoints, d=1.0/samplingFrequency)
        frequencies = frequencies[0:int(numberOfPoints/2)]
        fft         = np.abs(scipy.fft.rfft(signal, **kwargs))

        return frequencies, fft