"""
Created on February 17, 2023
@author: Lance A. Endres
"""

from   scipy.signal                                                  import freqz

import numpy                                                         as np
import pandas                                                        as pd
import matplotlib.pyplot                                             as plt

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


    def testSpectrogram(self):
        startTime          = 0
        timeLength         = 10
        samplingFrequency  = 1024
        frequency          = 60
        secondaryFrequency = 10
        steps              = timeLength*samplingFrequency

        dataFrame = FunctionGenerator.NoisySineWaveAsDataFrame(noiseScale=0.1, magnitude=10, frequency=frequency, startTime=startTime, timeLength=timeLength, steps=steps)
        x, y      = FunctionGenerator.SineWave(magnitude=2, frequency=secondaryFrequency, startTime=startTime, timeLength=timeLength, steps=steps)

        dataFrame["y"] = dataFrame["y"] + y

        self.CreateSineWavePlot(dataFrame["x"], dataFrame["y"], "Method 1")
        self.CreateSineWavePlot(dataFrame["x"].iloc[:256], dataFrame["y"].iloc[:256], "Method 1 Zoomed")
        SignalProcessingPlots.CreateSpectrogramPlot(dataFrame, column="y", samplingFrequency=samplingFrequency, maxFequency=90, titleSuffix="Method 1")


    def testSpectrogram2(self):
        """
        Example from:
            https://analyticsindiamag.com/hands-on-tutorial-on-visualizing-spectrograms-in-python/
        """
        samplingFrequency = 10e3
        N = 1e5
        # NFFT = 1024
        amplitude = 2 * np.sqrt(2)
        noisePower = 0.01 * samplingFrequency / 2
        time = np.arange(N) / float(samplingFrequency)
        mod = 500*np.cos(2*np.pi*0.25*time)
        carrier = amplitude * np.sin(2*np.pi*3e3*time + mod)
        noise = np.random.normal(scale=np.sqrt(noisePower), size=time.shape)
        noise *= np.exp(-time/5)
        y = carrier + noise

        dataFrame = pd.DataFrame({"x" : time, "y" : y})

        self.CreateSineWavePlot(dataFrame["x"], dataFrame["y"], "Method 2")
        SignalProcessingPlots.CreateSpectrogramPlot(dataFrame, column="y", samplingFrequency=samplingFrequency, titleSuffix="Method 2")


    @classmethod
    def CreateSineWavePlot(cls, x, y, title):
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

        plt.show()


if __name__ == "__main__":
    unittest.main()