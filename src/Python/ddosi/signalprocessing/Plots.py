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
    def CreatePowerSpectralDensityWithFrequencyIndicatorsPlot(cls, data, column, samplingFrequency, frequencys, frequencyLabels, fikwargs=[{}], titleSuffix=None, labelPeaks=True, **kwargs):
        """
        Creates a power spectral density plot with designated frequencies indicated as vertical lines.
        """
        figure, axes = cls.NewPowerSpectralDensityPlot(data, column, samplingFrequency, titleSuffix, labelPeaks=labelPeaks, **kwargs)

        for frequency, label, frequencyKwargs in zip(frequencys, frequencyLabels, fikwargs):
            # Apply designated colors, if the color exists.
            kwargsFrequency = DesignatedColors.ApplyKeyWordArgumentsToColors(frequencyKwargs, label)
            # Provide a default dashed line.  We don't want to override specified line styles though, so we check first.
            if not "linestyle" in kwargsFrequency:
                kwargsFrequency.update({"linestyle" : (0, (4, 6))})
            axes.axvline(frequency, **kwargsFrequency, label=label)

        legend = LegendHelper.CreateLegendAtFigureBottom(figure, axes, offset=0.15)
        LegendHelper.SetLegendLineWidths(legend, 4)

        plt.show()
        return figure


    @classmethod
    def CreatePowerSpectralDensityPlot(cls, data, column, samplingFrequency, titleSuffix=None, labelPeaks=True, **kwargs):
        """
        Creates a power spectral density plot and finalizes it.
        """
        figure, axes = cls.NewPowerSpectralDensityPlot(data, column, samplingFrequency, titleSuffix, labelPeaks=labelPeaks, **kwargs)
        legend = LegendHelper.CreateLegendAtFigureBottom(figure, axes, offset=0.15)
        LegendHelper.SetLegendLineWidths(legend, 4)

        plt.show()
        return figure


    @classmethod
    def NewPowerSpectralDensityPlot(cls, data, column, samplingFrequency, titleSuffix=None, labelPeaks=True, **kwargs):
        """
        Does the main work of making a power spectral density plot.
        """
        PlotHelper.Format()
        figure = plt.gcf()
        axes   = plt.gca()

        kwargs = DesignatedColors.ApplyKeyWordArgumentsToColors(kwargs, column)
        Pxx, frequencies = plt.psd(data[column], Fs=samplingFrequency, label=column, **kwargs)
        AxesHelper.Label(axes, "Power Spectral Density of Accelerations", xLabels="Frequency (Hz)", yLabels="Power Spectral Density (dB/Hz)", titleSuffix=titleSuffix)

        if labelPeaks:
            # The plotted line on the PSD is different than the returned values.  We need to scale the retuned values by the same
            # method as the plotted line was.
            # We then find the peaks.  The indices of the peaks are the first firsted value from find_peaks.
            plotPxx = 10*np.log10(Pxx)
            peaks   = find_peaks(plotPxx, distance=5)
            peaks   = peaks[0]

            # Now we annotate the plot.
            for peak in peaks:
                axes.annotate("{0:.0f}".format(frequencies[peak]), (frequencies[peak], plotPxx[peak]),
                    size=0.6*PlotHelper.GetScaledAnnotationSize(),                 # Font size.
                    fontweight="bold",                                             # Font weight.
                    xytext=(0, 3),                                                 # Move text up a few points so it doesn't touch the curve.
                    textcoords="offset points",                                    # Specifies that xytext is in points.
                    horizontalalignment="center",                                  # Center text horizontally.
                    verticalalignment="bottom"                                     # Justify to bottom of text.  We annotate above the curve.
                )

        return figure, axes


    @classmethod
    def CreateSpectrogramPlot(cls, data, column, samplingFrequency, maxFequency=None, titleSuffix=None, **kwargs):
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