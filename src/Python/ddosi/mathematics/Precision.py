"""
Created on August 12, 2022
@author: Lance A. Endres
"""

class Precision():
    epsilon = 1e-10;


    @classmethod
    def IsZero(cls, value, epsilon=None):
        if epsilon is None:
            epsilon = Precision.epsilon

        return abs(value) < epsilon


    @classmethod
    def Equal(cls, value1, value2, epsilon=None):
        if epsilon is None:
            epsilon = Precision.epsilon

        return abs(value1 - value2) < epsilon