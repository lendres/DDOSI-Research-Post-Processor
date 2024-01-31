"""
Created on February 17, 2023
@author: Lance A. Endres
"""
import numpy                                                         as np
import pandas                                                        as pd
import matplotlib.pyplot                                             as plt
from   matplotlib                                                    import mlab

from   lendres.demonstration.FunctionGenerator                       import FunctionGenerator
from   lendres.plotting.PlotHelper                                   import PlotHelper
from   ddosi.signalprocessing.Plots                                  import Plots                                      as SignalProcessingPlots

import unittest


class testSignalProcessingPlots(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Solution provided in paper.
        # Columns that are in the input file.  The first two are input to the function, the last three are the known solution.
        pass


    def setUp(self):
        """
        Set up function that runs before each test.
        """
        pass


    # @unittest.skip
    def testSpectrogram(self):
        startTime          = 0
        timeLength         = 10
        samplingFrequency  = 1024
        frequency          = 60
        magnitude          = 10
        limit              = magnitude+1
        secondaryFrequency = 10
        steps              = timeLength*samplingFrequency
        zoomedSamples      = 512

        dataFrame = FunctionGenerator.NoisySineWaveAsDataFrame(noiseScale=0.1, magnitude=magnitude, frequency=frequency, startTime=startTime, timeLength=timeLength, steps=steps)

        self.CreateSineWavePlot(dataFrame["x"].iloc[:zoomedSamples], dataFrame["y original"].iloc[:zoomedSamples], "Method 1 - "+str(frequency)+" Hz Sine Wave", limit=limit)
        self.CreateSineWavePlot(dataFrame["x"].iloc[:zoomedSamples], dataFrame["noise"].iloc[:zoomedSamples], "Method 1 - Noise", limit=limit)

        x, y      = FunctionGenerator.SineWave(magnitude=2, frequency=secondaryFrequency, startTime=startTime, timeLength=timeLength, steps=steps)

        dataFrame["y"] = dataFrame["y"] + y

        self.CreateSineWavePlot(x[:zoomedSamples], y[:zoomedSamples], "Method 1 - "+str(secondaryFrequency)+" Hz Sine Wave", limit=limit)
        # self.CreateSineWavePlot(dataFrame["x"], dataFrame["y"], "Method 1 - Combined Signal", limit=limit)
        self.CreateSineWavePlot(dataFrame["x"].iloc[:zoomedSamples], dataFrame["y"].iloc[:zoomedSamples], "Method 1 - Zoomed Combined Signal")
        SignalProcessingPlots.CreateSpectrogramPlot(dataFrame, column="y", samplingFrequency=samplingFrequency, maxFequency=90, titleSuffix="Method 1")


    def testSpectrogram2(self):
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

        noisePower          =  0.01 * samplingFrequency / 2
        noise               =  np.random.normal(scale=np.sqrt(noisePower), size=time.shape)
        noise               *= np.exp(-time/5)

        y                   =  carrier + noise

        dataFrame = pd.DataFrame({"x" : time, "y" : y})

        self.CreateSineWavePlot(dataFrame["x"], dataFrame["y"], "Method 2")
        SignalProcessingPlots.CreateSpectrogramPlot(dataFrame, column="y", samplingFrequency=samplingFrequency, titleSuffix="Method 2")


        # New.
        self.Plot3dSpectrogram(y, samplingFrequency=samplingFrequency, title="3D Spectrogram")
        plt.show()



    def Plot3dSpectrogram(self, y, samplingFrequency=44100, ax=None, title=None):
        PlotHelper.PushSettings(scale=0.5)
        PlotHelper.Format()

        figure, ax = plt.subplots(subplot_kw={"projection": "3d"})
        ax.set_box_aspect(aspect=None, zoom=0.85)

        spec, freqs, t = mlab.specgram(y, Fs=samplingFrequency)
        X, Y, Z = t[None, :], freqs[:, None],  20.0 * np.log10(spec)
        ax.plot_surface(X, Y, Z, cmap="viridis")

        ax.set_title(title, y=0.97, verticalalignment="top")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Frequencies (Hz)")
        ax.set_zlabel("Amplitude (dB)")
        ax.set_zlim(-140, 0)

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