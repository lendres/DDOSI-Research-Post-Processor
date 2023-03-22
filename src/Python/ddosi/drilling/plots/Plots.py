"""
Created on March 15, 2023
@author: Lance A. Endres
"""
from   lendres.plotting.PlotHelper                         import PlotHelper
from   lendres.plotting.PlotMaker                          import PlotMaker

class Plots():


    @classmethod
    def NewWobAndRpmPlot(cls, title, data, xAxisColumn="Time", wobColumn="WOB", xUnits="s", rpmColumn="RPM", **kwargs):
        figure, axes = PlotMaker.NewMultiAxesPlot(data, xAxisColumn, [[wobColumn], [rpmColumn]], **kwargs)

        # Labels.
        PlotHelper.Label(axes[0], title, xAxisColumn+" ("+xUnits+")", "Weight on Bit (tons)")
        axes[1].set_ylabel("Revolutions per Minute")

        return figure, axes

    @classmethod
    def NewDepthBasedWobAndRpmPlot(cls, title, data, xAxisColumn="Depth", wobColumn="WOB", xUnits="cm", rpmColumn="RPM", **kwargs):
        figure, axes = PlotMaker.NewMultiAxesPlot(data, xAxisColumn, [[wobColumn], [rpmColumn]], **kwargs)

        # Labels.
        PlotHelper.Label(axes[0], title, xAxisColumn+" ("+xUnits+")", "Weight on Bit (tons)")
        axes[1].set_ylabel("Revolutions per Minute")

        return figure, axes

    @classmethod
    def NewTobWobAndRpmPlot(cls, title, data, xAxisColumn="Time", tobColumn="TOB", wobColumn="WOB", rpmColumn="RPM", **kwargs):
        return cls.NewParameterVersusWobAndRpmPlot(title, data, xAxisColumn, "Torque (daN.m)", tobColumn, wobColumn, rpmColumn, **kwargs)


    @classmethod
    def NewRopWobAndRpmPlot(cls, title, data, xAxisColumn="Time", ropColumn="ROP", wobColumn="WOB", rpmColumn="RPM", **kwargs):
        return cls.NewParameterVersusWobAndRpmPlot(title, data, xAxisColumn, "Rate of Penetration (cm/s)", ropColumn, wobColumn, rpmColumn, **kwargs)


    @classmethod
    def NewDepthOfCutWobAndRpmPlot(cls, title, data, xAxisColumn="Time", depthOfCutColumn="Depth of Cut", wobColumn="WOB", rpmColumn="RPM", **kwargs):
        return cls.NewParameterVersusWobAndRpmPlot(title, data, xAxisColumn, "Depth of Cut (cm/revolution)", depthOfCutColumn, wobColumn, rpmColumn, **kwargs)


    @classmethod
    def NewParameterVersusWobAndRpmPlot(cls, title, data, xAxisColumn, parameterLabel, parameterColumn, wobColumn="WOB", rpmColumn="RPM", **kwargs):
        figure, axes = PlotMaker.NewMultiAxesPlot(data, xAxisColumn, [[parameterColumn], [wobColumn], [rpmColumn]], **kwargs)

        # Labels.
        PlotHelper.Label(axes[0], title, "Time (s)", parameterLabel)
        axes[1].set_ylabel("Weight on Bit (tons)")
        axes[2].set_ylabel("Revolutions per Minute")

        return figure, axes