"""
Created on January 31, 2024
@author: Lance A. Endres
"""
import pandas                                                        as pd
import matplotlib.pyplot                                             as plt
import os

from   lendres.demonstration.FunctionGenerator                       import FunctionGenerator
from   lendres.plotting.PlotHelper                                   import PlotHelper

from   ddosi.units.Units                                             import Units

# from   pint                                                          import UnitRegistry
# import pint_pandas

import unittest


class testUnits(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pd.set_option("display.max_columns", None)
        pd.set_option("display.precision", 4)

        cls.xAxisColumn  = "time"
        cls.yAxisColumns = ["displacement", "velocity", "acceleration"]

        Units.Initialize("SI")


    def setUp(self):
        """
        Set up function that runs before each test.
        """
        self.dataFrame = FunctionGenerator.GetDisplacementVelocityAccelerationDataFrame()

        units      = ["s", "m", "m/s", "m/s^2"]
        unitsTypes = ["time", "length", "velocity", "acceleration"]

        self.dataFrame = Units.AddUnitsToDataFrame(self.dataFrame, units, unitsTypes)

        # print("\n\n")
        # print(self.dataFrame.head())
        # print(self.dataFrame.dtypes)


    #@unittest.skip
    def testCreatePlot(self):
        """
        Plot the original data.
        """
        self.CreatePlot(self.dataFrame, "Original")


    def testCsvReadWrite(self):
        """
        Test reading and writing units data.
        """
        path = os.path.join(os.path.dirname(__file__), "test_file.csv")
        Units.ToCsv(self.dataFrame, path)

        dataFrame = Units.FromCsv(path)
        self.CreatePlot(dataFrame, "After Reading From File")

        Units.Initialize("US")
        self.CreatePlot(dataFrame, "Converted to US from File")


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