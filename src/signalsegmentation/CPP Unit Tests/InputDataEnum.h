#ifndef INPUTDATAENUM_H
#define INPUTDATAENUM_H

// Enumeration stating how data is located in the data file.
enum class InputData
{
	Depth = 0,
	Log,
	SegmentedLog,
	EventSequence,
	FilteredLog
};

#endif