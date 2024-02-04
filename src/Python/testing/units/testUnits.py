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

# from   pint                                                          import UnitRegistry
# import pint_pandas

import unittest


class testUnits(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # ureg = UnitRegistry()
        # ureg.default_format = ".3fP"

        pd.reset_option("all")
        pd.set_option("display.max_columns", None)
        pd.set_option("display.precision", 4)

        cls.xAxisColumn  = "time"
        cls.yAxisColumns = ["displacement", "velocity", "acceleration"]

        Units.Initialize("European")


    def setUp(self):
        """
        Set up function that runs before each test.
        """
        self.dataFrame = FunctionGenerator.GetDisplacementVelocityAccelerationDataFrame()
        print(self.dataFrame.head())

        unitsForHeaderInsert   = ["s", "m", "m/s", "m/s^2"]
        self.dataFrame.columns = pd.MultiIndex.from_tuples(list(zip(self.dataFrame.columns, unitsForHeaderInsert)))
        self.dataFrame         = self.dataFrame.pint.quantify(level=-1)

        unitsTypes             = ["time", "length", "velocity", "acceleration"]

        for column, unitType in zip(self.dataFrame, unitsTypes):
            self.dataFrame[column].attrs["unitstype"] = unitType

        print("\n\n")
        print(self.dataFrame.dtypes)


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

        convertedData, xSuffix, ySuffixes = Units.ConvertOutput(dataFrame, cls.xAxisColumn, cls.yAxisColumns)
        for column in cls.yAxisColumns:
            axes.plot(
                convertedData["time"],
                convertedData[column],
                label=column.title()
            )

        axes.set(title=title, xlabel="Time", ylabel="Value")
        plt.legend(loc="upper left")

        plt.show()


if __name__ == "__main__":
    unittest.main()