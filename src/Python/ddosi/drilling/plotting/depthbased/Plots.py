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

from   ddosi.plotting.DesignatedColors                               import DesignatedColors


class Plots():

    
    @classmethod
    def CreateWobAndRotarySpeedPlot(cls, data:pd.DataFrame, yAxisColumn:str="Depth", yUnits:str="cm", wobColumn:str="Weight on Bit", rpmColumn:str="Rotary Speed", title:str="Weight on Bit and Rotary Speed", titleSuffix:str=None, legendOptions:LegendOptions=LegendOptions(), **kwargs):
        figure, axeses = cls.NewWobAndRotarySpeedPlot(data, yAxisColumn, wobColumn, yUnits, rpmColumn, title, titleSuffix, **kwargs)
        LegendHelper.CreateLegendAtFigureBottom(figure, axeses[0], offset=0.02*PlotHelper.scale, legendOptions=legendOptions)
        plt.show()
        return figure, axeses


    @classmethod
    def NewWobAndRotarySpeedPlot(cls, data:pd.DataFrame, yAxisColumn:str="Depth", wobColumn:str="Weight on Bit", yUnits:str="cm", rpmColumn:str="Rotary Speed", title:str="Weight on Bit and Rotary Speed", titleSuffix:str=None, **kwargs):
        PlotHelper.scale      = 0.4
        PlotHelper.widthScale = 0.35
        
        yDataLabels    = [[wobColumn], [rpmColumn]]
        kwargs         = DesignatedColors.ApplyKeyWordArgumentsToColors(kwargs, yDataLabels)
        figure, axeses = PlotMaker.NewMultiXAxesPlot(data, yAxisColumn, yDataLabels, **kwargs)

        # Labels.
        AxesHelper.Label(axeses, title, ["Weight on Bit (tons)", "Revolutions per Minute"], yAxisColumn+" ("+yUnits+")", titleSuffix=titleSuffix)
        AxesHelper.ReverseYAxisLimits(axeses[0])

        PlotHelper.scale      = 0.8
        PlotHelper.widthScale = 1.0

        return figure, axeses