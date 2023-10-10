"""
Created on October 4, 2023
@author: Lance A. Endres
"""
import pandas                                                        as pd
import matplotlib.pyplot                                             as plt

from   lendres.plotting.AxesHelper                                   import AxesHelper
from   lendres.plotting.PlotHelper                                   import PlotHelper
from   lendres.plotting.LegendHelper                                 import LegendHelper
from   lendres.plotting.LegendOptions                                import LegendOptions

from   ddosi.plotting.DesignatedColors                               import DesignatedColors


class Plots():

    @classmethod
    def CreatePowerSpectralDensityPlot(cls, data, column, samplingFrequency, titleSuffix, **kwargs):
        PlotHelper.Format()
        figure = plt.gcf()
        axes   = plt.gca()

        kwargs = DesignatedColors.ApplyKeyWordArgumentsToColors(kwargs, column)
        plt.psd(data[column], Fs=samplingFrequency, label=column, **kwargs)
        AxesHelper.Label(axes, "Power Spectral Density of Accelerations", xLabels="Time", yLabels="Power Spectral Density (dB/Hz)", titleSuffix=titleSuffix)

        legend = LegendHelper.CreateLegendAtFigureBottom(figure, axes, offset=0.15)
        LegendHelper.SetLegendLineWidths(legend, 4)

        plt.show()
        return figure


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