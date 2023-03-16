"""
Created on February 14, 2023
@author: Lance A. Endres
"""
import numpy                                     as np
import pandas                                    as pd
import matplotlib.pyplot                         as plt

from itertools                                   import chain

from   ddosi.signalprocessing.NoiseVarianceEstimateMethod                      import NoiseVarianceEstimateMethod

from   SegmentSignalPy                           import Segment                as SegmentC
from   SegmentSignalPy                           import SegmentationResults
from   SegmentSignalPy                           import FindSignificantZones

from   lendres.plotting.PlotHelper               import PlotHelper

class SegmentSignal():
    results                     = None
    xData                       = None

    def __init__(self, xData=None):
        """
        Contructor.

        Parameters
        ----------
        dataFrame: Pandas DataFrame
        xData : array like or string
            The x-axis data.  Not required to segment, but is required for a lot of plotting and post processing.
            If "dataFrame" is provided, "xData" can be a string that is the column name of the x-axis data in the
            DataFrame.

        Returns
        -------
        None.
        """
        self.xData = xData


    def Segment(
            self,
            signal,
            threshold,
            jumpSequenceWindowSize=10,
            noiseVarianceWindowSize=None,
            noiseVarianceEstimateMethod=NoiseVarianceEstimateMethod.Point,
            maxSMLRIterations=300
        ):
        """
        Signal Segmentation Algorithm of Radhakrishnan, et al.  The algorithm is useful for dividing
        a source signal into regions where the signal can be considered constant, but with noise. The
        boundaries of the regions and the value of the signal within each region are not known a priori.


        Parameters
        ----------
        signal : array like
            Input signal to be segmented.
        threshold : double
            Segmentation threshold.
        jumpSequenceWindowSize : integer, optional
            Length of the moving average window sized used for smoothing the input well log
            to arrive at an initial estimate of the jump sequence variance. The default is 10.
        noiseVarianceWindowSize : integer, optional
            Length of the moving average window used for smoothing the noise variances. It
            is recommended to be approximatly half of the jumpSequenceWindowSize.  If it is
            "None" the window will automatically be selected as half the jumpSequenceWindowSize
            The default is None.
        noiseVarianceEstimateMethod : NoiseVarianceEstimateMethod, optional
            Noise variance estimate option.
    		    0 : Point estimate of noise variance.
    		    1 : Noise estimates smoothed within segments.
            The default is NoiseVarianceEstimateMethod.Point.
        maxSMLRIterations : integer, optional
            Upper bound on the number of Single Most Likelihood Replacement iterations. The
            default is 300.

        Returns
        -------
        results : SegmentationResults
            Results of the segmentation.
        """
        # Handle input data type.  We need to pass a list to the C function, so anything else
        # needs to be converted to a list.
        if type(signal) == pd.core.series.Series:
            signal = list(signal.values)

        # Handle options.
        if noiseVarianceWindowSize is None:
            noiseVarianceWindowSize = int(np.round(0.5*jumpSequenceWindowSize))

        results = SegmentC(signal, threshold, jumpSequenceWindowSize, noiseVarianceWindowSize, int(noiseVarianceEstimateMethod), maxSMLRIterations)

        # Check error results and provide a message if an error occured.
        if results.Error < 0:
            raise Exception("An invalid event density estimated after threshold, reduce/increase f and rerun.")

        if results.Error > 0:
            message =  "The logarithm argument became zero at sample number " + str(results.Error)
            message += " during the calculation of likelihood ratios in Single Most Likelihood Replacement iterations.  "
            message += "There may be more samples of this type which may give rise to this problem, edit/rescale data values and rerun."
            raise Exception(message)

        self.results = results
        return results


    def PlotFileteredSignal(self, axis, **kwargs):
        """
        Plots the filtered signal calculated during the signal segmentation.

        Parameters
        ----------
        axis : matplotlib.pyplot.axis
            The axis of the plot.
        **kwargs : keyword arguments
            These arguments are passed on to the plot function.

        Returns
        -------
        None.
        """
        if self.xData is None:
            raise Exception("The x-axis data was not set.")

        axis.plot(self.xData, self.results.FilteredSignal, color="cyan", label="Filtered Signal", **kwargs)


    def PlotSegmentedSignal(self, axis, **kwargs):
        """
        Plots the calculated segmented signal.

        Parameters
        ----------
        axis : matplotlib.pyplot.axis
            The axis of the plot.
        **kwargs : keyword arguments
            These arguments are passed on to the plot function.

        Returns
        -------
        None.
        """
        if self.xData is None:
            raise Exception("The x-axis data was not set.")

        # It seems like we can't just pass two of the same keyword arguments (like "label") and have them automatically overwrite
        # the first value.  So if we want to use defaults for label and color, while allowing them to be overwritten, we need to
        # create a new dictionary and overwrite them in the process of creating it.
        kwargs = {"label" : "Segmented Signal", "color" : "red", **kwargs}
        axis.plot(self.xData, self.results.SegmentedLog, **kwargs)


    def PlotBinaryEvents(self, axis, **kwargs):
        """
        Plots the binary events (the "1"s in the binary event sequence) as vertical lines.

        Parameters
        ----------
        axis : matplotlib.pyplot.axis
            The axis of the plot.
        **kwargs : keyword arguments
            These arguments are passed on to the plot function.

        Returns
        -------
        None.
        """
        yData = PlotHelper.GetYBoundaries(axis)

        label = "Segment Boundry"

        for i in range(self.results.SignalLength):
            if self.results.BinaryEventSequence[i]:
                #"mediumvioletred"
                kwargs.setdefault("linewidth", 0.5)
                kwargs.setdefault("color", "orchid")
                axis.plot([self.xData[i], self.xData[i]], yData, label=label, **kwargs)
                label = None