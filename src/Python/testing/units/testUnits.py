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

        self.units      = ["s", "m", "m/s", "m/s^2"]
        self.unitTypes = ["time", "length", "velocity", "acceleration"]

        self.dataFrame = Units.AddUnitsToDataFrame(self.dataFrame, self.units, self.unitTypes)

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


    def testGetTypes(self):
        """
        Test getting the unit types.
        """
        result = Units.GetUnitTypes(self.dataFrame)
        self.assertListEqual(result, self.unitTypes)


    def testAttributes(self):
        series = pd.Series([1, 2, 3, 4])
        series.attrs["unittypes"] = "time"

        seriesNew = series + 5

        dataFrame = pd.DataFrame([series, seriesNew]).T

        print("\n\nSeries attributes:")
        print(series.attrs)
        print(seriesNew.attrs)
        print(Units.GetUnitTypes(dataFrame))

        print("\n\nSeries:")
        print(series)
        print("")
        print(seriesNew)

        print("\n\nDataFrame:")
        print(dataFrame)
        print(Units.GetUnitTypes(dataFrame))


    def testAttrsDataFrame(self):
        df = pd.DataFrame(dict(column1=[1,2,3,4], column2=[1,2,3,4]))
        df.attrs['name'] = "hello"
        print(df)
        print(df.attrs)

        df1 = df.astype(float)
        print(df1)
        print(df1.attrs)

        df2 = df.astype({'column1':float})
        print(df2)
        print(df2.attrs)


    def testAttrsSeries(self):
        df = pd.DataFrame(dict(column1=[1,2,3,4], column2=[1,2,3,4]))
        df["column1"].attrs['name'] = 'hello'
        print(df)
        print(df.attrs)
        print(df["column1"].attrs)

        df1 = df.astype(float)
        print(df1)
        print(df1["column1"].attrs)

        df2 = df.astype({'column1':float})
        print(df2)
        print(df2["column1"].attrs)


    def testPintPandas(self):
        """
        Test Pint Pandas features.
        """
        addTime = 5 * Units.GetUnitRegistry().second
        # print("\nTime:", addTime)
        # print("Time type:", type(addTime))
        # print("\nSeries type:", type(self.dataFrame["time"]))
        # print("\nSeries data type:", type(self.dataFrame["time"].dtype))
        print("\nBefore:")
        print(Units.GetUnitTypes(self.dataFrame))
        newTime = self.dataFrame["time"] + addTime
        print("\nAfter:")
        print(Units.GetUnitTypes(self.dataFrame))
        print(Units.GetUnitTypes(newTime))

        print("\nAfter assignment:")
        self.dataFrame["time"] = newTime
        print(Units.GetUnitTypes(self.dataFrame))
        print(Units.GetUnitTypes(newTime))


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