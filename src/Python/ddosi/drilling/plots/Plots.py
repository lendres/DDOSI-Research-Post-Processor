"""
Created on March 15, 2023
@author: Lance A. Endres
"""
import pandas                                                        as pd
from   lendres.plotting.PlotHelper                                   import PlotHelper
from   lendres.plotting.PlotMaker                                    import PlotMaker
from   lendres.plotting.AxesHelper                                   import AxesHelper

class Plots():


    @classmethod
    def NewWobAndRpmPlot(cls, title:str, data:pd.DataFrame, xAxisColumn:str="Time", wobColumn:str="WOB", xUnits:str="s", rpmColumn:str="RPM", **kwargs):
        figure, axes = PlotMaker.NewMultiYAxesPlot(data, xAxisColumn, [[wobColumn], [rpmColumn]], **kwargs)

        # Labels.
        AxesHelper.Label(axes[0], title, xAxisColumn+" ("+xUnits+")", "Weight on Bit (tons)")
        axes[1].set_ylabel("Revolutions per Minute")

        return figure, axes


    @classmethod
    def NewDepthBasedWobAndRpmPlot(cls, title:str, data:pd.DataFrame, yAxisColumn:str="Depth", wobColumn:str="WOB", yUnits:str="cm", rpmColumn:str="RPM", **kwargs):
        PlotHelper.scale      = 0.4
        PlotHelper.widthScale = 0.35
        figure, axes = PlotMaker.NewMultiXAxesPlot(data, yAxisColumn, [[wobColumn], [rpmColumn]], **kwargs)

        # Labels.
        AxesHelper.Label(axes[0], title, "Weight on Bit (tons)", yAxisColumn+" ("+yUnits+")")
        AxesHelper.ReverseYAxisLimits(axes[0])
        axes[1].set_xlabel("Revolutions per Minute")

        PlotHelper.scale      = 0.8
        PlotHelper.widthScale = 1.0

        return figure, axes


    @classmethod
    def NewTobWobAndRpmPlot(cls, title:str, data:pd.DataFrame, xAxisColumn:str="Time", tobColumn:str="TOB", wobColumn:str="WOB", rpmColumn:str="RPM", **kwargs):
        return cls.NewParameterVersusWobAndRpmPlot(title, data, xAxisColumn, "Torque (daN.m)", tobColumn, wobColumn, rpmColumn, **kwargs)


    @classmethod
    def NewRopWobAndRpmPlot(cls, title:str, data:pd.DataFrame, xAxisColumn:str="Time", ropColumn:str="ROP", wobColumn:str="WOB", rpmColumn:str="RPM", **kwargs):
        return cls.NewParameterVersusWobAndRpmPlot(title, data, xAxisColumn, "Rate of Penetration (cm/s)", ropColumn, wobColumn, rpmColumn, **kwargs)


    @classmethod
    def NewDepthOfCutWobAndRpmPlot(cls, title:str, data:pd.DataFrame, xAxisColumn:str="Time", depthOfCutColumn:str="Depth of Cut", wobColumn:str="WOB", rpmColumn:str="RPM", **kwargs):
        return cls.NewParameterVersusWobAndRpmPlot(title, data, xAxisColumn, "Depth of Cut (cm/revolution)", depthOfCutColumn, wobColumn, rpmColumn, **kwargs)


    @classmethod
    def NewParameterVersusWobAndRpmPlot(cls, title:str, data:pd.DataFrame, xAxisColumn:str, parameterLabel:str, parameterColumn:str, wobColumn:str="WOB", rpmColumn:str="RPM", **kwargs):
        figure, axes = PlotMaker.NewMultiYAxesPlot(data, xAxisColumn, [[parameterColumn], [wobColumn], [rpmColumn]], **kwargs)

        # Labels.
        AxesHelper.Label(axes[0], title, "Time (s)", parameterLabel)
        axes[1].set_ylabel("Weight on Bit (tons)")
        axes[2].set_ylabel("Revolutions per Minute")

        return figure, axes