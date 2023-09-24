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
        pass


    def setUp(self):
        file                  = os.path.join(os.path.dirname(__file__), "Colors.xlsx")
        DesignatedColors.Initialize(file)


    def testData(self):
        pass
        # print(self.colors.head())


    def testPlot(self):
        x, a = FunctionGenerator.GetSineWave(magnitude=10, frequency=4, yOffset=0, slope=0, steps=1000)
        x, b = FunctionGenerator.GetSineWave(magnitude=4, frequency=2, yOffset=0, slope=10, steps=1000)
        x, c = FunctionGenerator.GetSineWave(magnitude=5, frequency=3, yOffset=30, slope=-5, steps=1000)

        # Show that order plotted doesn't change the colors.
        self.Plot(x, [a, b, c], ["Category A", "Category C", "Doesn't Exist"])
        self.Plot(x, [b, a, c], ["Category C", "Category A", "Doesn't Exist"])


    def Plot(self, xData, yData, yDataLabels):
        # Must be run before creating figure or plotting data.
        PlotHelper.Format()

        figure = plt.gcf()
        axes   = plt.gca()

        colors = DesignatedColors.GetColors(yDataLabels)

        for y, label, color in zip(yData, yDataLabels, colors):
            axes.plot(xData, y, label=label, color=color)
        figure.legend()
        plt.show()


    def testMultipleAxeses(self):
        dataFrame = FunctionGenerator.GetMultipleSineWaveDataFrame()
        dataFrame.rename({
            "y0" : "Category C",
            "y1" : "Category B"
        })

        # This function is a short cut for creating multiple Y axis plots.
        yDataLabels = [["Category C"], ["Category B", "y2"], ["y3"]]
        colors      = DesignatedColors.GetColors(yDataLabels)
        print("Colors:", colors)
        figure, axeses = PlotMaker.NewMultiYAxesPlot(dataFrame, "x", yDataLabels, color=colors)

        # The AxesHelper can automatically label the axes if you supply it a list of strings for the y labels.
        AxesHelper.Label(axeses, title="Multiple Y Axis Plot", xLabel="Time", yLabels=["Left", "Right 1", "Right 2"])


if __name__ == "__main__":
    unittest.main()