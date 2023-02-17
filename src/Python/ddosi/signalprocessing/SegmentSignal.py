"""
Created on February 14, 2023
@author: Lance A. Endres
"""
import numpy                                     as np
import pandas                                    as pd
import matplotlib.pyplot                         as plt

from   ddosi.signalprocessing.NoiseVarianceEstimateMethod                      import NoiseVarianceEstimateMethod

from   SegmentSignalPy                           import Segment                as SegmentC
from   SegmentSignalPy                           import SegmentationResults
from   SegmentSignalPy                           import FindSignificantZones

from   lendres.plotting.PlotHelper               import PlotHelper

class SegmentSignal():
    results                     = None
    significantZonesIndices     = None
    significantZoneValues       = None


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
            message = "The logarithm argument became zero at sample number " + str(results.Error)
            message += " during the calculation of likelihood ratios in Single Most Likelihood Replacement iterations.  "
            message += "There may be more samples of this type which may give rise to this problem, edit/rescale data values and rerun."
            raise Exception(message)

        self.results = results
        return results


    def FindSignificantZones(self, xData, threshold, includeBoundaries=False):
        if self.results is None:
            raise Exception("There are no results.  You must first run \"Segment\".")

        self.significantZonesIndices = FindSignificantZones(self.results.BinaryEventSequence, xData, threshold, includeBoundaries)
        self.significantZoneValues   = [[xData[pointSet[0]], xData[pointSet[1]]] for pointSet in self.significantZonesIndices]


    @property
    def NumberOfSignificantZones(self):
        return len(self.significantZonesIndices)


    def PlotFileteredSignal(self, axis, xData, **kwargs):
        axis.plot(xData, self.results.FilteredSignal, color="cyan", label="Filtered Signal", **kwargs)


    def PlotSegmentedSignal(self, axis, xData, **kwargs):
        axis.plot(xData, self.results.SegmentedLog, color="red", label="Segmented Signal", **kwargs)


    def PlotBinaryEvents(self, axis, xData, **kwargs):
        yData = PlotHelper.GetYBoundaries(axis)

        label="Segment Boundry"

        for i in range(self.results.SignalLength):
            if self.results.BinaryEventSequence[i]:
                #"mediumvioletred"
                kwargs.setdefault("linewidth", 0.5)
                kwargs.setdefault("color", "orchid")
                axis.plot([xData[i], xData[i]], yData, **kwargs, label=label)
                label = None


    def PlotSignificantZones(self, axis, xData, threshold, includeBoundaries=False, **kwargs):
        self.FindSignificantZones(xData, threshold, includeBoundaries)

        yData = PlotHelper.GetYBoundaries(axis)

        yBottom = [yData[0], yData[0]]
        yTop = [yData[1], yData[1]]

        label = "Zone"
        for zone, i in zip(self.significantZoneValues, range(self.NumberOfSignificantZones)):
            plt.fill_between(zone, yTop, yBottom, color="blue", alpha=0.15, label=label)
            annotation = axis.annotate(
                i,
                xy=(np.average(zone), yTop[0]),                                # Point to annotate (top center of fill).
                xytext=(0, -3),                                                # Move text down a few points.
                textcoords="offset points",                                    # Specifies that xytext is in points.
                size=0.5*PlotHelper.GetScaledAnnotationSize(),                 # Font size.
                fontweight="bold",                                             # Bold font.
                horizontalalignment="center",                                  # Center text horizontally.
                verticalalignment="top"                                        # Justify to top of text.
            )
            #annotation.
            label = None