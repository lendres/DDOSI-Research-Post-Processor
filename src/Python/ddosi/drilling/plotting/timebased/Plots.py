"""
Created on March 15, 2023
@author: Lance A. Endres
"""
import pandas                                                        as pd
import matplotlib.pyplot                                             as plt
from   lendres.plotting.AxesHelper                                   import AxesHelper
from   lendres.plotting.PlotHelper                                   import PlotHelper
from   lendres.plotting.PlotMaker                                    import PlotMaker


class Plots():


    @classmethod
    def NewWobAndRotarySpeedPlot(cls, titleSuffix:str, data:pd.DataFrame, xAxisColumn:str="Time", wobColumn:str="WOB", rpmColumn:str="RPM", **kwargs):
        figure, axes = PlotMaker.NewMultiYAxesPlot(data, xAxisColumn, [[wobColumn], [rpmColumn]], **kwargs)

        # Title and labels.
        title = "Weight on Bit and Rotary Speed\n" + titleSuffix
        AxesHelper.Label(axes[0], title, xAxisColumn+" (s)", "Weight on Bit (tons)")
        axes[1].set_ylabel("Rotary Speed (RPM)")

        return figure, axes


    @classmethod
    def NewTobWobAndRpmPlot(cls, titleSuffix:str, data:pd.DataFrame, xAxisColumn:str="Time", tobColumn:str="TOB", wobColumn:str="WOB", rpmColumn:str="RPM", **kwargs):
        title = "Torque\n" + titleSuffix
        return cls.NewParameterWobAndRpmPlot(title, data, xAxisColumn, "Torque (daN.m)", tobColumn, wobColumn, rpmColumn, **kwargs)


    @classmethod
    def NewRopWobAndRpmPlot(cls, titleSuffix:str, data:pd.DataFrame, xAxisColumn:str="Time", ropColumn:str="ROP", wobColumn:str="WOB", rpmColumn:str="RPM", **kwargs):
        title = "Rate of Penetration\n" + titleSuffix
        return cls.NewParameterWobAndRpmPlot(title, data, xAxisColumn, "Rate of Penetration (cm/s)", ropColumn, wobColumn, rpmColumn, **kwargs)


    @classmethod
    def NewDepthOfCutWobAndRpmPlot(cls, titleSuffix:str, data:pd.DataFrame, xAxisColumn:str="Time", depthOfCutColumn:str="Depth of Cut", wobColumn:str="WOB", rpmColumn:str="RPM", **kwargs):
        title = "Depth of Cut\n" + titleSuffix
        return cls.NewParameterWobAndRpmPlot(title, data, xAxisColumn, "Depth of Cut (cm/revolution)", depthOfCutColumn, wobColumn, rpmColumn, **kwargs)


    @classmethod
    def NewParameterWobAndRpmPlot(cls, title:str, data:pd.DataFrame, xAxisColumn:str, parameterLabel:str, parameterColumn:str, wobColumn:str="WOB", rpmColumn:str="RPM", **kwargs):
        figure, axes = PlotMaker.NewMultiYAxesPlot(data, xAxisColumn, [[parameterColumn], [wobColumn], [rpmColumn]], **kwargs)

        # Labels.
        AxesHelper.Label(axes[0], title, "Time (s)", parameterLabel)
        axes[1].set_ylabel("Weight on Bit (tons)")
        axes[2].set_ylabel("Rotary Speed (RPM)")

        return figure, axes


    @classmethod
    def NewCombinedAccelerationPlot(cls, titleSuffix:str, data:pd.DataFrame, columns:list=["Acceleration X", "Acceleration Y", "Acceleration Z"], **kwargs):
        PlotHelper.Format()
        axes = plt.gca()

        for i in range(len(columns)):
            axes.plot(data["Time"], data[columns[i]], label=columns[i], color=PlotHelper.NextColor(), **kwargs)

        AxesHelper.Label(axes, "Accelerations\n"+titleSuffix, "Time (s)", "Acceleration (m/s^2)")

        return plt.gcf(), axes


    @classmethod
    def NewAccelerationPlot(cls, titleSuffix:str, data:pd.DataFrame, column:str, colorIndex=0, **kwargs):
        # Must be run before creating figure or plotting data.
        PlotHelper.Format()

        axes = plt.gca()
        axes.plot(data["Time"], data[column], label=column, color=PlotHelper.GetColor(colorIndex), **kwargs)

        AxesHelper.Label(axes, "Accelerations\n"+titleSuffix, "Time (s)", "Acceleration (m/s^2)")

        return plt.gcf(), axes