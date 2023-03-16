"""
Created on February 17, 2023
@author: Lance A. Endres

https://medium.com/analytics-vidhya/how-to-filter-noise-with-a-low-pass-filter-python-885223e5e9b7
"""
from   scipy.signal                              import butter
from   scipy.signal                              import filtfilt


def ButterworthLowPassFilter(data, cutOffFrequency, samplingFrequency, order):
    nyquistFrequency = int(samplingFrequency/2.0)
    normalCutOff = cutOffFrequency / nyquistFrequency

    # Get the filter coefficients.
    # Analog is false because we are using regularly sampled data.
    b, a = butter(order, normalCutOff, btype="low", analog=False)
    y    = filtfilt(b, a, data)

    return y, b, a