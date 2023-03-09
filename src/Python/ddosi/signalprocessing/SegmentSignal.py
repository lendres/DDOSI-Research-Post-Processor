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
    significantZonesIndices     = None
    significantZoneValues       = None
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
            message = "The logarithm argument became zero at sample number " + str(results.Error)
            message += " during the calculation of likelihood ratios in Single Most Likelihood Replacement iterations.  "
            message += "There may be more samples of this type which may give rise to this problem, edit/rescale data values and rerun."
            raise Exception(message)

        self.results = results
        return results


    def FindSignificantZones(self, threshold, includeBoundaries=False):
        if self.results is None:
            raise Exception("There are no results.  You must first run \"Segment\".")

        if self.xData is None:
            raise Exception("The x-axis data was not set.")

        self.significantZonesIndices = FindSignificantZones(self.results.BinaryEventSequence, self.xData, threshold, includeBoundaries)
        self.significantZoneValues   = [[self.xData[pointSet[0]], self.xData[pointSet[1]]] for pointSet in self.significantZonesIndices]


    @property
    def NumberOfSignificantZones(self):
        return len(self.significantZonesIndices)


    def PlotFileteredSignal(self, axis, **kwargs):
        if self.xData is None:
            raise Exception("The x-axis data was not set.")

        axis.plot(self.xData, self.results.FilteredSignal, color="cyan", label="Filtered Signal", **kwargs)


    def PlotSegmentedSignal(self, axis, **kwargs):
        if self.xData is None:
            raise Exception("The x-axis data was not set.")

        axis.plot(self.xData, self.results.SegmentedLog, color="red", label="Segmented Signal", **kwargs)


    def PlotBinaryEvents(self, axis, **kwargs):
        yData = PlotHelper.GetYBoundaries(axis)

        label="Segment Boundry"

        for i in range(self.results.SignalLength):
            if self.results.BinaryEventSequence[i]:
                #"mediumvioletred"
                kwargs.setdefault("linewidth", 0.5)
                kwargs.setdefault("color", "orchid")
                axis.plot([self.xData[i], self.xData[i]], yData, **kwargs, label=label)
                label = None


    def PlotSignificantZones(self, axis, threshold, legendPrefix="", includeBoundaries=False, **kwargs):
        # Find signifcant zones will raise the exception if there isn't any x-axis data, so no need to do it here.
        self.FindSignificantZones(threshold, includeBoundaries)

        yData = PlotHelper.GetYBoundaries(axis)

        yBottom = [yData[0], yData[0]]
        yTop    = [yData[1], yData[1]]

        label = legendPrefix+" "+"Zone" if legendPrefix!="" else "Zone"
        for zone, i in zip(self.significantZoneValues, range(self.NumberOfSignificantZones)):
            plt.fill_between(zone, yTop, yBottom, color="blue", alpha=0.15, label=label)
            axis.annotate(
                i,
                xy=(np.average(zone), yTop[0]),                                # Point to annotate (top center of fill).
                xytext=(0, -3),                                                # Move text down a few points.
                textcoords="offset points",                                    # Specifies that xytext is in points.
                size=0.5*PlotHelper.GetScaledAnnotationSize(),                 # Font size.
                fontweight="bold",                                             # Bold font.
                horizontalalignment="center",                                  # Center text horizontally.
                verticalalignment="top"                                        # Justify to top of text.
            )
            label = None


    def DropDataByZoneRange(self, data, xData, startZone, endZone, keep=False):
        # Indices in the DataFrame.
        startIndex = (self.significantZonesIndices[startZone])[0]
        endIndex   = (self.significantZonesIndices[endZone])[1]

        if keep:
            dropIndices = list(chain(range(0, startIndex-1), range(endIndex+1, data.shape[0])))
            dropZones   = list(chain(range(0, startZone-1),  range(endZone+1, len(self.significantZoneValues)-1)))
        else:
            dropIndices = list(range(startIndex, endIndex))
            dropZones   = list(range(startZone, endZone))

        self._DropResults(dropIndices)
        self.significantZonesIndices = np.delete(self.significantZonesIndices, dropZones)
        self.significantZoneValues   = np.delete(self.significantZoneValues, dropZones)

        # Generate new data as a subset of the old.
        dataSubset = data.drop(dropIndices, inplace=False).reset_index()

        # Update the x-axis data.  This must be done after the data has been updated to make sure we get the new, reduced data.
        if type(xData) == str:
            self.xData = dataSubset[xData]
        elif type(xData) is np.ndarray:
            self.xData = np.delete(xData, dropIndices)
        elif type(xData) == pd.core.series.Series:
            self.xData = xData.drop(dropIndices, inplace=False).reset_index()

        return dataSubset


    def _DropResults(self, dropIndices):
        binaryEventSequence = np.delete(self.results.BinaryEventSequence, dropIndices)

        self.results = SegmentationResults(
            len(binaryEventSequence),
            binaryEventSequence,
            sum(binaryEventSequence),
            np.delete(self.results.FilteredSignal, dropIndices),
            np.delete(self.results.SegmentedLog, dropIndices),
            np.delete(self.results.NoiseVariance, dropIndices),
            self.results.JumpSequenceVariance,
            self.results.SegmentDensity,
            self.results.Iterations,
            self.results.Error
        )

        print(len(binaryEventSequence))