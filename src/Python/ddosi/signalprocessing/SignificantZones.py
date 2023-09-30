"""
Created on February 14, 2023
@author: Lance A. Endres
"""
import numpy                                                         as np
import pandas                                                        as pd
import matplotlib.pyplot                                             as plt
import matplotlib

from   itertools                                                     import chain

from   SegmentSignalPy                                               import SegmentationResults
from   SegmentSignalPy                                               import FindSignificantZones

from   lendres.plotting.AxesHelper                                   import AxesHelper
from   lendres.plotting.PlotHelper                                   import PlotHelper


class SignificantZones():


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
        self.results                    = segmentationResults
        self.xData                      = xData
        self.significantZonesIndices    = None


    def Copy(self, xData=None):
        newSignificantZones                         = SignificantZones(self.results, self.xData)
        newSignificantZones.significantZonesIndices = self.significantZonesIndices

        if xData is not None:
            newSignificantZones.xData = xData

        return newSignificantZones


    @property
    def NumberOfZones(self):
        """
        Returns
        -------
        : int
            The number of significant zones.
        """
        return len(self.significantZonesIndices)


    def FindSignificantZones(self, threshold:float, includeBoundaries:bool=False):
        """
        Finds the zones that are longer than the specified threshold.  The threshold is in the x-axis units.  For example, if plotted in time, the
        threshold would be in seconds, minutes, et cetera.

        Parameters
        ----------
        threshold : float
            The minimum length a zone must be to qualify as significant.  Zones smaller than this are ignored.
        includeBoundaries : bool, optional
            Specifies if the boundaries should be included as part of the zone.  I.e., the starting edge and trailing edge (binary event). The default is False.

        Returns
        -------
        None.
        """
        if self.results is None:
            raise Exception("There are no results.  You must first run \"Segment\".")

        if self.xData is None:
            raise Exception("The x-axis data was not set.")

        self.significantZonesIndices = FindSignificantZones(self.results.BinaryEventSequence, self.xData, threshold, includeBoundaries)


    def InvertSignificantZones(self, ignoreStart:bool=False, ignoreEnd:bool=False):
        """
        Finds the inverse of the signficant zones.  Essentially, this creates significant zones out of the regions between significant zones.

        Often there are small insignificant zones at the start and end of the data set that are not of interest in the inverted zones.  These can
        be ignored using the arguments.

        Parameters
        ----------
        ignoreStart : bool, optional
            An option to ignore the first zone in the inverted set.  This parameter only applies if the first signficant zone does not start at the first data value (index 0). The default is False.
        ignoreEnd : bool, optional
            An option to ignore the last zone in the inverted set.  This parameter only applies if the last signficant zone does not start at the last data value (last index). The default is False.

        Returns
        -------
        None.
        """
        newIndices = []

        firstIndex = (self.significantZonesIndices[0])[0]
        if firstIndex > 0 and not ignoreStart:
            newIndices.append([0, firstIndex])

        numberOfZones = self.NumberOfZones

        for i in range(numberOfZones-1):
            newIndices.append([(self.significantZonesIndices[i])[1], (self.significantZonesIndices[i+1])[0]])

        lastIndex     = (self.significantZonesIndices[numberOfZones-1])[1]
        dataLastIndex = len(self.xData) - 1
        if dataLastIndex > lastIndex and not ignoreEnd:
            newIndices.append([lastIndex, dataLastIndex])

        # Save the new indices.
        self.significantZonesIndices = newIndices


    def GetZoneValues(self, zones:int|list=None):
        """
        Retrieves the values associated with the zone boundry indices.

        Parameters
        ----------
        zones : int|list
            The zones to extract the values for.  If None is specified, all the zone values are returned.  The default is None.

        Returns
        -------
        : list | list of lists
            The start and stop value of each requested zone.  If only one zone is requested, a list is returned.  If multiple zones are requested,
            return a list of lists.
        """
        match zones:
            case None:
                # Convert all the indices to values.
                return [[self.xData[indexSet[0]], self.xData[indexSet[1]]] for indexSet in self.significantZonesIndices]

            case int() | np.int64():
                # Extract just the one zone of interest and return it as a list.
                zone = self.significantZonesIndices[zones]
                return [self.xData[zone[0]], self.xData[zone[1]]]

            case list():
                # Extract the request set of zones and convert those indices to values.
                zones = [self.significantZonesIndices[zone] for zone in zones]
                return [[self.xData[indexSet[0]], self.xData[indexSet[1]]] for indexSet in zones]

            case _:
                raise Exception("The parameters 'zones' is an unknown type.")



    def PlotZones(self, axes:matplotlib.axes.Axes, **kwargs):
        """
        Plots the significant zones as shaded boxes and numbers them at the top.

        A default label of "Zone" is applied if none is specified.

        Parameters
        ----------
        axes : matplotlib.axes.Axes
            The axis of the plot.
        **kwargs : keyword arguments
            Keyword arguments passed to the fill_between plotting function.

        Returns
        -------
        None.
        """
        # Add default kwargs if they do not already exist in the dictionary.
        kwargs.setdefault("label", "Zone")
        kwargs.setdefault("facecolor", (0,0,1,0.075))
        kwargs.setdefault("edgecolor", (0,0,1,0.30))

        self._PlotZoneBoundaries(axes, **kwargs)
        self._AnnotateZones(axes)


    def HighlightZones(self, axes:matplotlib.axes.Axes, zones:list, **kwargs):
        """
        Highlights the specified zones in an alternate color.

        Parameters
        ----------
        axes : matplotlib.axes.Axes
            The axis of the plot.
        zones : list
            Zone numbers to highlight.
        **kwargs : keyword arguments
            Keyword arguments passed to the fill_between plotting function.

        Returns
        -------
        None.
        """
        # Add default kwargs if they do not already exist in the dictionary.
        kwargs.setdefault("label", "Highlighted Zone")
        kwargs.setdefault("facecolor", (1,0.9,0.6,0.2))
        kwargs.setdefault("edgecolor", (1,0.63,0,1.0))

        self._PlotZoneBoundaries(axes, zones, **kwargs)


    def _PlotZoneBoundaries(self, axes:matplotlib.axes.Axes, zones:list=None, **kwargs):
        """
        Plots the specified zones as shaded boxes.  The face and edge color for the fill must be specified in the keyword arguments.

        Parameters
        ----------
        axes : matplotlib.axes.Axes
            The axis of the plot.
        zones : list, optional
            Zone numbers to plot.  If None, all the zones are plotted.  The default is None.
        **kwargs : keyword arguments
            Keyword arguments passed to the fill_between plotting function.

        Returns
        -------
        None.
        """
        if self.significantZonesIndices is None:
            raise Exception("There are no indices.  Run \"FindSignificantZones\" first.")

        yTop, yBottom = self._GetYBoundryLists(axes)

        if zones is None:
            zones = list(range(self.NumberOfZones))

        for zone, i in zip(self.GetZoneValues(zones), zones):
            # Fill between two horizontal line segements.  The x data is used for both curves.
            # Top line: (zone[0], yTop) to (zone[1], yTop)
            # Bottom line: (zone[0], yBttom) to (zone[1], yBottom)
            patch = plt.fill_between(zone, yTop, yBottom, **kwargs)

            # Provide a name so we can find the patch later if needed.
            patch.zoneName = "Zone " + str(i)

            # Remove the fill label so that only the first one shows up in the legend.
            kwargs["label"] = None


    def _AnnotateZones(self, axes:matplotlib.axes.Axes):
        """
        Numbers each zone at the top center of the zone.

        Parameters
        ----------
        axes : matplotlib.axes.Axes
            DESCRIPTION.

        Returns
        -------
        None.
        """
        # Get the top of the y axis.
        yPosition = (AxesHelper.GetYBoundaries(axes))[1]

        for zone, i in zip(self.GetZoneValues(), range(self.NumberOfZones)):
            # Number the zone at the top, inside, center of the zone.
            axes.annotate(
                i,
                xy=(np.average(zone), yPosition),                              # Point to annotate (top center of fill).
                xytext=(0, -3),                                                # Move text down a few points.
                textcoords="offset points",                                    # Specifies that xytext is in points.
                size=0.5*PlotHelper.GetScaledAnnotationSize(),                 # Font size.
                fontweight="bold",                                             # Bold font.
                horizontalalignment="center",                                  # Center text horizontally.
                verticalalignment="top"                                        # Justify to top of text.
            )


    def _GetYBoundryLists(self, axes:matplotlib.axes.Axes):
        """
        Gets the top and bottom boundries of the axes in a format suitable for plotting with the "fill_between" function.

        Parameters
        ----------
        axes : matplotlib.axes.Axes
            The axes to get the boundaries from..

        Returns
        -------
        yTop : list
            The top value as a list.
        yBottom : list
            The bottom value as a list.
        """
        yData   = AxesHelper.GetYBoundaries(axes)
        yBottom = [yData[0], yData[0]]
        yTop    = [yData[1], yData[1]]
        return yTop, yBottom


    def DropDataByZoneRange(self, data, xData, startZone, endZone, keep=False):
        if self.significantZonesIndices is None:
            raise Exception("There are no indices.  Run \"FindSignificantZones\" first.")

        # Indices in the DataFrame.
        startIndex = (self.significantZonesIndices[startZone])[0]
        endIndex   = (self.significantZonesIndices[endZone])[1]

        if keep:
            dropIndices = list(chain(range(0, startIndex), range(endIndex+1, data.shape[0])))
            dropZones   = list(chain(range(0, startZone),  range(endZone+1, len(self.significantZonesIndices))))

            # If we are keeping the zones, some data at the start can be removed, so we have to adjust the indices to account.
            self.significantZonesIndices -= startIndex
        else:
            dropIndices = list(range(startIndex, endIndex+1))
            dropZones   = list(range(startZone, endZone+1))
            self._AdjustZoneIndicesForRemovedSection(startIndex, endIndex)

        self._DropResults(dropIndices)
        self.significantZonesIndices = np.delete(self.significantZonesIndices, dropZones, axis=0)

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


    def _AdjustZoneIndicesForRemovedSection(self, startIndex:int, endIndex:int):
        """
        Adjusts the zone indices for remove a section of data from the middle.

        Parameters
        ----------
        startIndex : int
            The starting index of the removed data.
        endIndex : int
            The ending index of the removed data.

        Returns
        -------
        None.
        """
        length = endIndex - startIndex

        # Loop over the signficant zones.  For everthing before the start zone, we just copy the zone indices.  Once we find the start zone, we
        # create a set of indices out of the start of the start zone and end of the end zone.  The remaining indices are then copied.
        for i in range(len(self.significantZonesIndices)):
            # If the current zone ends after the end index, we need to start subtracting the removed indices.
            if (self.significantZonesIndices[i])[1] > endIndex:
                for j in range(len(self.significantZonesIndices[i])):
                    (self.significantZonesIndices[i])[j] -= length


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

        # Loop through the zones and copy all values expcept those specified in the input.
        for i in range(0, len(self.significantZonesIndices)):
            if not i in zones:
                newIndices.append(self.significantZonesIndices[i])

        # Update the class's indices and values.
        self.significantZonesIndices = newIndices


    def MergeZones(self, zones:list):
        """
        Creates one zone out of everything between the start zone and the end zone.  This includes any intermediate zones and any data that was otherwise excluded.  Saves
        the new set of zone indices to self.

        Parameters
        ----------
        zones : list
            The start zone and end zone indices.

        Returns
        -------
        None.
        """
        if len(zones) < 1:
            return

        newIndices = []
        startZone  = zones[0]
        i          = 0

        # Loop over the signficant zones.  For everthing before the start zone, we just copy the zone indices.  Once we find the start zone, we
        # create a set of indices out of the start of the start zone and end of the end zone.  The remaining indices are then copied.
        while i < len(self.significantZonesIndices):
            if i == startZone:
                # Get the start index of the merged zones (start of the start zone).
                startIndex = (self.significantZonesIndices[i])[0]

                # Use the end zone to get the end index.
                endZone    = zones[1]
                endIndex   = (self.significantZonesIndices[endZone])[1]

                # Create a new zone from the start of the start zone and end of the end zone.
                newIndices.append([startIndex, endIndex])

                # We need to now skip to the next zone.
                i = endZone + 1
            else:
                # Copy the existing indices and move to the next zone.
                newIndices.append(self.significantZonesIndices[i])
                i += 1

        # Save the new indices.
        self.significantZonesIndices = newIndices


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
        intersections = []
        for zone in self.significantZonesIndices:
            for otherZone in otherSignificantZones.significantZonesIndices:
                largestMin = max(zone[0], otherZone[0])
                smallestMax = min(zone[1], otherZone[1])
                if smallestMax > largestMin:
                    intersections.append([largestMin, smallestMax])
        newSignificantZones = SignificantZones(self.results, self.xData)
        newSignificantZones.significantZonesIndices = intersections
        return newSignificantZones


    def ExtractDataByZones(self, data, zones):
        keepIndices = []

        # Allow for input of a single zone by converting it to a list so the loop below works.
        if type(zones) is not list:
            zones = [zones]

        for zone in zones:
            # Indices in the DataFrame.
            startIndex = (self.significantZonesIndices[zone])[0]
            endIndex   = (self.significantZonesIndices[zone])[1]

            keepIndices = list(chain(keepIndices, range(startIndex, endIndex)))

        # Start with a list of all the indices and remove the ones we are keeping to generate a list of dropped indices.
        allIndices  = range(data.shape[0])
        dropIndices = [i for i in allIndices if i not in keepIndices]

        # Generate new data as a subset of the old.
        dataSubset = data.drop(dropIndices, inplace=False).reset_index()
        return dataSubset