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

        data["Rate of Penetration"]                    = rateOfPenetration
        data["Rate of Penetration"].attrs["unitstype"] = "penetration rate"


    @classmethod
    def CalculateDepthOfCutFromRopAndRotarySpeed(cls, data, ropColumn="Rate of Penetration", rpmColumn="Rotary Speed"):
        """
        Calculates the depth of cut from the rate of penetration and rotary speed.

        Parameters
        ----------
        data : pandas.DataFrame
            Data in a pandas.DataFrame
        ropColumn : string, optional
            The column name of the rate of penetration data. The default is "Rate of Penetration".
        rpmColumn : string, optional
            The column name of the angular velocity data. The default is "Rotary Speed".

        Returns
        -------
        None.
        """
        revolutionsPerSecond = data[rpmColumn].pint.to("revolutions_per_second")
        data["Depth of Cut"] = data[ropColumn].pint.to("meter_per_second") / revolutionsPerSecond
        data["Depth of Cut"].replace([np.inf, -np.inf], 0, inplace=True)
        data["Depth of Cut"].attrs["unitstype"] = "spiral rate"