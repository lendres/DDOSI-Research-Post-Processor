"""
Created on March 15, 2023
@author: Lance A. Endres
"""
import pandas                                                        as pd
from   lendres.plotting.AxesHelper                                   import AxesHelper
from   lendres.plotting.PlotHelper                                   import PlotHelper
from   lendres.plotting.PlotMaker                                    import PlotMaker

from   ddosi.plotting.DesignatedColors                               import DesignatedColors


class Plots():


    @classmethod
    def NewWobAndRotarySpeedPlot(cls, data:pd.DataFrame, yAxisColumn:str="Depth", wobColumn:str="Weight on Bit", yUnits:str="cm", rpmColumn:str="Rotary Speed", title:str="Weight on Bit and Rotary Speed", titleSuffix:str=None, **kwargs):
        PlotHelper.scale      = 0.4
        PlotHelper.widthScale = 0.35
        
        yDataLabels = [[wobColumn], [rpmColumn]]
        kwargs      = DesignatedColors.ApplyKeyWordArgumentsToColors(kwargs, yDataLabels)
        figure, axes = PlotMaker.NewMultiXAxesPlot(data, yAxisColumn, yDataLabels, **kwargs)

        # Labels.
        AxesHelper.Label(axes[0], title, "Weight on Bit (tons)", yAxisColumn+" ("+yUnits+")", titleSuffix=titleSuffix)
        AxesHelper.ReverseYAxisLimits(axes[0])
        axes[1].set_xlabel("Revolutions per Minute")

        PlotHelper.scale      = 0.8
        PlotHelper.widthScale = 1.0

        return figure, axes