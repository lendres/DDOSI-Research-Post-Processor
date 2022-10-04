#ifndef NOISEVARIANCEESTIMATEMETHOD_H
#define NOISEVARIANCEESTIMATEMETHOD_H

enum class NoiseVarianceEstimateMethod
{
	/// <summary>Point estimate.</summary>
	Point           = 0,

	/// <summary>Smoothed estimate.</summary>
	Smoothed        = 1,

	/// <summary>The number of types/items in the enumeration.</summary>
	Length

}; // End enum.

#endif