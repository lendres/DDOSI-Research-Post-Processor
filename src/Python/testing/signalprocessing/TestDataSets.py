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


class TestDataSets():

    @classmethod
    def GetDataSets(cls, plot:bool=True):
        dataSets = cls.GetDataSets123()
        dataSets.append(cls.GetDataSet4())
        dataSets.append(cls.GetDataSet5())

        return dataSets


    @classmethod
    def GetDataSets123(cls, plot:bool=True):
        numberOfPoints    = 1000
        timeLength        = 4
        samplingFrequency = int(numberOfPoints/timeLength)

        # Sine wave.
        signal      = FunctionGenerator.SineWavesAsDataFrame(magnitude=10, frequency=4, steps=numberOfPoints, timeLength=4)
        signal.name = "Set 1 - 4 Hz Sine Wave"
        signals     = [signal]

        # Two sine waves superimposed.
        signal      = FunctionGenerator.SineWavesAsDataFrame(magnitude=2, frequency=20, steps=numberOfPoints, timeLength=4)
        signal      = signals[0] + signal
        signal.name = "Set 2 - 4 Hz + 20 Hz Sine Wave"
        signals.append(signal)

        # Sine wave with radom noise added.
        signal = FunctionGenerator.NoisySineWaveAsDataFrame(magnitude=10, frequency=4, noiseScale=0.1, steps=numberOfPoints, timeLength=4)
        signal.name = "Set 3 - 4 Hz Noisy Sine Wave"
        signals.append(signal)

        for i in range(len(signals)):
            dataSet = signals[i]
            dataSet.samplingFrequency = samplingFrequency
            if plot:
                cls.CreatePlot(dataSet["x"], dataSet["y"], dataSet.name)

        return signals


    @classmethod
    def GetDataSet4(cls, plot:bool=True):
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

        name               = "Set 4 - "

        if plot:
            cls.CreatePlot(dataFrame["x"].iloc[:zoomedSamples], dataFrame["y original"].iloc[:zoomedSamples], name+str(frequency)+" Hz Sine Wave", limit=limit)
            cls.CreatePlot(dataFrame["x"].iloc[:zoomedSamples], dataFrame["noise"].iloc[:zoomedSamples], name+"Noise", limit=limit)

        x, y = FunctionGenerator.SineWave(magnitude=2, frequency=secondaryFrequency, startTime=startTime, timeLength=timeLength, steps=steps)

        dataFrame["y"] = dataFrame["y"] + y

        if plot:
            cls.CreatePlot(x[:zoomedSamples], y[:zoomedSamples], name+str(secondaryFrequency)+" Hz Sine Wave", limit=limit)
            # cls.CreatePlot(dataFrame["x"], dataFrame["y"], "Data Set 1 - Combined Signal", limit=limit)
            cls.CreatePlot(dataFrame["x"].iloc[:zoomedSamples], dataFrame["y"].iloc[:zoomedSamples], name+"Zoomed Combined Signal")

        dataFrame.name              = name + "60 Hz + 10 Hz Noisy Sine Wave"
        dataFrame.samplingFrequency = samplingFrequency

        return dataFrame


    @classmethod
    def GetDataSet5(cls, plot:bool=True):
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

        dataFrame.name              = "Set 5 - Decaying Cosine Wave with Noise"
        dataFrame.samplingFrequency = samplingFrequency


        # Plot of function.
        if plot:
            cls.CreatePlot(dataFrame["x"], dataFrame["y"], dataFrame.name)

        return dataFrame


    @classmethod
    def CreatePlot(cls, x, y, title, limit=None):
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