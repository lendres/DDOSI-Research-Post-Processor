#include "SegmentationResults.h"

namespace Algorithms
{
	SegmentationResults::SegmentationResults(double binaryEventSequence[], int numberOfBinaryEvents, double filteredSignal[], double segmentedLog[], double noiseVariance[], double jumpSequenceVariance, double segmentDensity, int iterations, int error)
	{
		_binaryEventSequence	= binaryEventSequence;
		_numberOfBinaryEvents	= numberOfBinaryEvents;
		_filteredSignal			= filteredSignal;
		_segmentedLog			= segmentedLog;
		_noiseVariance			= noiseVariance;

		_jumpSequenceVariance	= jumpSequenceVariance;
		_segmentDensity			= segmentDensity;
		_iterations				= iterations;
		_error					= error;
	}

	SegmentationResults::~SegmentationResults()
	{
		if (_binaryEventSequence)
		{
			delete _binaryEventSequence;
			delete _filteredSignal;
			delete _segmentedLog;
			delete _noiseVariance;
		}
	}

	double* SegmentationResults::GetBinaryEventSequence()
	{
		return _binaryEventSequence;
	}

	int SegmentationResults::GetNumberOfBinaryEvents()
	{
		return _numberOfBinaryEvents;
	}

	double* SegmentationResults::GetFilteredSignal()
	{
		return _filteredSignal;
	}

	double* SegmentationResults::GetSegmentedLog()
	{
		return _segmentedLog;
	}

	double* SegmentationResults::GetNoiseVariance()
	{
		return _noiseVariance;
	}

	double SegmentationResults::GetJumpSequenceVariance()
	{
		return _jumpSequenceVariance;
	}

	double SegmentationResults::GetSegmentDensity()
	{
		return _segmentDensity;
	}
		
	int SegmentationResults::GetIterations()
	{
		return _iterations;
	}

	int SegmentationResults::GetError()
	{
		return _error;
	}

} // End namespace.