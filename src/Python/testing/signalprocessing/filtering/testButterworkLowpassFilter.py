"""
Created on February 17, 2023
@author: Lance A. Endres
"""

from   scipy.signal                                                  import freqz

import numpy                                                         as np
import pandas                                                        as pd
import matplotlib.pyplot                                             as plt

from   ddosi.signalprocessing.ButterworthLowPass                     import ButterworthLowPassFilter

import unittest


class testButterworthLowPassFilter(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Solution provided in paper.
        # Columns that are in the input file.  The first two are input to the function, the last three are the known solution.
        pass

    def setUp(self):
        """
        Set up function that runs before each test.
        """
        pass


    def testButterworkLowpassFilter(self):
        # Filter requirements.
        order                = 6
        samplingFrequency    = 30.0   # Sample rate, Hz.
        cutOff               = 3.667  # Desired cutoff frequency of the filter, Hz.

        # Demonstrate the use of the filter.
        # First make some data to be filtered.
        totalTime       = 5.0
        numberOfSamples = int(totalTime*samplingFrequency)
        time            = np.linspace(0, totalTime, numberOfSamples, endpoint=False)

        # "Noisy" data.  We want to recover the 1.2 Hz signal from this.
        data = np.sin(1.2*2*np.pi*time) + 1.5*np.cos(9*2*np.pi*time) + 0.5*np.sin(12.0*2*np.pi*time)

        # Get the filter coefficients so we can check its frequency response.
        y, b, a = ButterworthLowPassFilter(data, cutOff, samplingFrequency, order)

        # Plot the frequency response.
        w, h = freqz(b, a, fs=samplingFrequency, worN=8000)
        plt.subplot(2, 1, 1)
        plt.plot(w, np.abs(h), 'b')
        plt.plot(cutOff, 0.5*np.sqrt(2), 'ko')
        plt.axvline(cutOff, color='k')
        plt.xlim(0, 0.5*samplingFrequency)
        plt.title("Lowpass Filter Frequency Response")
        plt.xlabel('Frequency [Hz]')
        plt.grid()

        # Filter the data, and plot both the original and filtered signals.
        plt.subplot(2, 1, 2)
        plt.plot(time, data, 'b-', label='data')
        plt.plot(time, y, 'g-', linewidth=2, label='filtered data')
        plt.xlabel('Time [sec]')

        plt.grid(True)
        plt.legend()
        plt.show()






if __name__ == "__main__":
    unittest.main()