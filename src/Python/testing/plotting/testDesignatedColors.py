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

        # This function is a short cut for creating multiple Y axis plots.
        cls.yDataLabels = [["Category C"], ["Category B", "y2"], ["y3"]]
        
        # Designated colors setup.
        file = os.path.join(os.path.dirname(__file__), "Colors.xlsx")
        DesignatedColors.Initialize(file)


    def setUp(self):
        pass


    def testData(self):
        pass
        # print(self.colors.head())


    def testPlot(self):
        x, a = FunctionGenerator.GetSineWave(magnitude=10, frequency=4, yOffset=0, slope=0, steps=1000)
        x, b = FunctionGenerator.GetSineWave(magnitude=4, frequency=2, yOffset=0, slope=10, steps=1000)
        x, c = FunctionGenerator.GetSineWave(magnitude=5, frequency=3, yOffset=30, slope=-5, steps=1000)

        # Show that order plotted doesn't change the colors.
        self.Plot(x, [a, b, c], ["Category A", "Category C", "Doesn't Exist"])
        self.Plot(x, [c, b, a], ["Doesn't Exist", "Category C", "Category A"])


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
        self.PlotMultipleAxeses("No Key Word Arguments")

        colors = DesignatedColors.GetColors(self.yDataLabels)
        self.PlotMultipleAxeses("Designated Colors", color=colors)


    def PlotMultipleAxeses(self, titleSuffix, **kwargs):
        figure, axeses = PlotMaker.NewMultiYAxesPlot(self.dataFrame, "x", self.yDataLabels, **kwargs)

        # The AxesHelper can automatically label the axes if you supply it a list of strings for the y labels.
        AxesHelper.Label(axeses, title="Multiple Y Axis Plot\n"+titleSuffix, xLabel="Time", yLabels=["Left", "Right 1", "Right 2"])
        figure.legend(loc="upper left", bbox_to_anchor=(0, -0.15), ncol=2, bbox_transform=axeses[0].transAxes)
        plt.show()


if __name__ == "__main__":
    unittest.main()