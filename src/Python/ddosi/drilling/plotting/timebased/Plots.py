"""
Created on March 15, 2023
@author: Lance A. Endres
"""
import pandas                                                        as pd
import matplotlib.pyplot                                             as plt

from   lendres.plotting.AxesHelper                                   import AxesHelper
from   lendres.plotting.PlotHelper                                   import PlotHelper
from   lendres.plotting.PlotMaker                                    import PlotMaker
from   lendres.plotting.LegendHelper                                 import LegendHelper
from   lendres.plotting.LegendOptions                                import LegendOptions
from   lendres.datatypes.ListTools                                   import ListTools

from   ddosi.plotting.DesignatedColors                               import DesignatedColors
from   ddosi.units.Units                                             import Units


class Plots():

    @classmethod
    def CreateWobAndRotarySpeedPlot(cls, data:pd.DataFrame, xAxisColumn:str="Time", wobColumn:str="Weight on Bit", rpmColumn:str="Rotary Speed", title:str="Weight on Bit and Rotary Speed", titleSuffix:str=None, legendOptions:LegendOptions=LegendOptions(), **kwargs):
        """
        Creates a time based weight on bit and rotary speed plot.  The weight on bit and rotary speed are plotted on their own axes.  If specified,
        a legend is generated.  The plot is finalized.

        This function uses DesignatedColors to provide default colors for the plotted lines.

        Parameters
        ----------
        data : pd.DataFrame
            The data.
        xAxisColumn : str, optional
            The column name of the time data to use as the x-axis values. The default is "Time".
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
        """
        figure, axeses = cls.NewWobAndRotarySpeedPlot(data, xAxisColumn, wobColumn, rpmColumn, title, titleSuffix, **kwargs)
        LegendHelper.CreateLegendAtFigureBottom(figure, axeses[0], offset=0.15*PlotHelper.GetSettings().Scale, legendOptions=legendOptions)
        plt.show()
        return figure


    @classmethod
    # @ureg.wraps((None, None), (None, None, None, None, None, None, None, None), False)
    def NewWobAndRotarySpeedPlot(cls, data:pd.DataFrame, xAxisColumn:str="Time", wobColumn:str="Weight on Bit", rpmColumn:str="Rotary Speed", title:str="Weight on Bit and Rotary Speed", titleSuffix:str=None, **kwargs):
        yDataLabels    = [[wobColumn], [rpmColumn]]
        kwargs         = DesignatedColors.ApplyKeyWordArgumentsToColors(kwargs, yDataLabels)

        convertedData, xSuffix, ySuffixes = Units.ConvertOutput(data, xAxisColumn, yDataLabels)
        figure, axeses                    = PlotMaker.NewMultiYAxesPlot(convertedData, xAxisColumn, yDataLabels, **kwargs)

        # Title and labels.
        xLabel  = Units.CombineLabelsAndUnits(xAxisColumn, xSuffix)
        yLabels = Units.CombineLabelsAndUnits(["Weight on Bit", "Rotary Speed"], ySuffixes)
        AxesHelper.Label(axeses, title, xLabel, yLabels, titleSuffix=titleSuffix)

        return figure, axeses


    @classmethod
    def CreateTobWobAndRotarySpeedPlot(cls, data:pd.DataFrame, xAxisColumn:str="Time", tobColumn:str="Torque on Bit", wobColumn:str="Weight on Bit", rpmColumn:str="Rotary Speed", title:str="Torque", titleSuffix:str=None, legendOptions:LegendOptions=LegendOptions(), **kwargs):
        figure, axeses = cls.NewTobWobAndRotarySpeedPlot(data, xAxisColumn, tobColumn, wobColumn, rpmColumn, title, titleSuffix, **kwargs)
        LegendHelper.CreateLegendAtFigureBottom(figure, axeses[0], offset=0.15*PlotHelper.GetSettings().Scale, legendOptions=legendOptions)
        plt.show()
        return figure


    @classmethod
    def NewTobWobAndRotarySpeedPlot(cls, data:pd.DataFrame, xAxisColumn:str="Time", tobColumn:str="Torque on Bit", wobColumn:str="Weight on Bit", rpmColumn:str="Rotary Speed", title:str="Torque", titleSuffix:str=None, **kwargs):
        return cls.NewParameterWobAndRotarySpeedPlot(title, data, xAxisColumn, "Torque", tobColumn, wobColumn, rpmColumn, titleSuffix, **kwargs)


    @classmethod
    def NewRopWobAndRotarySpeedPlot(cls, data:pd.DataFrame, xAxisColumn:str="Time", ropColumn:str="Rate of Penetration", wobColumn:str="Weight on Bit", rpmColumn:str="Rotary Speed", title:str="Rate of Penetration", titleSuffix:str=None, **kwargs):
        return cls.NewParameterWobAndRotarySpeedPlot(title, data, xAxisColumn, "Rate of Penetration", ropColumn, wobColumn, rpmColumn, titleSuffix, **kwargs)


    @classmethod
    def NewDepthOfCutWobAndRotarySpeedPlot(cls, data:pd.DataFrame, xAxisColumn:str="Time", depthOfCutColumn:str="Depth of Cut", wobColumn:str="Weight on Bit", rpmColumn:str="Rotary Speed", title:str="Depth of Cut", titleSuffix:str=None, **kwargs):
        return cls.NewParameterWobAndRotarySpeedPlot(title, data, xAxisColumn, "Depth of Cut", depthOfCutColumn, wobColumn, rpmColumn, titleSuffix, **kwargs)


    @classmethod
    def CreateParameterWobAndRotarySpeedPlot(cls, title:str, data:pd.DataFrame, xAxisColumn:str, parameterLabel:str, parameterColumn:str, wobColumn:str="Weight on Bit", rpmColumn:str="Rotary Speed", titleSuffix:str=None, legendOptions:LegendOptions=LegendOptions(), **kwargs):
        """
        Plots a parameter versus the weight on bit and rotary speed on a multi y-axes figure.  The parameter is read off of the left axis and the weight on bit and rotary speed
        have axes on the right side.

        This assumes all the data (parameter, WOB, and rotary speed) are in the same data frame and have been sampled at the same rate (same x-axis data).

        Parameters
        ----------
        title : str
            The first line of the title..
        data : pd.DataFrame
            The data.
        xAxisColumn : str
            The column name of the x-axis data.
        parameterLabel : str
            Left y-axis label.
        parameterColumn : str
            The column name of the parameter to plot on the left axis.
        wobColumn : str, optional
            The column name of the weight on bit. The default is "Weight on Bit".
        rpmColumn : str, optional
            The column name of the rotary speed. The default is "Rotary Speed".
        titleSuffix : str
            The second line of the title, if present.  If the titleSuffix string is blank, the second line is not added. The default is "".
        **kwargs : keyword arguments
            These arguments are passed to the plot function.

        Returns
        -------
        figure : matplotlib.figure.Figure
            The newly created figure.
        """
        figure, axeses = cls.NewParameterWobAndRotarySpeedPlot(title, data, xAxisColumn, parameterLabel, parameterColumn, wobColumn, rpmColumn, titleSuffix, **kwargs)
        LegendHelper.CreateLegendAtFigureBottom(figure, axeses[0], offset=0.15*PlotHelper.GetSettings().Scale, legendOptions=legendOptions)
        plt.show()
        return figure


    @classmethod
    def NewParameterWobAndRotarySpeedPlot(cls, title:str, data:pd.DataFrame, xAxisColumn:str, parameterLabel:str, parameterColumn:str, wobColumn:str="Weight on Bit", rpmColumn:str="Rotary Speed", titleSuffix:str=None, **kwargs):
        """
        Plots a parameter versus the weight on bit and rotary speed on a multi y-axes figure.  The parameter is read off of the left axis and the weight on bit and rotary speed
        have axes on the right side.

        This assumes all the data (parameter, WOB, and rotary speed) are in the same data frame and have been sampled at the same rate (same x-axis data).

        Parameters
        ----------
        title : str
            The first line of the title..
        data : pd.DataFrame
            The data.
        xAxisColumn : str
            The column name of the x-axis data.
        parameterLabel : str
            Left y-axis label.
        parameterColumn : str
            The column name of the parameter to plot on the left axis.
        wobColumn : str, optional
            The column name of the weight on bit. The default is "Weight on Bit".
        rpmColumn : str, optional
            The column name of the rotary speed. The default is "Rotary Speed".
        titleSuffix : str
            The second line of the title, if present.  If the titleSuffix string is blank, the second line is not added. The default is "".
        **kwargs : keyword arguments
            These arguments are passed to the plot function.

        Returns
        -------
        figure : matplotlib.figure.Figure
            The newly created figure.
        axeses : tuple of matplotlib.axes.Axes
            The axes of the plot.
        """
        yDataLabels = [[parameterColumn], [wobColumn], [rpmColumn]]
        kwargs      = DesignatedColors.ApplyKeyWordArgumentsToColors(kwargs, yDataLabels)

        convertedData, xSuffix, ySuffixes = Units.ConvertOutput(data, xAxisColumn, yDataLabels)
        figure, axeses                    = PlotMaker.NewMultiYAxesPlot(convertedData, xAxisColumn, yDataLabels, **kwargs)

        # Labels.
        xLabel  = Units.CombineLabelsAndUnits(xAxisColumn, xSuffix)
        yLabels = Units.CombineLabelsAndUnits([parameterLabel, "Weight on Bit", "Rotary Speed"], ySuffixes)
        AxesHelper.Label(axeses, title, xLabel, yLabels, titleSuffix=titleSuffix)

        return figure, axeses


    @classmethod
    def NewThreeAxesWobAndRotarySpeedFigure(cls, title:str, data:pd.DataFrame, xAxisColumn:str="Time", wobColumn:str="Weight on Bit", rpmColumn:str="Rotary Speed", titleSuffix:str=None, **kwargs):
        # Creates a figure with two axes having an aligned (shared) x-axis.
        figure, axeses = PlotHelper.NewMultiYAxesFigure(3)

        yDataLabels                       = [[wobColumn], [rpmColumn]]
        kwargs                            = DesignatedColors.ApplyKeyWordArgumentsToColors(kwargs, yDataLabels)
        convertedData, xSuffix, ySuffixes = Units.ConvertOutput(data, xAxisColumn, yDataLabels)
        PlotMaker.MultiAxesPlot(axeses[1:], convertedData, xAxisColumn, yDataLabels, "x", **kwargs)

        # Labels.
        xLabel  = Units.CombineLabelsAndUnits(xAxisColumn, xSuffix)
        yLabels = Units.CombineLabelsAndUnits(["", "Weight on Bit", "Rotary Speed"], ySuffixes)
        AxesHelper.Label(axeses, title, xLabel, yLabels, titleSuffix=titleSuffix)

        return figure, axeses


    @classmethod
    def NewCombinedAccelerationPlot(cls, data:pd.DataFrame, columns:list=["Acceleration X", "Acceleration Y", "Acceleration Z"], title:str="Accelerations", titleSuffix:str=None, **kwargs):
        PlotHelper.Format()

        kwargs            = DesignatedColors.ApplyKeyWordArgumentsToColors(kwargs, columns)
        seriesKeyWordArgs = PlotHelper.ConvertKeyWordArgumentsToSeriesSets(ListTools.GetLengthOfNestedObjects(columns), **kwargs)

        figure = plt.gcf()
        axes   = plt.gca()

        convertedData, xSuffix, ySuffixes = Units.ConvertOutput(data, "Time", columns)

        for i in range(len(columns)):
            axes.plot(convertedData["Time"], convertedData[columns[i]], label=columns[i], **(seriesKeyWordArgs[i]))

        xLabel  = Units.CombineLabelsAndUnits("Time", xSuffix)
        yLabels = Units.CombineLabelsAndUnits("Acceleration", ySuffixes[0])

        AxesHelper.Label(axes, title, xLabel, yLabels, titleSuffix=titleSuffix)

        return figure, axes


    @classmethod
    def CreateNewAccelerationPlot(cls, data:pd.DataFrame, column:str, title:str="Acceleration", titleSuffix:str=None, legendOptions:LegendOptions=LegendOptions(), **kwargs):
        figure, axes= cls.NewAccelerationPlot(data, column, title, titleSuffix, **kwargs)
        LegendHelper.CreateLegendAtFigureBottom(figure, axes, offset=0.15*PlotHelper.GetSettings().Scale, legendOptions=legendOptions)
        plt.show()
        return figure


    @classmethod
    def NewAccelerationPlot(cls, data:pd.DataFrame, column:str, title:str="Acceleration", titleSuffix:str=None, **kwargs):
        # Must be run before creating figure or plotting data.
        PlotHelper.Format()

        kwargs = DesignatedColors.ApplyKeyWordArgumentsToColors(kwargs, column)

        figure = plt.gcf()
        axes   = plt.gca()

        convertedData, xSuffix, ySuffixes = Units.ConvertOutput(data, "Time", column)

        axes.plot(convertedData["Time"], convertedData[column], label=column, **kwargs)

        xLabel  = Units.CombineLabelsAndUnits("Time", xSuffix)
        yLabels = Units.CombineLabelsAndUnits("Acceleration", ySuffixes[0])

        AxesHelper.Label(axes, title, xLabel, yLabels, titleSuffix=titleSuffix)

        return figure, axes