#ifndef SEGMENTATIONRESULTS_H
#define SEGMENTATIONRESULTS_H

namespace Algorithms
{
	class SegmentationResults
	{
		private:
			double*		_binaryEventSequence			= 0;
			int			_numberOfBinaryEvents;
			double*		_filteredSignal					= 0;
			double*		_segmentedLog					= 0;
			double*		_noiseVariance					= 0;
			double		_jumpSequenceVariance;
			double		_segmentDensity;
			int			_iterations;
			int			_error;

		public:
			/// <summary>
			/// Constructor.
			/// </summary>
			/// <param name="binaryEventSequence">Binary event sequence.</param>
			/// <param name="numberOfBinaryEvents">Number of binary events found (number of "1"s found in binary event sequence).</param>
			/// <param name="filteredSignal">Filtered signal.</param>
			/// <param name="segmentedLog">Segmented log.</param>
			/// <param name="noiseVariance">Noise variance.</param>
			/// <param name="jumpSequenceVariance">Jump sequence variance.</param>
			/// <param name="segmentDensity">Segment density (ratio of events to total entries in binary event sequence).</param>
			/// <param name="iterations">Number of iterations performed.</param>
			/// <param name="error">Error flag.</param>
			SegmentationResults(double binaryEventSequence[], int numberOfBinaryEvents, double filteredSignal[], double segmentedLog[], double noiseVariance[], double jumpSequenceVariance, double segmentDensity, int iterations, int error);

			/// <summary>
			/// destructor.
			/// </summary>
			~SegmentationResults();

		public:
			/// <summary>
			/// Array that contains 1s at segmented log boundaries and 0s elsewhere.
			/// </summary>
			double* GetBinaryEventSequence();

			/// <summary>
			/// Number of binary event sequences detected (number of "1"s in the BinaryEventSequence array).
			/// </summary>
			int GetNumberOfBinaryEvents();

			/// <summary>
			/// Filtered estimate of the signal.
			/// </summary>
			double* GetFilteredSignal();

			/// <summary>
			/// Average of filter log for each segment.
			/// </summary>
			double* GetSegmentedLog();

			/// <summary>
			/// Estimate noise variance.
			/// </summary>
			double* GetNoiseVariance();

			/// <summary>
			/// Estimated variance of the jump sequence.
			/// </summary>
			double GetJumpSequenceVariance();

			/// <summary>
			/// Estimate segment density.
			/// </summary>
			double GetSegmentDensity();
		
			/// <summary>
			/// SMLR iteration count.
			/// </summary>
			int GetIterations();

			/// <summary>
			/// Error flag.
			///		Zero - no error.
			///		Less than zero - invalid event density estimated after threshold.  Reduce/increase
			///			threshold and rerun.
			///		Greater than zero - logarithm argument became zero at sample number returned in error during
			///			the calculation of likelihood ratios in SMLR.  There may be more samples of this type which
			///			may give rise to this problem.  Edit/rescale data values and rerun.
			/// </summary>
			int GetError();

	}; // End class.
} // End namespace.

#endif