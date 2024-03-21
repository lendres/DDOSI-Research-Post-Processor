"""
Created on February 17, 2023
@author: Lance A. Endres
"""

from   scipy.signal                                                  import freqz

import numpy                                                         as np
import pandas                                                        as pd
import matplotlib.pyplot                                             as plt
from   matplotlib                                                    import mlab

from   lendres.demonstration.FunctionGenerator                       import FunctionGenerator
from   lendres.plotting.PlotHelper                                   import PlotHelper
from   lendres.plotting.AnnotationHelper                             import AnnotationHelper

from   ddosi.signalprocessing.Plots                                  import Plots                                      as SignalProcessingPlots
from   ddosi.plotting.DesignatedColors                               import DesignatedColors

import unittest


class testSignalProcessingPlots(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        DesignatedColors.Initialize()

        cls.annotationHelper = AnnotationHelper(formatString="{x:0.1f}")
        cls.annotationHelper.SetAdjustText(True, arrowstyle="-")

        cls.dataSet1, cls.samplingFrequency1 = cls.CreateDataSet1()
        cls.dataSet2, cls.samplingFrequency2 = cls.CreateDataSet2()


    @classmethod
    def CreateDataSet1(cls):
        startTime          = 0
        timeLength         = 10
        samplingFrequency  = 1024
        frequency          = 60
        magnitude          = 10
        limit              = magnitude+1
        secondaryFrequency = 10
        steps              = timeLength*samplingFrequency


        dataFrame = FunctionGenerator.NoisySineWaveAsDataFrame(noiseScale=0.1, magnitude=magnitude, frequency=frequency, startTime=startTime, timeLength=timeLength, steps=steps)

        limit              = 11
        zoomedSamples      = 512

        cls.CreateSineWavePlot(dataFrame["x"].iloc[:zoomedSamples], dataFrame["y original"].iloc[:zoomedSamples], "Data Set 1 - "+str(frequency)+" Hz Sine Wave", limit=limit)
        cls.CreateSineWavePlot(dataFrame["x"].iloc[:zoomedSamples], dataFrame["noise"].iloc[:zoomedSamples], "Data Set 1 - Noise", limit=limit)

        x, y = FunctionGenerator.SineWave(magnitude=2, frequency=secondaryFrequency, startTime=startTime, timeLength=timeLength, steps=steps)

        dataFrame["y"] = dataFrame["y"] + y

        cls.CreateSineWavePlot(x[:zoomedSamples], y[:zoomedSamples], "Data Set 1 - "+str(secondaryFrequency)+" Hz Sine Wave", limit=limit)
        # cls.CreateSineWavePlot(dataFrame["x"], dataFrame["y"], "Data Set 1 - Combined Signal", limit=limit)
        cls.CreateSineWavePlot(dataFrame["x"].iloc[:zoomedSamples], dataFrame["y"].iloc[:zoomedSamples], "Data Set 1 - Zoomed Combined Signal")

        return dataFrame, samplingFrequency


    @classmethod
    def CreateDataSet2(cls):
        """
        Example from:
            https://analyticsindiamag.com/hands-on-tutorial-on-visualizing-spectrograms-in-python/
        """
        # NFFT = 1024
        samplingFrequency   = 10e3
        numberOfPoints      = 1e5

        time                =  np.arange(numberOfPoints) / float(samplingFrequency)

        # The low frequency signal with a period of 4 seconds (prevents having a dominate signal at 0 Hz).
        lowFrequencySignal  = 500*np.cos(2*np.pi*0.25*time)

        amplitude           =  2 * np.sqrt(2)
        carrier             =  amplitude * np.sin(2*np.pi*3e3*time + lowFrequencySignal)
        carrier             =  amplitude * carrier

        np.random.seed(0)
        noisePower          =  0.01 * samplingFrequency / 2
        noise               =  np.random.normal(scale=np.sqrt(noisePower), size=time.shape)
        noise               *= np.exp(-time/5)

        y                   =  carrier + noise

        dataFrame           = pd.DataFrame({"x" : time, "y" : y})

        # Plot of function.
        cls.CreateSineWavePlot(dataFrame["x"], dataFrame["y"], "Data Set 2")

        return dataFrame, samplingFrequency


    def setUp(self):
        """
        Set up function that runs before each test.
        """
        pass


    # @unittest.skip
    def testPlotRealFft(self):
        numberOfPoints    = 1000
        timeLength        = 4
        samplingFrequency = int(numberOfPoints/timeLength)

        # Sine wave.
        signal = FunctionGenerator.SineWavesAsDataFrame(magnitude=10, frequency=4, steps=numberOfPoints, timeLength=4)
        signals = [signal]

        # Two sine waves superimposed.
        signal = FunctionGenerator.SineWavesAsDataFrame(magnitude=2, frequency=20, steps=numberOfPoints, timeLength=4)
        signals.append(signals[0] + signal)

        # Sine wave with radom noise added.
        signal = FunctionGenerator.NoisySineWaveAsDataFrame(magnitude=10, frequency=4, noiseScale=0.1, steps=numberOfPoints, timeLength=4)
        signals.append(signal)

        for i in range(len(signals)):
            self.CreateSineWavePlot(signals[i].loc[:, "x"], signals[i].loc[:, "y"], "Test Real FFT "+str(i+1))
            SignalProcessingPlots.CreateRealFftPlot(signals[i], "y", samplingFrequency, labelPeaks=True)


    @unittest.skip
    def testRealFftOnDataSets(self):
        # Data set 1.
        SignalProcessingPlots.CreateRealFftPlot(self.dataSet1, column="y", samplingFrequency=self.samplingFrequency1, titleSuffix="Data Set 1")

        # Data set 2.
        SignalProcessingPlots.CreateRealFftPlot(self.dataSet2, column="y", samplingFrequency=self.samplingFrequency2, limits=[2872, 2886], titleSuffix="Data Set 2", labelPeaks=self.annotationHelper)
        SignalProcessingPlots.CreateRealFftPlot(self.dataSet2, column="y", samplingFrequency=self.samplingFrequency2, stem=False, limits=[2872, 2886], titleSuffix="Data Set 2", labelPeaks=self.annotationHelper)

        SignalProcessingPlots.CreateRealFftPlot(self.dataSet2, column="y", samplingFrequency=self.samplingFrequency2, titleSuffix="Data Set 2", labelPeaks=True, numberOfAnnotations=1)


    @unittest.skip
    def testPsdDataSets(self):
        # Data set 1.
        SignalProcessingPlots.CreatePowerSpectralDensityPlot(self.dataSet1, column="y", samplingFrequency=self.samplingFrequency1, titleSuffix="Data Set 1")

        # Data set 2.
        SignalProcessingPlots.CreatePowerSpectralDensityPlot(self.dataSet2, column="y", samplingFrequency=self.samplingFrequency2, titleSuffix="Data Set 2")


    @unittest.skip
    def testSpectrogramOnDataSets(self):
        # Data set 1.
        SignalProcessingPlots.CreateSpectrogramPlot(self.dataSet1, column="y", samplingFrequency=self.samplingFrequency1, maxFequency=90, titleSuffix="Data Set 1")

        # Data set 2.
        SignalProcessingPlots.CreateSpectrogramPlot(self.dataSet2, column="y", samplingFrequency=self.samplingFrequency2, titleSuffix="Data Set 2")


    @unittest.skip
    def test3DSpectrogram(self):
        # Data set 2.
        self.Plot3dSpectrogram(self.dataSet2["y"], samplingFrequency=self.samplingFrequency2, title="3D Spectrogram")
        plt.show()


    @classmethod
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


    @classmethod
    def CreateSineWavePlot(cls, x, y, title, limit=None):
        """
        An example plot that is a simple sine wave.

        Parameters
        ----------
        x : array like
            The sine wave x values.
        y : array like
            The sine wave y values.
        title : string
            Title to use for the plot.

        Returns
        -------
        None.
        """
        PlotHelper.Format()

        axes = plt.gca()

        axes.plot(x, y, label="Sine Wave")
        axes.set(title=title, xlabel="Time", ylabel="Signal")

        if limit is not None:
            axes.set_ylim(-limit, limit)

        plt.show()


if __name__ == "__main__":
    unittest.main()