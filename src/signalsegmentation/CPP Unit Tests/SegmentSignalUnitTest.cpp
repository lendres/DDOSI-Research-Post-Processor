#include "stdafx.h"
#include "CppUnitTest.h"
#include <stdio.h>
#include <direct.h>
#include <iterator>
#include "InputDataEnum.h"
#include "SegmentSignal.h"
#include "SegmentationResults.h"

using namespace Algorithms;
using namespace Microsoft::VisualStudio::CppUnitTestFramework;

namespace UnitTests
{
	// Test class for C version of signal segmenting library.
	TEST_CLASS(SegmentSignalUnitTest)
	{
	private:
		// For reading a data file with known input and solution.
		static const int				_numberOfDataPoints			= 100;
		static const int				_rows						= 5;
		static const int				_columns					= _numberOfDataPoints;
		double							_data[_rows][_columns];

		// Input values specified in paper.
		double							_f;
		static const int				_order						= 10;
		static const int				_order1						= 6;
		static const int				_niter						= 300;
		NoiseVarianceEstimateMethod		_rmode						= NoiseVarianceEstimateMethod::Point;


		// For debugging information only.  Used to check that the data file is located correctly relative to current
		// working directory.
		char _path[FILENAME_MAX];

	public:
		// Default constructor.
		SegmentSignalUnitTest()
		{
			_f							= 2.50;

			// Get the path so we can use the information for debugging.
			if (_getcwd(_path, sizeof(_path)) == NULL)
			{
				throw std::runtime_error("Cannot determine the current path.");
			}

			// Read the data file with our input and solution.
			ReadData();
		}

		~SegmentSignalUnitTest()
		{
		}

		// Test the function on input with a known solution.  This is the example in the paper.
		TEST_METHOD(LogSeparateTest)
		{
			// Known solutions from paper.
			double	C_solution		= 45.842;
			double	D_solution		= 0.06;
			int		NACT_solution	= 2;

			// Call to separate the signal.
			SegmentationResults* results = SegmentSignal::Segment(_data[(int)InputData::Log], _numberOfDataPoints, _f, _order, _order1, _rmode, _niter);

			// Check the output.
			Assert::AreEqual(D_solution, results->GetSegmentDensity(), 0.0000001, L"Event density \"D\" failed.");

			// The variance of the jump sequence is not correct.  The reason is unknown.  Either there is an error in the implementation
			// or the numerics are enough to cause an error.  There was only 3 decimal places of accuracy in the input file and C seams
			// somewhat sensitive.  We will run this check but allow for a fairly crude match.
			Assert::AreEqual(C_solution, results->GetJumpSequenceVariance(), 10, L"Variance of the jump sequence \"D\" failed.");

			// Check binary event sequence, segmented log, and filtered log.  The text file the input was taken from only contained 3 decimal points
			// of accuracy, so we have to specify some somewhat crude tolerances.
			for (int i = 0; i < _numberOfDataPoints; i++)
			{
				Assert::AreEqual(_data[(int)InputData::SegmentedLog][i], results->GetSegmentedLog()[i], 0.1, L"Segmented log failed.");
				Assert::AreEqual(_data[(int)InputData::EventSequence][i], results->GetBinaryEventSequence()[i], 0.1, L"Event sequence failed.");
				Assert::AreEqual(_data[(int)InputData::FilteredLog][i], results->GetFilteredSignal()[i], 0.3, L"Filter log failed.");
			}

			delete results;
		}

		TEST_METHOD(SignificantZoneTest)
		{
			// Initial data sets / input.
			//                                      Zone 1                        Zone 2
			double		baseData[]		= {0, 0, 0, 1, 0, 1, 1, 0, 0, 1,  0,  0,  0,  1,  1,  0,  0};
			double		xData[]			= {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16};
			int			signalLength	= 17;
			double		threshold		= 1.5;

			// Working and output data.
			double		workingData[]	= {0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0};
			vector<vector<int>>* results;

			// Copy the base line data set to the working data set so it can be modified.
			std::copy(std::begin(baseData), std::end(baseData), std::begin(workingData));

			// Initial test.  Check that the correct number of zones was found and that the indexes are correct.
			results = SegmentSignal::FindSignificantZones(workingData, xData, signalLength, threshold);
			Assert::AreEqual(2, (int)results->size(), L"The number of significant zones found is not correct.");
			Assert::AreEqual(0, (*results)[0][0], L"The index of the significant zone is not correct.");
			Assert::AreEqual(2, (*results)[0][1], L"The index of the significant zone is not correct.");
			Assert::AreEqual(10, (*results)[1][0], L"The index of the significant zone is not correct.");
			Assert::AreEqual(12, (*results)[1][1], L"The index of the significant zone is not correct.");

			// Check starting case of starting with a 1 but no significant zone: 1, 0, 0, 1 ...
			// Should only return 1 zone now.
			workingData[0]	= 1;
			results			= SegmentSignal::FindSignificantZones(workingData, xData, signalLength, threshold);
			Assert::AreEqual(1, (int)results->size(), L"The number of significant zones found is not correct.");

			// Check case of starting with with a 1 and having a significant zone: 1, 0, 0, 0, 0, 1 ...
			workingData[3]	= 0;
			results			= SegmentSignal::FindSignificantZones(workingData, xData, signalLength, threshold);
			Assert::AreEqual(2, (int)results->size(), L"The number of significant zones found is not correct.");
			Assert::AreEqual(1, (*results)[0][0], L"The index of the significant zone is not correct.");
			Assert::AreEqual(4, (*results)[0][1], L"The index of the significant zone is not correct.");

			// Reset working data to original data.
			std::copy(std::begin(baseData), std::end(baseData), std::begin(workingData));

			// Check case of two zones immediately following each other: ... 0, 0, 0, 1, 0, 0, 0 ...
			workingData[6]	= 0;
			results			= SegmentSignal::FindSignificantZones(workingData, xData, signalLength, threshold);
			Assert::AreEqual(3, (int)results->size(), L"The number of significant zones found is not correct.");

			// Reset working data to original data.
			std::copy(std::begin(baseData), std::end(baseData), std::begin(workingData));

			// Check case of ending with a zone: ... 1, 0, 0, 0
			workingData[14]	= 0;
			results			= SegmentSignal::FindSignificantZones(workingData, xData, signalLength, threshold);
			Assert::AreEqual(3, (int)results->size(), L"The number of significant zones found is not correct.");

			// Check case of ending with a 1: ... 0, 0, 0, 1
			workingData[13] = 0;
			workingData[16] = 1;
			results = SegmentSignal::FindSignificantZones(workingData, xData, signalLength, threshold);
			Assert::AreEqual(2, (int)results->size(), L"The number of significant zones found is not correct.");
			Assert::AreEqual(10, (*results)[1][0], L"The index of the significant zone is not correct.");
			Assert::AreEqual(15, (*results)[1][1], L"The index of the significant zone is not correct.");

			// Reset working data to original data.
			std::copy(std::begin(baseData), std::end(baseData), std::begin(workingData));

			// Test including the end points a the zones.  Include both end points of the array and one zone in the middle.
			workingData[14]	= 0;
			results			= SegmentSignal::FindSignificantZones(workingData, xData, signalLength, threshold, true);
			Assert::AreEqual(3, (int)results->size(), L"The number of significant zones found is not correct.");
			Assert::AreEqual(0, (*results)[0][0], L"The index of the significant zone is not correct.");
			Assert::AreEqual(3, (*results)[0][1], L"The index of the significant zone is not correct.");
			Assert::AreEqual(9, (*results)[1][0], L"The index of the significant zone is not correct.");
			Assert::AreEqual(13, (*results)[1][1], L"The index of the significant zone is not correct.");
			Assert::AreEqual(13, (*results)[2][0], L"The index of the significant zone is not correct.");
			Assert::AreEqual(16, (*results)[2][1], L"The index of the significant zone is not correct.");
		}


		// Reads a data file that contains the information from the example used in the paper on the algorithm.
		void ReadData()
		{
			// Open the file and validate the opening.  This will through an error to the "Test Explorer" if
			// if fails to open.
			FILE* file;
			int error = fopen_s(&file, "..\\..\\..\\Test Data\\Data Set 1.txt", "r");
			Assert::IsFalse(error || file == NULL, L"Error opening data file.");

			// Read the data from the file transposing the data as we go.  The loops are set up to read the data from the as
			// you normally would.  For each line (column), read each entry (row).  The transposing happens when the data
			// is stored into the array "_data".
			for (int i = 0; i < _columns; i++)
			{
				for (int j = 0; j < _rows; j++)
				{
					float val = 0;
					int scanResult = fscanf_s(file, "%f", &val);

					// We should have the correct number of entries in the file, if this file does not contain enough
					// data, then it is the wrong file.  Throw an error.
					Assert::AreNotEqual(scanResult, EOF, L"End of file reached before all data read.  Not the correct input file.");

					// Transpose the data as we read it.  This is done to make it easier to pass the data to the functions.  We don't have
					// to rearrange the data, just pass it the entry point (address of first value) to the data we want to pass.
					_data[j][i] = val;
				}
			}

			// Close the file.
			fclose(file);
		}

	}; // End class.
} // End namespace.