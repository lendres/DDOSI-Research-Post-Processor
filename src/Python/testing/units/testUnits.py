"""
Created on January 31, 2024
@author: Lance A. Endres
"""
import numpy                                                         as np
import pandas                                                        as pd
import matplotlib.pyplot                                             as plt
from   matplotlib                                                    import mlab

from   lendres.demonstration.FunctionGenerator                       import FunctionGenerator
from   lendres.plotting.PlotHelper                                   import PlotHelper

from   ddosi.units.Units                                             import Units

import unittest


class testUnits(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass


    def setUp(self):
        """
        Set up function that runs before each test.
        """
        self.dataFrame = FunctionGenerator.GetDisplacementVelocityAccelerationDataFrame()

        unitsForHeaderInsert   = ["m/s", "m/s", "m/s^2"]
        self.dataFrame.columns = pd.MultiIndex.from_tuples(list(zip(self.dataFrame.columns, unitsForHeaderInsert)))
        self.accelerationData  = self.accelerationData.pint.quantify(level=-1)

        accelerationTypes      = ["length", "velocity", "acceleration"]

        for column, unitType in zip(self.accelerationData, accelerationTypes):
            self.accelerationData[column].attrs["unitstype"] = unitType


    #@unittest.skip
    def testCreatePlot(self):
        self.CreatePlot(self.dataFrame, "Original")


    def testCsvReadWrite(self):
        pass


    @classmethod
    def CreatePlot(cls, dataFrame, title):
        """
        An example plot that is a simple sine wave.

        Parameters
        ----------
        title : string
            Title to use for the plot.

        Returns
        -------
        None.
        """
        # PlotHelper.Format()

        axes = plt.gca()

        axes.plot(dataFrame["time"], dataFrame["displacement"], label="Displacement")
        axes.plot(dataFrame["time"], dataFrame["velocity"],     label="Velocity")
        axes.plot(dataFrame["time"], dataFrame["acceleration"], label="Acceleration")

        axes.set(title=title, xlabel="Time", ylabel="Value")
        plt.legend(loc="upper left")

        plt.show()


if __name__ == "__main__":
    unittest.main()