"""
Created on March 21, 2023
@author: Lance A. Endres
"""
class Math():

    @classmethod
    def PercentDifference(cls, value1, value2):
        return abs(value1 - value2) / (0.5 * (value1 + value2)) * 100


    @classmethod
    def NormalizedDifference(cls, value1, value2):
        """
        Difference between two values expressed in a range from 0 to 1.  The percent
        difference divided by 100.

        Parameters
        ----------
        value1 : int, float, array like.
            The first value(s).
        value2 : int, float, array like.
            The second value(s).

        Returns
        -------
        float, array like of floats
            The differen ce(s) expressed in the range of 0 to 1.
        """
        return abs(value1 - value2) / (0.5 * (value1 + value2))


    @classmethod
    def PercentChange(cls, originalValue, newValue):
        return (newValue - originalValue) / abs(originalValue) * 100


    @classmethod
    def PercentError(cls, exactValue, approximateValue):
        return abs(exactValue - approximateValue) / abs(exactValue) * 100