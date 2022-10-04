#include "SegmentSignal.h"
#include "NoiseVarianceEstimateMethod.h"
#include "SegmentSignalFunctions.h"
#include <vector>
#include <cmath>

using namespace std;

namespace Algorithms
{
	SegmentationResults* SegmentSignal::Segment(double signal[], int signalLength, double threshold, int jumpSequenceWindowSize, int noiseVarianceWindowSize)
	{
		return Segment(signal, signalLength, threshold, jumpSequenceWindowSize, noiseVarianceWindowSize, NoiseVarianceEstimateMethod::Point, 300);
	}

	SegmentationResults* SegmentSignal::Segment(double signal[], int signalLength, double threshold, int jumpSequenceWindowSize, int noiseVarianceWindowSize, NoiseVarianceEstimateMethod noiseVarianceEstimateMethod)
	{
		return Segment(signal, signalLength, threshold, jumpSequenceWindowSize, noiseVarianceWindowSize, noiseVarianceEstimateMethod, 300);
	}

	SegmentationResults* SegmentSignal::Segment(double signal[], int signalLength, double threshold, int jumpSequenceWindowSize, int noiseVarianceWindowSize, NoiseVarianceEstimateMethod noiseVarianceEstimateMethod, int maxSMLRIterations)
	{
		// Scalars which are need for output from the call to the algorithm.
		int		numberOfBinaryEvents	= 0;
		double	jumpSequenceVariance	= 0;
		double	segmentDensity			= 0;
		int		iterations				= 0;
		int		error					= 0;

		// We seem to need to create the array in the function immediately prior to calling the unmanaged code, otherwise the garbage collector
		// gets cute and moves things around, which the unmanaged code takes offense to.
		//double* signalToPass = new double[signalLength];
		//for (int i = 0; i < signalLength; i++)
		//{
		//	signalToPass[i] = signal[i];
		//}


		// Create the output arrays.  After being populated by the call to the algorithm they are grouped, stored, and returned in the SegmenationResults data structure.
		double* Q		= new double[signalLength];		// Binary event sequence.
		double* FLTLOG	= new double[signalLength];		// Filtered signal.
		double* SEGLOG	= new double[signalLength];		// Segmented log.
		double* R		= new double[signalLength];		// Noise variance.

		// Function call to the C DLL.
		::SegmentSignal(signal, signalLength, threshold, jumpSequenceWindowSize, noiseVarianceWindowSize, (int)noiseVarianceEstimateMethod, maxSMLRIterations, Q, numberOfBinaryEvents, FLTLOG, SEGLOG, R, jumpSequenceVariance, segmentDensity, iterations, error);

		return new SegmentationResults(Q, numberOfBinaryEvents, FLTLOG, SEGLOG, R, jumpSequenceVariance, segmentDensity, iterations, error);
	}

	SegmentationResults* SegmentSignal::Segment(vector<double> signal, double threshold, int jumpSequenceWindowSize, int noiseVarianceWindowSize)
	{
		return Segment(signal, threshold, jumpSequenceWindowSize, noiseVarianceWindowSize, NoiseVarianceEstimateMethod::Point, 300);
	}

	SegmentationResults* SegmentSignal::Segment(vector<double> signal, double threshold, int jumpSequenceWindowSize, int noiseVarianceWindowSize, NoiseVarianceEstimateMethod noiseVarianceEstimateMethod)
	{
		return Segment(signal, threshold, jumpSequenceWindowSize, noiseVarianceWindowSize, noiseVarianceEstimateMethod, 300);
	}

	SegmentationResults* SegmentSignal::Segment(vector<double> signal, double threshold, int jumpSequenceWindowSize, int noiseVarianceWindowSize, NoiseVarianceEstimateMethod noiseVarianceEstimateMethod, int maxSMLRIterations)
	{
		// Scalars which are need for output from the call to the algorithm.
		int		numberOfBinaryEvents	= 0;
		double	jumpSequenceVariance	= 0;
		double	segmentDensity			= 0;
		int		iterations				= 0;
		int		error					= 0;
	
		int signalLength		= signal.size();
		double* signalToPass	= new double[signalLength];
		for (int i = 0; i < signalLength; i++)
		{
			signalToPass[i] = signal[i];
		}

		// Create the output arrays.  After being populated by the call to the algorithm they are grouped, stored, and returned in the SegmenationResults data structure.
		double* Q		= new double[signalLength];		// Binary event sequence.
		double* FLTLOG	= new double[signalLength];		// Filtered signal.
		double* SEGLOG	= new double[signalLength];		// Segmented log.
		double* R		= new double[signalLength];		// Noise variance.


		int estimateMethod	= (int)noiseVarianceEstimateMethod;

		// Function call to the C DLL.
		::SegmentSignal(signalToPass, signalLength, threshold, jumpSequenceWindowSize, noiseVarianceWindowSize, estimateMethod, maxSMLRIterations, Q, numberOfBinaryEvents, FLTLOG, SEGLOG, R, jumpSequenceVariance, segmentDensity, iterations, error);

		return new SegmentationResults(Q, numberOfBinaryEvents, FLTLOG, SEGLOG, R, jumpSequenceVariance, segmentDensity, iterations, error);
	}

	vector<vector<int>>* SegmentSignal::FindSignificantZones(double binaryEvents[], double xData[], int signalLength, double threshold)
	{
		return FindSignificantZones(binaryEvents, xData, signalLength, threshold, false);
	}

	vector<vector<int>>* SegmentSignal::FindSignificantZones(double binaryEvents[], double xData[], int signalLength, double threshold, bool includeBoundries)
	{
		vector<vector<int>>* significantZones = new vector<vector<int>>	();

		// Find the first "0" entry which will mark the beginning of a zone.
		int zoneStart = FindNextZero(binaryEvents, signalLength, 0);

		for (int currentIndex = zoneStart+1; currentIndex < signalLength; currentIndex++)
		{
			if (binaryEvents[currentIndex] == 1)
			{
				CheckIfValidZone(xData, threshold, includeBoundries, significantZones, zoneStart, currentIndex-1);

				// Scan for the start of the next potential section.
				zoneStart = FindNextZero(binaryEvents, signalLength, currentIndex);
				currentIndex = zoneStart;
			}
		}

		// If the last entry of the binary events is zero, we need to handle the final section.
		if (binaryEvents[signalLength-1] == 0)
		{
			CheckIfValidZone(xData, threshold, includeBoundries, significantZones, zoneStart, signalLength-1);
		}

		// When including the boundaries (includeBoundaries==true), it is possible to have added data points before the beginning of the array
		// and after the end.  We need to check for and, if they exist, correct them.
		if (significantZones->size() > 0)
		{
			if ((*significantZones)[0][0] < 0)
			{
				(*significantZones)[0][0] = 0;
			}

			if ((*significantZones)[significantZones->size()-1][1] >= signalLength)
			{
				(*significantZones)[significantZones->size()-1][1] = signalLength-1;
			}
		}

		return significantZones;
	}

	int SegmentSignal::FindNextZero(double binaryEvents[], int signalLength, int currentIndex)
	{
		// Find the first zero.
		while (binaryEvents[currentIndex] == 1 && currentIndex < signalLength-1)
		{
			currentIndex++;
		}
		return currentIndex;
	}

	void SegmentSignal::CheckIfValidZone(double xData[], double threshold, bool includeBoundries, vector<vector<int>>* significantZones, int startIndex, int endIndex)
	{
		// Check to see if the threshold is met.  If it met, we will store the section
		// as a significant zone.  If the threshold is not met, then the zone is not long
		// enough so it is ignored and we scan ahead.
		if (abs(xData[endIndex] - xData[startIndex]) > threshold)
		{
			if (includeBoundries)
			{
				significantZones->push_back({startIndex-1, endIndex+1});
			}
			else
			{
				significantZones->push_back({startIndex, endIndex});
			}
		}
	}
} // End namespace.