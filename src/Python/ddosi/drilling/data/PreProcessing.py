"""
Created on March 15, 2023
@author: Lance A. Endres
"""
import numpy                                               as np

class PreProcessing():

    @classmethod
    def CalculateRopFromTimeAndDepth(cls, data, timeColumn="Time", depthColumn="Depth"):
        """
        Calculates the rate of penetration from the time and depth.

        Parameters
        ----------
        data : pandas.DataFrame
            Data in a pandas.DataFrame
        timeColumn : string, optional
            The column name of the time data. The default is "Time".
        depthColumn : string, optional
            The column name of the depth data. The default is "Depth".

        Returns
        -------
        None.

        """
        rateOfPenetration = data[depthColumn].diff() / data[timeColumn].diff()

        # To calculate ROP, we need intervals of distance and time so we end up with one less entry for the ROP
        # than either of those data sets and Pandas fills this in with nan.  The first entry is back filled with the
        # same value as the second entry to make them the same length.  Repeating an entry is better than adding a
        # zero because plots that use a starting value of zero create a big spike and look funny.
        rateOfPenetration[0] = rateOfPenetration[1]

        data["ROP"] = rateOfPenetration


    @classmethod
    def CalculateDepthOfCutFromRopAndRotarySpeed(cls, data, ropColumn="ROP", rpmColumn="Rotary Speed"):
        """
        Calculates the depth of cut from the rate of penetration and revolutions per minute.

        Parameters
        ----------
        data : pandas.DataFrame
            Data in a pandas.DataFrame
        ropColumn : string, optional
            The column name of the rate of penetration data. The default is "ROP".
        rpmColumn : string, optional
            The column name of the angular velocity data. The default is "Rotary Speed".

        Returns
        -------
        None.
        """
        revolutionsPerSecond = data[rpmColumn] / 60.0
        data["Depth of Cut"] = data[ropColumn] / revolutionsPerSecond
        data["Depth of Cut"].replace([np.inf, -np.inf], 0, inplace=True)