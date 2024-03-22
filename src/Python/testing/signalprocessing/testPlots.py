"""
Created on February 17, 2023
@author: Lance A. Endres
"""
import numpy                                                         as np
import matplotlib.pyplot                                             as plt
from   matplotlib                                                    import mlab

from   lendres.plotting.PlotHelper                                   import PlotHelper
from   lendres.plotting.AnnotationHelper                             import AnnotationHelper

from   ddosi.signalprocessing.Plots                                  import Plots                                      as SignalProcessingPlots
from   ddosi.plotting.DesignatedColors                               import DesignatedColors
# from   ddosi.signalprocessing.SignalProcessing                       import SignalProcessing
from   testing.signalprocessing.TestDataSets                         import TestDataSets

import unittest


class testSignalProcessingPlots(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        DesignatedColors.Initialize()

        cls.annotationHelper = AnnotationHelper(formatString="{x:0.1f}")
        cls.annotationHelper.SetAdjustText(True, arrowstyle="-")

        cls.dataSets = TestDataSets.GetDataSets()


    def setUp(self):
        """
        Set up function that runs before each test.
        """
        pass


    # @unittest.skip
    def testPlotRealFft(self):
        numberOfAnnotations = [1, 2, 1, 2, 1]
        for i in range(len(self.dataSets)):
            dataSet = self.dataSets[i]
            SignalProcessingPlots.CreateRealFftPlot(dataSet, "y", dataSet.samplingFrequency, titleSuffix=dataSet.name, labelPeaks=True, numberOfAnnotations=numberOfAnnotations[i])

            if i == 4:
                SignalProcessingPlots.CreateRealFftPlot(dataSet, column="y", samplingFrequency=dataSet.samplingFrequency, limits=[2872, 2886], titleSuffix=dataSet.name, labelPeaks=self.annotationHelper)
                SignalProcessingPlots.CreateRealFftPlot(dataSet, column="y", samplingFrequency=dataSet.samplingFrequency, stem=False, limits=[2872, 2886], titleSuffix=dataSet.name, labelPeaks=self.annotationHelper)


    # @unittest.skip
    def testPsdDataSets(self):
        for i in range(len(self.dataSets)):
            dataSet = self.dataSets[i]
            # frequencies, psd = SignalProcessing.PowerSpectralDensity(dataSet["y"], dataSet.samplingFrequency)
            # TestDataSets.CreatePlot(frequencies, psd, dataSet.name)

            SignalProcessingPlots.CreatePowerSpectralDensityPlot(dataSet, column="y", samplingFrequency=dataSet.samplingFrequency, titleSuffix=dataSet.name)


    # @unittest.skip
    def testSpectrogramOnDataSets(self):
        maxFequencies = [None, None, None, 90, None]
        for i in [3, 4]:
            dataSet = self.dataSets[i]
            SignalProcessingPlots.CreateSpectrogramPlot(dataSet, column="y", samplingFrequency=dataSet.samplingFrequency, maxFequency=maxFequencies[i], titleSuffix=dataSet.name)


    # @unittest.skip
    def test3DSpectrogram(self):
        dataSet = self.dataSets[4]
        self.Plot3dSpectrogram(dataSet["y"], samplingFrequency=dataSet.samplingFrequency, title="3D Spectrogram")
        plt.show()


    # @classmethod
    def Plot3dSpectrogram(cls, y, samplingFrequency=44100, ax=None, title=None):
        PlotHelper.PushSettings(scale=0.5)
        PlotHelper.Format()

        figure, axes = plt.subplots(subplot_kw={"projection": "3d"})
        axes.set_box_aspect(aspect=None, zoom=0.85)

        spec, freqs, t = mlab.specgram(y, Fs=samplingFrequency)
        X, Y, Z = t[None, :], freqs[:, None],  20.0 * np.log10(spec)
        axes.plot_surface(X, Y, Z, cmap="viridis")

        axes.set_title(title, y=0.97, verticalalignment="top")
        axes.set_xlabel("Time (s)")
        axes.set_ylabel("Frequencies (Hz)")
        axes.set_zlabel("Amplitude (dB)")
        axes.set_zlim(-140, 0)

        PlotHelper.PopSettings()
        return X, Y, Z


if __name__ == "__main__":
    unittest.main()