"""
Created on March 15, 2023
@author: Lance A. Endres
"""
import pandas                                                             as pd
import matplotlib.pyplot                                                  as plt

from   lendres.plotting.AxesHelper                                        import AxesHelper
from   lendres.plotting.PlotHelper                                        import PlotHelper
from   lendres.plotting.PlotMaker                                         import PlotMaker
from   lendres.algorithms.DataType                                        import DataType

from   ddosi.plotting.DesignatedColors                                    import DesignatedColors


class Plots():


    @classmethod
    def NewWobAndRotarySpeedPlot(cls, data:pd.DataFrame, xAxisColumn:str="Time", wobColumn:str="Weight on Bit", rpmColumn:str="Rotary Speed", title:str="Weight on Bit and Rotary Speed", titleSuffix:str=None, **kwargs):
        yDataLabels = [[wobColumn], [rpmColumn]]
        kwargs      = DesignatedColors.ApplyKeyWordArgumentsToColors(kwargs, yDataLabels)

        figure, axeses = PlotMaker.NewMultiYAxesPlot(data, xAxisColumn, yDataLabels, **kwargs)

        # Title and labels.
        AxesHelper.Label(axeses, title, xAxisColumn+" (s)", ["Weight on Bit (tons)", "Rotary Speed (RPM)"], titleSuffix=titleSuffix)

        return figure, axeses


    @classmethod
    def NewTobWobAndRpmPlot(cls, data:pd.DataFrame, xAxisColumn:str="Time", tobColumn:str="TOB", wobColumn:str="Weight on Bit", rpmColumn:str="Rotary Speed", title:str="Torque", titleSuffix:str=None, **kwargs):
        return cls.NewParameterWobAndRotarySpeedPlot(title, data, xAxisColumn, "Torque (daN.m)", tobColumn, wobColumn, rpmColumn, titleSuffix, **kwargs)


    @classmethod
    def NewRopWobAndRotarySpeedPlot(cls, data:pd.DataFrame, xAxisColumn:str="Time", ropColumn:str="ROP", wobColumn:str="Weight on Bit", rpmColumn:str="Rotary Speed", title:str="Rate of Penetration", titleSuffix:str=None, **kwargs):
        return cls.NewParameterWobAndRotarySpeedPlot(title, data, xAxisColumn, "Rate of Penetration (cm/s)", ropColumn, wobColumn, rpmColumn, titleSuffix, **kwargs)


    @classmethod
    def NewDepthOfCutWobAndRotarySpeedPlot(cls, data:pd.DataFrame, xAxisColumn:str="Time", depthOfCutColumn:str="Depth of Cut", wobColumn:str="Weight on Bit", rpmColumn:str="Rotary Speed", title:str="Depth of Cut", titleSuffix:str=None, **kwargs):
        return cls.NewParameterWobAndRotarySpeedPlot(title, data, xAxisColumn, "Depth of Cut (cm/revolution)", depthOfCutColumn, wobColumn, rpmColumn, titleSuffix, **kwargs)


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

        figure, axeses = PlotMaker.NewMultiYAxesPlot(data, xAxisColumn, yDataLabels, **kwargs)

        # Labels.
        AxesHelper.Label(axeses, title, "Time (s)", [parameterLabel, "Weight on Bit (tons)", "Rotary Speed (RPM)"], titleSuffix=titleSuffix)

        return figure, axeses


    @classmethod
    def NewThreeAxesWobAndRotarySpeedFigure(cls, title:str, data:pd.DataFrame, xAxisColumn:str="Time", wobColumn:str="Weight on Bit", rpmColumn:str="Rotary Speed", titleSuffix:str=None, **kwargs):
        # Creates a figure with two axes having an aligned (shared) x-axis.
        figure, axeses = PlotHelper.NewMultiYAxesFigure(3)

        yDataLabels = [[wobColumn], [rpmColumn]]
        kwargs      = DesignatedColors.ApplyKeyWordArgumentsToColors(kwargs, yDataLabels)
        PlotMaker.MultiAxesPlot(axeses[1:], data, xAxisColumn, yDataLabels, "x", **kwargs)

        # Labels.
        AxesHelper.Label(axeses, title, "Time (s)", ["", "Weight on Bit (tons)", "Rotary Speed (RPM)"], titleSuffix=titleSuffix)

        return figure, axeses


    @classmethod
    def NewCombinedAccelerationPlot(cls, data:pd.DataFrame, columns:list=["Acceleration X", "Acceleration Y", "Acceleration Z"], title:str="Accelerations", titleSuffix:str=None, **kwargs):
        PlotHelper.Format()

        kwargs            = DesignatedColors.ApplyKeyWordArgumentsToColors(kwargs, columns)
        seriesKeyWordArgs = PlotHelper.ConvertKeyWordArgumentsToSeriesSets(DataType.GetLengthOfNestedObjects(columns), **kwargs)

        figure = plt.gcf()
        axes   = plt.gca()

        for i in range(len(columns)):
            axes.plot(data["Time"], data[columns[i]], label=columns[i], **(seriesKeyWordArgs[i]))

        AxesHelper.Label(axes, title, "Time (s)", "Acceleration (m/s^2)", titleSuffix=titleSuffix)

        return figure, axes


    @classmethod
    def NewAccelerationPlot(cls, data:pd.DataFrame, column:str, title:str="Acceleration", titleSuffix:str=None, **kwargs):
        # Must be run before creating figure or plotting data.
        PlotHelper.Format()

        kwargs = DesignatedColors.ApplyKeyWordArgumentsToColors(kwargs, column)

        figure = plt.gcf()
        axes   = plt.gca()

        axes.plot(data["Time"], data[column], label=column, **kwargs)
        AxesHelper.Label(axes, title, "Time (s)", "Acceleration (m/s^2)", titleSuffix=titleSuffix)

        return figure, axes