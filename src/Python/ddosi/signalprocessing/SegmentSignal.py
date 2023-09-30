"""
Created on February 14, 2023
@author: Lance A. Endres
"""
import numpy                                                         as np
import pandas                                                        as pd

from   ddosi.signalprocessing.NoiseVarianceEstimateMethod            import NoiseVarianceEstimateMethod

from   SegmentSignalPy                                               import Segment                          as SegmentC

from   lendres.plotting.AxesHelper                                   import AxesHelper


class SegmentSignal():
    """
    Interface to Segment Signal algorithm.
    """


    def __init__(self, xData=None):
        """
        Contructor.

        Parameters
        ----------
        xData : array like or string
            The x-axis data.  Not required to segment, but is required for a lot of plotting and post processing.
            If "dataFrame" is provided, "xData" can be a string that is the column name of the x-axis data in the
            DataFrame.

        Returns
        -------
        None.
        """
        self.xData     = xData
        self.results   = None


    def Segment(
            self,
            signal,
            threshold:float,
            jumpSequenceWindowSize:int=10,
            noiseVarianceWindowSize:int=None,
            noiseVarianceEstimateMethod=NoiseVarianceEstimateMethod.Point,
            maxSMLRIterations:int=300
        ):
        """
        Signal Segmentation Algorithm of Radhakrishnan, et al.  The algorithm is useful for dividing
        a source signal into regions where the signal can be considered constant, but with noise. The
        boundaries of the regions and the value of the signal within each region are not known a priori.


        Parameters
        ----------
        signal : array like
            Input signal to be segmented.
        threshold : float
            Segmentation threshold.
        jumpSequenceWindowSize : int, optional
            Length of the moving average window sized used for smoothing the input well log
            to arrive at an initial estimate of the jump sequence variance. The default is 10.
        noiseVarianceWindowSize : int, optional
            Length of the moving average window used for smoothing the noise variances. It
            is recommended to be approximatly half of the jumpSequenceWindowSize.  If it is
            "None" the window will automatically be selected as half the jumpSequenceWindowSize
            The default is None.
        noiseVarianceEstimateMethod : NoiseVarianceEstimateMethod, optional
            Noise variance estimate option.
    		    0 : Point estimate of noise variance.
    		    1 : Noise estimates smoothed within segments.
            The default is NoiseVarianceEstimateMethod.Point.
        maxSMLRIterations : int, optional
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

        # Add the label and color width to the kwargs if they do not already exist in the dictionary.
        kwargs.setdefault("label", "Filtered Signal")
        kwargs.setdefault("color", "cyan")

        axis.plot(self.xData, self.results.FilteredSignal, **kwargs)


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

        # Add the label and color width to the kwargs if they do not already exist in the dictionary.
        kwargs.setdefault("label", "Segmented Signal")
        kwargs.setdefault("color", "red")

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
        yData = AxesHelper.GetYBoundaries(axis)

        label = "Segment Boundry"

        # Add the color and line width to the kwargs if they do not already exist in the dictionary.
        kwargs.setdefault("linewidth", 0.5)
        kwargs.setdefault("color", "orchid")

        for i in range(self.results.SignalLength):
            if self.results.BinaryEventSequence[i]:
                axis.plot([self.xData[i], self.xData[i]], yData, label=label, **kwargs)
                label = None