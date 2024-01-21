"""
Created on October 4, 2023
@author: Lance A. Endres
"""
import pandas                                                        as pd
import matplotlib.pyplot                                             as plt

from   scipy.signal                                                  import find_peaks
import numpy                                                         as np

from   lendres.plotting.AxesHelper                                   import AxesHelper
from   lendres.plotting.PlotHelper                                   import PlotHelper
from   lendres.plotting.LegendHelper                                 import LegendHelper
from   lendres.plotting.LegendOptions                                import LegendOptions

from   ddosi.plotting.DesignatedColors                               import DesignatedColors


class Plots():
    @classmethod
    def CreatePowerSpectralDensityWithFrequencyIndicatorsPlot(cls, data, column, samplingFrequency, frequencys, frequencyLabels, titleSuffix, **kwargs):
        """
        Creates a power spectral density plot with designated frequencies indicated as vertical lines.
        """
        figure, axes = cls.NewPowerSpectralDensityPlot(data, column, samplingFrequency, titleSuffix, **kwargs)

        for frequency, label in zip(frequencys, frequencyLabels):
            kwargsFrequency = DesignatedColors.ApplyKeyWordArgumentsToColors(kwargs, label)
            axes.axvline(frequency, **kwargsFrequency, label=label)

        legend = LegendHelper.CreateLegendAtFigureBottom(figure, axes, offset=0.15)
        LegendHelper.SetLegendLineWidths(legend, 4)

        plt.show()
        return figure


    @classmethod
    def CreatePowerSpectralDensityPlot(cls, data, column, samplingFrequency, titleSuffix, **kwargs):
        """
        Creates a power spectral density plot and finalizes it.
        """
        figure, axes = cls.NewPowerSpectralDensityPlot(data, column, samplingFrequency, titleSuffix, **kwargs)
        legend = LegendHelper.CreateLegendAtFigureBottom(figure, axes, offset=0.15)
        LegendHelper.SetLegendLineWidths(legend, 4)

        plt.show()
        return figure


    @classmethod
    def NewPowerSpectralDensityPlot(cls, data, column, samplingFrequency, titleSuffix, **kwargs):
        """
        Does the main work of making a power spectral density plot.
        """
        PlotHelper.Format()
        figure = plt.gcf()
        axes   = plt.gca()

        kwargs = DesignatedColors.ApplyKeyWordArgumentsToColors(kwargs, column)
        Pxx, frequencies = plt.psd(data[column], Fs=samplingFrequency, label=column, **kwargs)
        AxesHelper.Label(axes, "Power Spectral Density of Accelerations", xLabels="Frequency", yLabels="Power Spectral Density (dB/Hz)", titleSuffix=titleSuffix)


        plotPxx = 10*np.log10(Pxx)
        # axes.plot(frequencies, plotPxx+4, "r--")
        # print("Plot Pxx", plotPxx)
        peaks = find_peaks(plotPxx, distance=5)
        peaks = peaks[0]
        print(peaks)
        for peak in peaks:
            # print("Peak:", peak)
            axes.annotate("{0:.0f}".format(frequencies[peak]), (frequencies[peak], plotPxx[peak]),
                size=0.6*PlotHelper.GetScaledAnnotationSize(),                 # Font size.
                fontweight="bold",
                xytext=(0, 3),                                                 # Move text up a few points.
                textcoords="offset points",                                    # Specifies that xytext is in points.
                horizontalalignment="center",                                  # Center text horizontally.
                verticalalignment="bottom"                                     # Justify to top of text.
)

        return figure, axes


    @classmethod
    def CreateSpectrogramPlot(cls, data, column, samplingFrequency, maxFequency=None, titleSuffix=None, **kwargs):
        PlotHelper.Format()
        dataWidthPercent = 0.965
        figure, (dataAxes, colorBarAxes) = plt.subplots(1, 2, width_ratios=(dataWidthPercent, 1-dataWidthPercent))
        # figure = plt.gcf()
        # axes   = plt.gca()

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