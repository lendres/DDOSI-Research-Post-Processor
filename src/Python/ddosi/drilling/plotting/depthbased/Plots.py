"""
Created on March 15, 2023
@author: Lance A. Endres
"""
import pandas                                                        as pd
from   lendres.plotting.AxesHelper                                   import AxesHelper
from   lendres.plotting.PlotHelper                                   import PlotHelper
from   lendres.plotting.PlotMaker                                    import PlotMaker

class Plots():


    @classmethod
    def NewWobAndRotarySpeedPlot(cls, title:str, data:pd.DataFrame, yAxisColumn:str="Depth", wobColumn:str="WOB", yUnits:str="cm", rpmColumn:str="RPM", **kwargs):
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