"""
Created on October 4, 2023
@author: Lance A. Endres
"""
import pandas                                                        as pd
import numpy                                                         as np

import matplotlib.pyplot                                             as plt

from   scipy.signal                                                  import find_peaks
from   scipy.fft                                                     import rfft
from   scipy.fft                                                     import rfftfreq

import heapq

from   lendres.plotting.AxesHelper                                   import AxesHelper
from   lendres.plotting.PlotHelper                                   import PlotHelper
from   lendres.plotting.LegendHelper                                 import LegendHelper
from   lendres.plotting.LegendOptions                                import LegendOptions
from   lendres.plotting.AnnotationHelper                             import AnnotationHelper

from   ddosi.plotting.DesignatedColors                               import DesignatedColors


class Plots():
    @classmethod
    def CreatePowerSpectralDensityWithFrequencyIndicatorsPlot(cls, data:pd.DataFrame, column:str, samplingFrequency:int, frequencys:list, frequencyLabels:list, fikwargs=[{}], titleSuffix:str=None, labelPeaks:bool=True, **kwargs):
        """
        Creates a power spectral density plot with designated frequencies indicated as vertical lines.

        Parameters
        ----------
        data : pandas.DataFrame
            Data in a pandas.DataFrame
        column : string
            The column name.
        samplingFrequency : int
            The sampling frequency.
        frequencys : list
            A list of frequencies to labels.
        frequencyLabels : list
            The names of the frequencies.
        fikwargs : list of dict, optional
            A list of keyword arguments passed to the line of each frequency that is plotted. The default is [{}].
        titleSuffix : str, optional
            DESCRIPTION. The default is None.
        labelPeaks : bool, optional
            Specifies if the local peaks should be labeled. The default is True.
        **kwargs : keyword arguments
            Keyword arguments passed to the plotting function.

        Returns
        -------
        figure : matplotlib.figure.Figure
            The newly created figure.
        """
        figure, axes = cls.NewPowerSpectralDensityPlot(data, column, samplingFrequency, titleSuffix, labelPeaks=labelPeaks, **kwargs)

        for frequency, label, frequencyKwargs in zip(frequencys, frequencyLabels, fikwargs):
            # Apply designated colors, if the color exists.
            kwargsFrequency = DesignatedColors.ApplyKeyWordArgumentsToColors(frequencyKwargs, label)

            # Provide a default dashed line.  We don't want to override specified line styles though, so we check first.
            if not "linestyle" in kwargsFrequency:
                kwargsFrequency.update({"linestyle" : (0, (4, 6))})

            # Plot the frequency indicator/marker as a vertical line.
            axes.axvline(frequency, **kwargsFrequency, label=label)

        legend = LegendHelper.CreateLegendAtFigureBottom(figure, axes, offset=0.15)
        LegendHelper.SetLegendLineWidths(legend, 4)

        plt.show()
        return figure


    @classmethod
    def CreatePowerSpectralDensityPlot(cls, data:pd.DataFrame, column:str, samplingFrequency:int, titleSuffix:str=None, labelPeaks:bool=True, **kwargs):
        """
        Creates a power spectral density plot and finalizes it.

        Parameters
        ----------
        data : pandas.DataFrame
            Data in a pandas.DataFrame
        column : string
            The column name.
        samplingFrequency : int
            The sampling frequency.
        titleSuffix : str or None, optional
            If supplied, the string is appended as a second line to the title.  Default is none.
        labelPeaks : bool, optional
            Specifies if the local peaks should be labeled. The default is True.
        **kwargs : keyword arguments
            Keyword arguments passed to the plotting function.

        Returns
        -------
        figure : matplotlib.figure.Figure
            The newly created figure.
        """
        figure, axes = cls.NewPowerSpectralDensityPlot(data, column, samplingFrequency, titleSuffix, labelPeaks=labelPeaks, **kwargs)
        legend = LegendHelper.CreateLegendAtFigureBottom(figure, axes, offset=0.15)
        LegendHelper.SetLegendLineWidths(legend, 4)

        plt.show()
        return figure


    @classmethod
    def NewPowerSpectralDensityPlot(cls, data:pd.DataFrame, column:str, samplingFrequency:int, titleSuffix:str=None, labelPeaks:AnnotationHelper|bool=True, **kwargs):
        """
        Does the main work of making a power spectral density plot.

        Parameters
        ----------
        data : pandas.DataFrame
            Data in a pandas.DataFrame
        column : string
            The column name.
        samplingFrequency : int
            The sampling frequency.
        titleSuffix : str or None, optional
            If supplied, the string is appended as a second line to the title.  Default is none.
        labelPeaks : bool, optional
            Specifies if the local peaks should be labeled. The default is True.
        **kwargs : keyword arguments
            Keyword arguments passed to the plotting function.

        Returns
        -------
        figure : matplotlib.figure.Figure
            The newly created figure.
        """
        PlotHelper.Format()
        figure = plt.gcf()
        axes   = plt.gca()

        kwargs                 = DesignatedColors.ApplyKeyWordArgumentsToColors(kwargs, column)
        Pxx, frequencies, line = plt.psd(data[column], Fs=samplingFrequency, label=column, return_line=True, **kwargs)

        AxesHelper.Label(axes, "Power Spectral Density Plot", xLabels="Frequency (Hz)", yLabels="Power Spectral Density (dB/Hz)", titleSuffix=titleSuffix)

        match labelPeaks:
            case True:
                # Use default settings by creating a new AnnotationHelper.
                annotationHelper = AnnotationHelper(formatString="{x:0.0f}")
                annotationHelper.AddPeakAnnotations(line)
            case AnnotationHelper():
                annotationHelper.AddPeakAnnotations(line)
            case False:
                pass
            case _:
                raise Exception("Invalid 'labelPeaks' argument provided.")

            # # The plotted line on the PSD is different than the returned values.  We need to scale the retuned values by the same
            # # method as the plotted line was.
            # plotPxx = 10*np.log10(Pxx)
            # cls._LabelPeaks(axes, frequencies, plotPxx)

        return figure, axes


    @classmethod
    def _LabelPeaks(cls, axes, xValues, yValues):
        # We find the peaks.
        # The distance argument is provided to group values that are extremely close together.  I.e., a shallow slow with small local peaks is not of interest.
        # The height argument is provided only to get the algorithm to return the relative peak prominences.  The relative heights/prominences are used as an 'importance' factor in sorting.
        # The indices of the peaks are the first firsted value from find_peaks.
        peakResults  = find_peaks(yValues, distance=4, prominence=0.1)

        # Extract the top values from the results.  The top values are defined as those with the largest local peak height.
        localHeights = (peakResults[1])["prominences"]
        peaks        = peakResults[0]
        largestPeaks = heapq.nlargest(8, zip(localHeights, peaks))
        largestPeaks = [peakCouple[1] for peakCouple in largestPeaks]

        # X locations.
        peakXValues = xValues[largestPeaks]

        # Y locations.
        peakYValues = yValues[largestPeaks]

        for xValue, yValue in zip(peakXValues, peakYValues):
            # Now we annotate the plot.
            axes.annotate(
                "{0:.0f}".format(xValue),                                      # Text to plot.
                (xValue,                                                       # X location.
                yValue),                                                       # Y location.
                size=0.6*PlotHelper.GetScaledAnnotationSize(),                 # Font size.
                fontweight="bold",                                             # Font weight.
                xytext=(0, 3),                                                 # Move text up a few points so it doesn't touch the curve.
                textcoords="offset points",                                    # Specifies that xytext is in points.
                horizontalalignment="center",                                  # Center text horizontally.
                verticalalignment="bottom"                                     # Justify to bottom of text.  We annotate above the curve.
            )


    @classmethod
    def CreateRealFftPlot(cls, data:pd.DataFrame, column:str, samplingFrequency:int, titleSuffix:str=None, labelPeaks:bool=True, **kwargs):
        PlotHelper.Format()
        figure = plt.figure()
        axes   = plt.gca()

        signal         = data[column]
        numberOfPoints = len(signal)

        frequencies = rfftfreq(numberOfPoints, d=1.0/samplingFrequency)
        frequencies = frequencies[0:int(numberOfPoints/2)]
        result      = np.abs(rfft(signal.values))

        plt.stem(frequencies, result[0:-1], markerfmt=" ", basefmt="-b")

        AxesHelper.Label(axes, "FFT", xLabels="Frequency (Hz)", yLabels="Amplitude", titleSuffix=titleSuffix)

        if labelPeaks:
            cls._LabelPeaks(axes, frequencies, result)

        plt.show()
        return figure


    @classmethod
    def CreateSpectrogramPlot(cls, data:pd.DataFrame, column:str, samplingFrequency:int, maxFequency:float=None, titleSuffix:str=None, **kwargs):
        """
        Creates a spectrogram (waterfall) plot.  It includes a color bar to indicate the levels.

        Parameters
        ----------
       data : pandas.DataFrame
           Data in a pandas.DataFrame
       column : string
           The column name.
       samplingFrequency : int
           The sampling frequency.
        maxFequency : float, optional
            If provided, it is the upper bounds on the x-axis of the plot. The default is None.
        titleSuffix : str or None, optional
            If supplied, the string is appended as a second line to the title.  Default is none.
        **kwargs : keyword arguments
            Keyword arguments passed to the plotting function.

        Returns
        -------
        figure : matplotlib.figure.Figure
            The newly created figure.
        """
        PlotHelper.Format()
        dataWidthPercent = 0.965
        figure, (dataAxes, colorBarAxes) = plt.subplots(1, 2, width_ratios=(dataWidthPercent, 1-dataWidthPercent))

        spectrum, frequencies, times, image = dataAxes.specgram(data[column], Fs=samplingFrequency, **kwargs)

        colorBar = figure.colorbar(image, colorBarAxes)
        colorBarAxes.yaxis.label.set_size(fontsize=PlotHelper.GetScaledAnnotationSize())
        colorBarAxes.tick_params(axis="y", labelsize=0.80*PlotHelper.GetScaledAnnotationSize())
        colorBar.set_label("Amplitude (dB)")
        colorBar.minorticks_on()

        AxesHelper.Label(dataAxes, "Spectrogram of Accelerations", xLabels="Time", yLabels="Frequency", titleSuffix=titleSuffix)

        if maxFequency is not None:
            AxesHelper.SetYAxisLimits(dataAxes, upperLimit=maxFequency)

        plt.show()
        return figure