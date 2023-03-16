"""
Created on February 14, 2023
@author: Lance A. Endres
"""
import numpy                                     as np
import pandas                                    as pd
import matplotlib.pyplot                         as plt

from itertools                                   import chain

from   SegmentSignalPy                           import SegmentationResults
from   SegmentSignalPy                           import FindSignificantZones

from   lendres.plotting.PlotHelper               import PlotHelper

class SignificantZones():
    significantZonesIndices     = None
    significantZoneValues       = None
    xData                       = None

    def __init__(self, segmentationResults, xData=None):
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
        self.results = segmentationResults
        self.xData   = xData


    def FindSignificantZones(self, threshold, includeBoundaries=False):
        if self.results is None:
            raise Exception("There are no results.  You must first run \"Segment\".")

        if self.xData is None:
            raise Exception("The x-axis data was not set.")

        self.significantZonesIndices = FindSignificantZones(self.results.BinaryEventSequence, self.xData, threshold, includeBoundaries)
        self._CalculateZoneValues()


    def _CalculateZoneValues(self):
        self.significantZoneValues   = [[self.xData[pointSet[0]], self.xData[pointSet[1]]] for pointSet in self.significantZonesIndices]


    @property
    def NumberOfSignificantZones(self):
        """
        Returns
        -------
        int
            The number of significant zones.
        """
        return len(self.significantZonesIndices)


    def PlotSignificantZones(self, axis, legendPrefix=""):
        if self.significantZonesIndices is None:
            raise Exception("There are no indices.  Run \"FindSignificantZones\" first.")

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
        if self.significantZonesIndices is None:
            raise Exception("There are no indices.  Run \"FindSignificantZones\" first.")

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


    def IgnoreZones(self, zones):
        """
        Specifies zones to ignore (remove from set of significant zones.)  This does not alter the data in any way, it just removes
        the zone information.  This is a manual way of specifying that the zone is not signficant.

        Parameters
        ----------
        zones : list of ints
            The numbers (indices) of the zones to ignore.

        Returns
        -------
        None.
        """
        newIndices = []
        newValues  = []

        # Loop through the zones and copy all values expcept those specified in the input.
        for i in range(0, len(self.significantZonesIndices)):
            if not i in zones:
                newIndices.append(self.significantZonesIndices[i])
                newValues.append(self.significantZoneValues[i])

        # Update the class's indices and values.
        self.significantZonesIndices = newIndices
        self.significantZoneValues   = newValues


    def MergeZones(self, zones):
        if len(zones) < 1:
            return

        newIndices = []
        startZone  = zones[0]
        i = 0
        while i < len(self.significantZonesIndices):
            print(i)
            if i == startZone:
                # Get the start index of the merged zones.
                startIndex = (self.significantZonesIndices[i])[0]

                # Use the end zone to get the end index.
                endZone = zones[1]
                endIndex   = (self.significantZonesIndices[endZone])[1]
                newIndices.append([startIndex, endIndex])
                i = endZone + 1
            else:
                newIndices.append(self.significantZonesIndices[i])
                i += 1
        self.significantZonesIndices = newIndices
        self._CalculateZoneValues()


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


    def UnionSignificantZones(self, secondSignificantZones):
        allZones = [list(zone) for zone in self.significantZonesIndices]
        for zone in secondSignificantZones.significantZonesIndices:
            allZones.append(list(zone))
        print("\nAll zones", allZones)
        unions = []
        for begin, end in sorted(allZones):
            if unions and unions[-1][1] >= begin - 1:
                unions[-1][1] = max(unions[-1][1], end)
            else:
                unions.append([begin, end])

        newSignificantZones = SignificantZones(self.results, self.xData)
        newSignificantZones.significantZonesIndices = unions
        newSignificantZones._CalculateZoneValues()
        return newSignificantZones


    def IntersectionSignificantZones(self, otherSignificantZones):
        print()
        intersections = []
        for zone in self.significantZonesIndices:
            for otherZone in otherSignificantZones.significantZonesIndices:
                largestMin = max(zone[0], otherZone[0])
                smallestMax = min(zone[1], otherZone[1])
                if smallestMax > largestMin:
                    intersections.append([largestMin, smallestMax])
        newSignificantZones = SignificantZones(self.results, self.xData)
        newSignificantZones.significantZonesIndices = intersections
        newSignificantZones._CalculateZoneValues()
        return newSignificantZones