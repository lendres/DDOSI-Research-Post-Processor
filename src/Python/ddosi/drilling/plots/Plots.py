"""
Created on March 15, 2023
@author: Lance A. Endres
"""
from   lendres.plotting.PlotHelper                         import PlotHelper
from   lendres.plotting.PlotMaker                          import PlotMaker

class Plots():


    @classmethod
    def NewWobAndRpmPlot(cls, title, data, xAxisColumn="Time", wobColumn="WOB", rpmColumn="RPM", **kwargs):
        figure, (leftAxis, rightAxis) = PlotMaker.NewTwoAxesPlot(data, xAxisColumn, [wobColumn], [rpmColumn], **kwargs)

        # Labels.
        PlotHelper.Label(leftAxis, title, "Time (s)", "Weight on Bit (tons)")
        rightAxis.set_ylabel("Revolutions per Minute")

        return figure, (leftAxis, rightAxis)


    @classmethod
    def NewWobAndTobPlot(cls, title, data, xAxisColumn="Time", wobColumn="WOB", tobColumn="TOB", **kwargs):
        figure, (leftAxis, rightAxis) = PlotMaker.NewTwoAxesPlot(data, xAxisColumn, [wobColumn], [tobColumn], **kwargs)

        # Labels.
        PlotHelper.Label(leftAxis, title, "Time (s)", "Weight on Bit (tons)")
        rightAxis.set_ylabel("Torque (daN.m)")

        return figure, (leftAxis, rightAxis)


    @classmethod
    def NewWobAndRopPlot(cls, title, data, xAxisColumn="Time", wobColumn="WOB", ropColumn="ROP", **kwargs):
        figure, (leftAxis, rightAxis) = PlotMaker.NewTwoAxesPlot(data, xAxisColumn, [wobColumn], [ropColumn], **kwargs)

        # Labels.
        PlotHelper.Label(leftAxis, title, "Time (s)", "Weight on Bit (tons)")
        rightAxis.set_ylabel("Rate of Penetration (cm/s)")

        return figure, (leftAxis, rightAxis)


    @classmethod
    def NewRopWobAndRpmPlot(cls, title, data, xAxisColumn="Time", ropColumn="ROP", wobColumn="WOB", rpmColumn="TOB", **kwargs):
        figure, (leftAxis, rightAxis) = PlotMaker.CreateThreeAxisPlot(data, xAxisColumn, [ropColumn], [wobColumn, rpmColumn], **kwargs)

        # Labels.
        PlotHelper.Label(leftAxis, title, "Time (s)", "Weight on Bit (tons)")
        rightAxis.set_ylabel("Torque (daN.m)")

        return figure, (leftAxis, rightAxis)


    @classmethod
    def NewWobAndDepthOfCutPlot(cls, title, data, xAxisColumn="Time", wobColumn="WOB", depthOfCutColumn="Depth of Cut", **kwargs):
        figure, (leftAxis, rightAxis) = PlotMaker.NewTwoAxesPlot(data, xAxisColumn, [wobColumn], [depthOfCutColumn], **kwargs)

        # Labels.
        PlotHelper.Label(leftAxis, title, "Time (s)", "Weight on Bit (tons)")
        rightAxis.set_ylabel("Depth of Cut (cm/revolution)")

        return figure, (leftAxis, rightAxis)