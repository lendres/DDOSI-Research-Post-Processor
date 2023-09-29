"""
Created on March 15, 2023
@author: Lance A. Endres
"""
import pandas                                                        as pd
import matplotlib.pyplot                                             as plt
import matplotlib

from   lendres.plotting.AxesHelper                                   import AxesHelper
from   lendres.plotting.PlotHelper                                   import PlotHelper
from   lendres.plotting.PlotMaker                                    import PlotMaker
from   lendres.plotting.LegendHelper                                 import LegendHelper
from   lendres.plotting.LegendOptions                                import LegendOptions

from   ddosi.plotting.DesignatedColors                               import DesignatedColors


class Plots():


    @classmethod
    def CreateWobAndRotarySpeedPlot(cls, data:pd.DataFrame, yAxisColumn:str="Depth", yUnits:str="cm", wobColumn:str="Weight on Bit", rpmColumn:str="Rotary Speed", title:str="Weight on Bit and Rotary Speed", titleSuffix:str=None, legendOptions:LegendOptions=LegendOptions(), **kwargs):
        """
        Creates a depth based weight on bit and rotary speed plot.  The weight on bit and rotary speed are plotted on their own axes.  If specified,
        a legend is generated.  The plot is finalized.

        This function uses DesignatedColors to provide default colors for the plotted lines.

        Parameters
        ----------
        data : pd.DataFrame
            The data.
        yAxisColumn : str, optional
            The column name of the depth data to use as the y-axis values. The default is "Depth".
        wobColumn : str, optional
            The column name of the weight on bit data. The default is "Weight on Bit".
        rpmColumn : str, optional
            The column name of the rotary speed data. The default is "Rotary Speed".
        title : str, optional
            The figure title. The default is "Weight on Bit and Rotary Speed".
        titleSuffix : str, optional
            If specified, it is added as a second line immediately under "title". The default is None.
        legendOptions : LegendOptions, optional
            Options that specify if and how the legend is generated. The default is LegendOptions().
        **kwargs : keyword arguments
            These arguments are passed to the plot function.  Each keyword argument can be a single value or a list.  If it is
            a single value, the same value is used for every call to plat.  If it is a list, the values are passed in order to
            each series as it is plotted.
            Example 1:
                axesesColumnNames=['Column 1', 'Column 2'], linewidth=4
            Result
                The data in 'Column 1' and 'Column 2' are potted with a 'linewidth' of 4.
            Example 2:
                axesesColumnNames=['Column 1', ['Column 2', 'Column 3'], 'Column 4'], linewidth=[1, 2, 3, 4]
            Result
                The data in 'Column 1', 'Column 2', 'Column 3', and 'Column 4' are potted with a 'linewidth's of 1. 2. 3. and 4, respectively.

        Returns
        -------
        figure : matplotlib.figure.Figure
            The newly created figure.
        axeses : tuple of matplotlib.axes.Axes
            The axes of the plot.
        """
        figure, axeses = cls.NewWobAndRotarySpeedPlot(data, yAxisColumn, wobColumn, yUnits, rpmColumn, title, titleSuffix, **kwargs)
        LegendHelper.CreateLegendAtFigureBottom(figure, axeses[0], offset=0.02*PlotHelper.GetSettings().Scale, legendOptions=legendOptions)
        plt.show()
        return figure, axeses


    @classmethod
    def NewWobAndRotarySpeedPlot(cls, data:pd.DataFrame, yAxisColumn:str="Depth", wobColumn:str="Weight on Bit", yUnits:str="cm", rpmColumn:str="Rotary Speed", title:str="Weight on Bit and Rotary Speed", titleSuffix:str=None, **kwargs):
        """
        Creates a depth based weight on bit and rotary speed plot.  The weight on bit and rotary speed are plotted on their own axes.  The plot is NOT finalized.

        Use this function to continue plotting

        This function uses DesignatedColors to provide default colors for the plotted lines.

        Parameters
        ----------
        data : pd.DataFrame
            The data.
        yAxisColumn : str, optional
            The column name of the depth data to use as the y-axis values. The default is "Depth".
        wobColumn : str, optional
            The column name of the weight on bit data. The default is "Weight on Bit".
        rpmColumn : str, optional
            The column name of the rotary speed data. The default is "Rotary Speed".
        title : str, optional
            The figure title. The default is "Weight on Bit and Rotary Speed".
        titleSuffix : str, optional
            If specified, it is added as a second line immediately under "title". The default is None.
        legendOptions : LegendOptions, optional
            Options that specify if and how the legend is generated. The default is LegendOptions().
        **kwargs : keyword arguments
            These arguments are passed to the plot function.  Each keyword argument can be a single value or a list.  If it is
            a single value, the same value is used for every call to plat.  If it is a list, the values are passed in order to
            each series as it is plotted.
            Example 1:
                axesesColumnNames=['Column 1', 'Column 2'], linewidth=4
            Result
                The data in 'Column 1' and 'Column 2' are potted with a 'linewidth' of 4.
            Example 2:
                axesesColumnNames=['Column 1', ['Column 2', 'Column 3'], 'Column 4'], linewidth=[1, 2, 3, 4]
            Result
                The data in 'Column 1', 'Column 2', 'Column 3', and 'Column 4' are potted with a 'linewidth's of 1. 2. 3. and 4, respectively.

        Returns
        -------
        figure : matplotlib.figure.Figure
            The newly created figure.
        axeses : tuple of matplotlib.axes.Axes
            The axes of the plot.
        """
        yDataLabels    = [[wobColumn], [rpmColumn]]

        kwargs         = DesignatedColors.ApplyKeyWordArgumentsToColors(kwargs, yDataLabels)
        figure, axeses = PlotMaker.NewMultiXAxesPlot(data, yAxisColumn, yDataLabels, **kwargs)

        cls.SetFigureSize(figure)

        AxesHelper.Label(axeses, title, ["Weight on Bit (tons)", "Revolutions per Minute"], yAxisColumn+" ("+yUnits+")", titleSuffix=titleSuffix)

        # For depth based plots we want the smallest value at the top, so we need to reverse the axis limits.
        AxesHelper.ReverseYAxisLimits(axeses[0])

        return figure, axeses


    @classmethod
    def SetFigureSize(self, figure:matplotlib.figure.Figure):
        """
        Set the figure size.

        Parameters
        ----------
        figure : matplotlib.figure.Figure
            The figure..

        Returns
        -------
        None.
        """
        figure.set_figwidth(6.8)
        figure.set_figheight(12)