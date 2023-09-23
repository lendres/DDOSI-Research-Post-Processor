"""
Created on September 22, 2023
@author: Lance A. Endres
"""

import pandas                                                        as pd
import numpy                                                         as np
import matplotlib.pyplot                                             as plt

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
        self.designatedColors = DesignatedColors()


    def testData(self):
        pass
        # print(self.colors.head())


    def testPlot(self):
        x, weight = FunctionGenerator.GetSineWave(magnitude=10, frequency=4, yOffset=0, slope=0, steps=1000)
        x, torque = FunctionGenerator.GetSineWave(magnitude=4, frequency=2, yOffset=0, slope=10, steps=1000)

        self.Plot(x, [weight, torque], ["Weight on Bit", "Torque"])


    def Plot(self, xData, yData, yDataLabels):
        # Must be run before creating figure or plotting data.
        PlotHelper.Format()

        figure = plt.gcf()
        axes   = plt.gca()

        for y, label, column in zip(yData, yDataLabels, ["Weight on Bit", "Acceleration Z"]):
            axes.plot(xData, y, label=label, color=self.designatedColors.colors.loc[column, 0])
            # axes.plot(xData, y, label=label, color=self.designatedColors.colors.loc[0, column])
            # axes.plot(xData, y, label=label, color=(76, 114, 176))


        plt.show()


if __name__ == "__main__":
    unittest.main()