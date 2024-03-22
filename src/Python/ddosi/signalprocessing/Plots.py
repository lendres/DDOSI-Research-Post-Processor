"""
Created on October 4, 2023
@author: Lance A. Endres
"""
import pandas                                                        as pd

import matplotlib.lines                                              as Lines
import matplotlib.pyplot                                             as plt

from   lendres.plotting.AxesHelper                                   import AxesHelper
from   lendres.plotting.PlotHelper                                   import PlotHelper
from   lendres.plotting.LegendHelper                                 import LegendHelper
from   lendres.plotting.AnnotationHelper                             import AnnotationHelper

from   ddosi.signalprocessing.SignalProcessing                       import SignalProcessing
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
    def NewPowerSpectralDensityPlot(cls, data:pd.DataFrame, column:str, samplingFrequency:int, titleSuffix:str=None, labelPeaks:AnnotationHelper|bool=True, numberOfAnnotations=6, findPeaksKwargs:dict={}, **kwargs):
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
        axes : matplotlib.axes.Axes
            The axes plotted on.
        """
        PlotHelper.Format()
        figure = plt.gcf()
        axes   = plt.gca()

        kwargs                 = DesignatedColors.ApplyKeyWordArgumentsToColors(kwargs, column)
        Pxx, frequencies, line = plt.psd(data[column], Fs=samplingFrequency, label=column, return_line=True, **kwargs)
        # To convert the returned values to the values plotted, use: plotPxx = 10*np.log10(Pxx)

        AxesHelper.Label(axes, "Power Spectral Density Plot", xLabels="Frequency (Hz)", yLabels="Power Spectral Density (dB/Hz)", titleSuffix=titleSuffix)

        cls._LabelPeaks(line, labelPeaks, sortBy="localheight", number=numberOfAnnotations, **findPeaksKwargs)

        return figure, axes


    @classmethod
    def CreateRealFftPlot(cls, data:pd.DataFrame, column:str, samplingFrequency:int, stem=True, limits:list=None, titleSuffix:str=None, labelPeaks:AnnotationHelper|bool=True, numberOfAnnotations=6, findPeaksKwargs:dict={}, **kwargs):
        PlotHelper.Format()
        figure = plt.figure()
        axes   = plt.gca()

        frequencies, result = SignalProcessing.RealFFT(data[column], samplingFrequency);

        if stem:
            # A stem plot doesn't return a standard Line2D object, so we will create one for the labeling.
            line      = Lines.Line2D(frequencies, result[0:-1])
            line.axes = axes
            colorArg  = DesignatedColors.GetColorsAsKeyWordArguments(column)
            markerline, stemlines, baseline = plt.stem(frequencies, result[0:-1], colorArg["color"], markerfmt=" ", basefmt="-b", label=column, **kwargs)
            plt.setp(markerline, "color", colorArg["color"])
            plt.setp(baseline, "color", colorArg["color"])
        else:
            kwargs    = DesignatedColors.ApplyKeyWordArgumentsToColors(kwargs, column)
            line      = plt.plot(frequencies, result[0:-1], label=column, **kwargs)

        AxesHelper.Label(axes, "FFT", xLabels="Frequency (Hz)", yLabels="Amplitude", titleSuffix=titleSuffix)

        if limits is not None:
            AxesHelper.SetXAxisLimits(axes, limits=limits)

        cls._LabelPeaks(line, labelPeaks, sortBy="globalheight", number=numberOfAnnotations, **findPeaksKwargs)

        legend = LegendHelper.CreateLegendAtFigureBottom(figure, axes, offset=0.15)
        LegendHelper.SetLegendLineWidths(legend, 4)

        plt.show()

        return figure


    @classmethod
    def _LabelPeaks(cls, line, labelPeaks, sortBy, **kwargs):
        match labelPeaks:
            case True:
                # Use default settings by creating a new AnnotationHelper.
                annotationHelper = AnnotationHelper(formatString="{x:0.0f}")
                annotationHelper.AddPeakAnnotations(line, sortBy=sortBy, **kwargs)
            case AnnotationHelper():
                labelPeaks.AddPeakAnnotations(line, sortBy=sortBy, **kwargs)
            case False:
                pass
            case _:
                raise Exception("Invalid 'labelPeaks' argument provided.")


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