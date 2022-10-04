#ifndef SEGMENTSIGNAL_H
#define SEGMENTSIGNAL_H

#include "NoiseVarianceEstimateMethod.h"
#include "SegmentationResults.h"
#include <vector>

using namespace std;

namespace Algorithms
{
	/// <summary>
	/// C++ interface for the C code.
	/// </summary>
	class SegmentSignal
	{
		public:
			/// <summary>
			/// Segment a signal using the Maximum Likelihood Estimation of Radhakrishnan, et al, 1991.  Attempts to identify regions of the signal that are
			/// considered "consistent."  Assumes a signal that has a state which changes only at segment boundaries.  The state change can be random and the
			/// noise on top of the signal is modeled as Gaussian, but not necessarily stationary.
			/// 
			/// Assumes a point estimate of the noise variance and an upper bound of 300 on the number of Single Most Likelihood Replacement iterations.
			/// </summary>
			/// <param name="signal">Input signal to be segmented.</param>
			/// <param name="signalLength">Input signal to be segmented.</param>
			/// <param name="threshold">Segmentation threshold.</param>
			/// <param name="jumpSequenceWindowSize">Length of the moving average window sized used for smoothing the input well log to arrive at an initial estimate of the jump sequence variance.</param>
			/// <param name="noiseVarianceWindowSize">Length of the moving average window used for smoothing the noise variances.</param>
			/// <param name="noiseVarianceEstimateMethod">
			/// Noise variance estimate option.
			//		rmode = 0 ==> Point estimate of noise variance.
			//		rmode = 1 ==> Noise estimates smoothed within segments.
			/// </param>
			/// <returns>A SegmentationResults instance which contains the algorithm output of binary events, segmented log, filtered log, et cetera.</returns>
			static SegmentationResults* Segment(double signal[], int signalLength, double threshold, int jumpSequenceWindowSize, int noiseVarianceWindowSize);

			/// <summary>
			/// Segment a signal using the Maximum Likelihood Estimation of Radhakrishnan, et al, 1991.  Attempts to identify regions of the signal that are
			/// considered "consistent."  Assumes a signal that has a state which changes only at segment boundaries.  The state change can be random and the
			/// noise on top of the signal is modeled as Gaussian, but not necessarily stationary.
			/// 
			/// Assumes an upper bound of 300 on the number of Single Most Likelihood Replacement iterations.
			/// </summary>
			/// <param name="signal">Input signal to be segmented.</param>
			/// <param name="signalLength">Input signal to be segmented.</param>
			/// <param name="threshold">Segmentation threshold.</param>
			/// <param name="jumpSequenceWindowSize">Length of the moving average window sized used for smoothing the input well log to arrive at an initial estimate of the jump sequence variance.</param>
			/// <param name="noiseVarianceWindowSize">Length of the moving average window used for smoothing the noise variances.</param>
			/// <param name="noiseVarianceEstimateMethod">
			/// Noise variance estimate option.
			//		rmode = 0 ==> Point estimate of noise variance.
			//		rmode = 1 ==> Noise estimates smoothed within segments.
			/// </param>
			/// <returns>A SegmentationResults instance which contains the algorithm output of binary events, segmented log, filtered log, et cetera.</returns>
			static SegmentationResults* Segment(double signal[], int signalLength, double threshold, int jumpSequenceWindowSize, int noiseVarianceWindowSize, NoiseVarianceEstimateMethod noiseVarianceEstimateMethod);

			/// <summary>
			/// Segment a signal using the Maximum Likelihood Estimation of Radhakrishnan, et al, 1991.  Attempts to identify regions of the signal that are
			/// considered "consistent."  Assumes a signal that has a state which changes only at segment boundaries.  The state change can be random and the
			/// noise on top of the signal is modeled as Gaussian, but not necessarily stationary.
			/// </summary>
			/// <param name="signal">Input signal to be segmented.</param>
			/// <param name="signalLength">Input signal to be segmented.</param>
			/// <param name="threshold">Segmentation threshold.</param>
			/// <param name="jumpSequenceWindowSize">Length of the moving average window sized used for smoothing the input well log to arrive at an initial estimate of the jump sequence variance.</param>
			/// <param name="noiseVarianceWindowSize">Length of the moving average window used for smoothing the noise variances.</param>
			/// <param name="noiseVarianceEstimateMethod">
			/// Noise variance estimate option.
			//		rmode = 0 ==> Point estimate of noise variance.
			//		rmode = 1 ==> Noise estimates smoothed within segments.
			/// </param>
			/// <param name="maxSMLRIterations">Upper bound on the number of Single Most Likelihood Replacement iterations.</param>
			/// <returns>A SegmentationResults instance which contains the algorithm output of binary events, segmented log, filtered log, et cetera.</returns>
			static SegmentationResults* Segment(double signal[], int signalLength, double threshold, int jumpSequenceWindowSize, int noiseVarianceWindowSize, NoiseVarianceEstimateMethod noiseVarianceEstimateMethod, int maxSMLRIterations);

			/// <summary>
			/// Segment a signal using the Maximum Likelihood Estimation of Radhakrishnan, et al, 1991.  Attempts to identify regions of the signal that are
			/// considered "consistent."  Assumes a signal that has a state which changes only at segment boundaries.  The state change can be random and the
			/// noise on top of the signal is modeled as Gaussian, but not necessarily stationary.
			/// 
			/// Assumes a point estimate of the noise variance and an upper bound of 300 on the number of Single Most Likelihood Replacement iterations.
			/// </summary>
			/// <param name="signal">Input signal to be segmented.</param>
			/// <param name="threshold">Segmentation threshold.</param>
			/// <param name="jumpSequenceWindowSize">Length of the moving average window sized used for smoothing the input well log to arrive at an initial estimate of the jump sequence variance.</param>
			/// <param name="noiseVarianceWindowSize">Length of the moving average window used for smoothing the noise variances.</param>
			/// <param name="noiseVarianceEstimateMethod">
			/// Noise variance estimate option.
			//		rmode = 0 ==> Point estimate of noise variance.
			//		rmode = 1 ==> Noise estimates smoothed within segments.
			/// </param>
			/// <returns>A SegmentationResults instance which contains the algorithm output of binary events, segmented log, filtered log, et cetera.</returns>
			static SegmentationResults* Segment(vector<double> signal, double threshold, int jumpSequenceWindowSize, int noiseVarianceWindowSize);

			/// <summary>
			/// Segment a signal using the Maximum Likelihood Estimation of Radhakrishnan, et al, 1991.  Attempts to identify regions of the signal that are
			/// considered "consistent."  Assumes a signal that has a state which changes only at segment boundaries.  The state change can be random and the
			/// noise on top of the signal is modeled as Gaussian, but not necessarily stationary.
			/// 
			/// Assumes an upper bound of 300 on the number of Single Most Likelihood Replacement iterations.
			/// </summary>
			/// <param name="signal">Input signal to be segmented.</param>
			/// <param name="threshold">Segmentation threshold.</param>
			/// <param name="jumpSequenceWindowSize">Length of the moving average window sized used for smoothing the input well log to arrive at an initial estimate of the jump sequence variance.</param>
			/// <param name="noiseVarianceWindowSize">Length of the moving average window used for smoothing the noise variances.</param>
			/// <param name="noiseVarianceEstimateMethod">
			/// Noise variance estimate option.
			//		rmode = 0 ==> Point estimate of noise variance.
			//		rmode = 1 ==> Noise estimates smoothed within segments.
			/// </param>
			/// <returns>A SegmentationResults instance which contains the algorithm output of binary events, segmented log, filtered log, et cetera.</returns>
			static SegmentationResults* Segment(vector<double> signal, double threshold, int jumpSequenceWindowSize, int noiseVarianceWindowSize, NoiseVarianceEstimateMethod noiseVarianceEstimateMethod);

			/// <summary>
			/// Segment a signal using the Maximum Likelihood Estimation of Radhakrishnan, et al, 1991.  Attempts to identify regions of the signal that are
			/// considered "consistent."  Assumes a signal that has a state which changes only at segment boundaries.  The state change can be random and the
			/// noise on top of the signal is modeled as Gaussian, but not necessarily stationary.
			/// </summary>
			/// <param name="signal">Input signal to be segmented.</param>
			/// <param name="threshold">Segmentation threshold.</param>
			/// <param name="jumpSequenceWindowSize">Length of the moving average window sized used for smoothing the input well log to arrive at an initial estimate of the jump sequence variance.</param>
			/// <param name="noiseVarianceWindowSize">Length of the moving average window used for smoothing the noise variances.</param>
			/// <param name="noiseVarianceEstimateMethod">
			/// Noise variance estimate option.
			//		rmode = 0 ==> Point estimate of noise variance.
			//		rmode = 1 ==> Noise estimates smoothed within segments.
			/// </param>
			/// <param name="maxSMLRIterations">Upper bound on the number of Single Most Likelihood Replacement iterations.</param>
			/// <returns>A SegmentationResults instance which contains the algorithm output of binary events, segmented log, filtered log, et cetera.</returns>
			static SegmentationResults* Segment(vector<double> signal, double threshold, int jumpSequenceWindowSize, int noiseVarianceWindowSize, NoiseVarianceEstimateMethod noiseVarianceEstimateMethod, int maxSMLRIterations);

			/// <summary>
			/// Creates a list of indexes which indicate where the "significant zones" are in the results of the segmentation.  A significant
			/// zone is defined as a region between binary events (for example 1,0,0,0,1 is a region/zone of 3) that are longer than the
			/// specified threshold.
			/// 
			/// An example use for this algorithm would to be to first run the segmentation algorithm on the log/signal to get the results, then
			/// use this algorithm to find the regions of interest.
			/// 
			/// Since a log/signal fed to the segmentation algorithm is the dependent values (y values of a plot), the independent (x values)
			/// must be supplied to this algorithm to enable evaluate the "length" of each zone.
			/// </summary>
			/// <param name="binaryEvents">Array of binary events (1s and 0s) which specify the boundaries of each zone.</param>
			/// <param name="xData">Independent values associated with the log/signal fed to the Segment algorithm and produced the SegmentationResults.</param>
			/// <param name="signalLength">Input signal to be segmented.</param>
			/// <param name="threshold">Length a zone must be to be consider "significant."  Zones shorter than this are ignored.</param>
			/// <returns>A vector of arrays of length 2 indicating the zones.  Each entry in the List is a pair indicating the starting and ending index of one significant zone.</returns>
			static vector<vector<int>>* FindSignificantZones(double binaryEvents[], double xData[], int signalLength, double threshold);

			/// <summary>
			/// Creates a list of indexes which indicate where the "significant zones" are in the results of the segmentation.  A significant
			/// zone is defined as a region between binary events (for example 1,0,0,0,1 is a region/zone of 3) that are longer than the
			/// specified threshold.
			/// 
			/// An example use for this algorithm would to be to first run the segmentation algorithm on the log/signal to get the results, then
			/// use this algorithm to find the regions of interest.
			/// 
			/// Since a log/signal fed to the segmentation algorithm is the dependent values (y values of a plot), the independent (x values)
			/// must be supplied to this algorithm to enable evaluate the "length" of each zone.
			/// </summary>
			/// <param name="binaryEvents">Array of binary events (1s and 0s) which specify the boundaries of each zone.</param>
			/// <param name="xData">Independent values associated with the log/signal fed to the Segment algorithm and produced the SegmentationResults.</param>
			/// <param name="signalLength">Input signal to be segmented.</param>
			/// <param name="threshold">Length a zone must be to be consider "significant."  Zones shorter than this are ignored.</param>
			/// <param name="includeBoundries">If true, the end data points are added as part of the zone.  Does not change how zones are found.</param>
			/// <returns>A vector of arrays of length 2 indicating the zones.  Each entry in the List is a pair indicating the starting and ending index of one significant zone.</returns>
			static vector<vector<int>>* FindSignificantZones(double binaryEvents[], double xData[], int signalLength, double threshold, bool includeBoundries);

		private:
			/// <summary>
			/// Scans the binary events for the next zero.  Helper function to FindSignificantZones.
			/// </summary>
			/// <param name="binaryEvents">Binary event sequence array.</param>
			/// <param name="signalLength">Input signal to be segmented.</param>
			/// <param name="currentIndex">Index to start scanning from.</param>
			/// <returns>Index of next zero.</returns>
			static int FindNextZero(double binaryEvents[], int signalLength, int currentIndex);

			/// <summary>
			/// Checks to see if the threshold for being a significant zone is met.  If it is, it is added to the list of significant zones.
			/// </summary>
			/// <param name="xData">Independent values associated with the log/signal fed to the Segment algorithm and produced the SegmentationResults.</param>
			/// <param name="threshold">Length a zone must be to be consider "significant."  Zones shorter than this are ignored.</param>
			/// <param name="includeBoundries">If true, the end data points are added as part of the zone.  Does not change how zones are found.</param>
			/// <param name="significantZones">List of significant zones.</param>
			/// <param name="startIndex">Starting index of zone.</param>
			/// <param name="endIndex">Ending index of the zone.</param>
			static void CheckIfValidZone(double xData[], double threshold, bool includeBoundries, vector<vector<int>>* significantZones, int startIndex, int endIndex);

	}; // End class.
} // End namespace.

#endif