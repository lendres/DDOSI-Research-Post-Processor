"""
Created on September 22, 2023
@author: Lance A. Endres
"""

import pandas                                                        as pd
import numpy                                                         as np
import matplotlib.pyplot                                             as plt
import os

from   ddosi.plotting.DesignatedColors                               import DesignatedColors

from   lendres.plotting.AxesHelper                                   import AxesHelper
from   lendres.plotting.PlotHelper                                   import PlotHelper
from   lendres.plotting.PlotMaker                                    import PlotMaker
from   lendres.demonstration.FunctionGenerator                       import FunctionGenerator

import unittest


class TestDesignatedColors(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dataFrame = FunctionGenerator.GetMultipleSineWaveDataFrame()
        cls.dataFrame.rename(
            {
                "y0" : "Category C",
                "y1" : "Category B"
            },
            axis="columns",
            inplace=True
        )

        cls.sinX, cls.sinA = FunctionGenerator.GetSineWave(magnitude=10, frequency=4, yOffset=0, slope=0, steps=1000)
        cls.sinX, cls.sinB = FunctionGenerator.GetSineWave(magnitude=4, frequency=2, yOffset=0, slope=10, steps=1000)
        cls.sinX, cls.sinC = FunctionGenerator.GetSineWave(magnitude=5, frequency=3, yOffset=30, slope=-5, steps=1000)
        
        # Designated colors setup.
        file = os.path.join(os.path.dirname(__file__), "Colors.xlsx")
        DesignatedColors.Initialize(file)


    def setUp(self):
        pass


    def testPlotOrderInvariance(self):
        # Show that order plotted doesn't change the colors.
        self.Plot(self.sinX, [self.sinA, self.sinB, self.sinC], ["Category A", "Category C", "Doesn't Exist"])
        self.Plot(self.sinX, [self.sinC, self.sinB, self.sinA], ["Doesn't Exist", "Category C", "Category A"])
        
        
    def Plot(self, xData, yData, yDataLabels):
        # Must be run before creating figure or plotting data.
        PlotHelper.Format()

        axes   = plt.gca()

        colors = DesignatedColors.GetColors(yDataLabels)

        for y, label, color in zip(yData, yDataLabels, colors):
            axes.plot(xData, y, label=label, color=color)
        axes.set(title="Plott Order Invariance")
        axes.legend(loc="upper right")
        plt.show()


    def testMultipleAxeses(self):
        yDataLabels = [["Category C"], ["Category B", "y2"], ["y3"]]
        
        self.PlotMultipleAxeses("No Key Word Arguments", yDataLabels)

        colors = DesignatedColors.GetColors(yDataLabels)
        self.PlotMultipleAxeses("Designated Colors", yDataLabels, color=colors)


    def PlotMultipleAxeses(self, titleSuffix, yDataLabels, **kwargs):
        figure, axeses = PlotMaker.NewMultiYAxesPlot(self.dataFrame, "x", yDataLabels, **kwargs)

        # The AxesHelper can automatically label the axes if you supply it a list of strings for the y labels.
        AxesHelper.Label(axeses, title="Multiple Y Axis Plot\n"+titleSuffix, xLabel="Time", yLabels=["Left", "Right 1", "Right 2"])
        figure.legend(loc="upper left", bbox_to_anchor=(0, -0.15), ncol=2, bbox_transform=axeses[0].transAxes)
        plt.show()


    def testKeyWordArguments(self):
        yDataLabels = [["Category C"], ["Category B", "y2"], ["y3"]]
        self.PlotAutoColor("No Key Word Arguments", yDataLabels)
        
        self.PlotAutoColor("Color Key Word Arguments", yDataLabels, color=["r", "g", "b", "y"])
        self.PlotAutoColor("Multiple Key Word Arguments", yDataLabels, color=["r", "g", "b", "y"], linewidth=5)

        
    def PlotAutoColor(self, titleSuffix, yDataLabels, **kwargs):
        kwargs = DesignatedColors.ApplyKeyWordArgumentsToColors(kwargs, yDataLabels)
        
        figure, axeses = PlotMaker.NewMultiYAxesPlot(self.dataFrame, "x", yDataLabels, **kwargs)

        # The AxesHelper can automatically label the axes if you supply it a list of strings for the y labels.
        AxesHelper.Label(axeses, title="Plot using Designated Colors by Default\n"+titleSuffix, xLabel="Time", yLabels=["Left", "Right 1", "Right 2"])
        figure.legend(loc="upper left", bbox_to_anchor=(0, -0.15), ncol=2, bbox_transform=axeses[0].transAxes)
        plt.show()


if __name__ == "__main__":
    unittest.main()