#!/usr/bin/env python3
import drawsvg as draw
from OCC.Core.HLRBRep import HLRBRep_Algo, HLRBRep_HLRToShape
from OCC.Core.HLRAlgo import HLRAlgo_Projector
from OCC.Core.gp import gp_Ax2, gp_Pnt, gp_Dir
from OCC.Core.TopoDS import TopoDS_Compound
from OCC.Core.BRep import BRep_Builder
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Display.SimpleGui import init_display
from OCC.Core.TopAbs import TopAbs_FORWARD
from OCC.Core.TopoDS import TopoDS_Compound
from OCC.Core.BRep import BRep_Builder
from OCC.Core.gp import gp_Trsf, gp_Ax1
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform

from updatedOffscreenRenderer import UpdatedOffscreenRenderer
import time
import math

labelWidth = 370
labelHeight = 120



def addBorder(d, strokeSize = 4, margin = 5, topCornerRadius = 4):
    # Add border to the label with rounded corners on top
    d.append(draw.Lines(-labelWidth/2 + margin + topCornerRadius, -labelHeight/2 + margin,
                        labelWidth/2 - margin - topCornerRadius, -labelHeight/2 + margin,
                        close=False,
                fill='none',
                stroke='black',
                stroke_width=strokeSize))
    
    d.append(draw.Lines(labelWidth/2 - margin, -labelHeight/2 + margin + topCornerRadius,
                        labelWidth/2 - margin, labelHeight/2 - margin,
                        -labelWidth/2 + margin, labelHeight/2 - margin,
                        -labelWidth/2 + margin, -labelHeight/2 + margin + topCornerRadius,
                        close=False,
                fill='none',
                stroke='black',
                stroke_width=strokeSize))
    
    d.append(draw.ArcLine(-labelWidth/2 + margin + topCornerRadius, -labelHeight/2 + margin + topCornerRadius,
                          topCornerRadius, 90, 180,
        stroke='black', stroke_width=strokeSize, fill='none'))
    
    d.append(draw.ArcLine(labelWidth/2 - margin - topCornerRadius, -labelHeight/2 + margin + topCornerRadius,
                          topCornerRadius, 0, 90,
        stroke='black', stroke_width=strokeSize, fill='none'))


def addText(d, textLine1, textLine2 = ""):
    # Add text to the label
    fontSize = 30
    marginFromCenter = 5
    d.append(draw.Text(textLine1, fontSize, 0, -marginFromCenter, center=1))
    d.append(draw.Text(textLine2, fontSize, 0, marginFromCenter+fontSize, center=1))


def renderAngle(shape, orientation = gp_Dir(1., 0., 0.), hideObstructed = True):
    myAlgo = HLRBRep_Algo()
    aProjector = HLRAlgo_Projector(gp_Ax2(gp_Pnt(0., 0, 0), orientation))
    myAlgo.Add(shape)
    myAlgo.Projector(aProjector)

    myAlgo.Update()

    if hideObstructed:
        myAlgo.Hide()       # Hide the obsructed lines (very slow!)

    aHLRToShape = HLRBRep_HLRToShape(myAlgo)

    aCompound = TopoDS_Compound()
    aBuilder = BRep_Builder()
    aBuilder.MakeCompound(aCompound)
    aBuilder.Add(aCompound, aHLRToShape.VCompound())
    aBuilder.Add(aCompound, aHLRToShape.OutLineVCompound())

    return aCompound


def render3D(d):

    stepReader = STEPControl_Reader()
    stepReader.ReadFile('./meca/91255A008_Button Head Hex Drive Screw.STEP')
    # stepReader.ReadFile('./meca/93075A148_Low-Strength Zinc-Plated Steel Hex Head Screws.STEP')
    stepReader.TransferRoot()
    myshape = stepReader.Shape()

    for i in range(0, 360, 15):
        aCompound = renderAngle(myshape, gp_Dir(0., math.cos(math.radians(i)), math.sin(math.radians(i))), False)
        renderer = UpdatedOffscreenRenderer()
        renderer.DisplayShape(aCompound, color="Black", transparency=True, dump_image_path='.', dump_image_filename=f'bolt.png')


def generateLabel():

    # Create a new SVG drawing
    d = draw.Drawing(labelWidth, labelHeight, origin='center')

    # Add border to the label
    addBorder(d)

    addText(d, "M3-8 Screws", "Hex Button")

    render3D(d)

    # Add text to the label
    d.append(draw.Text("Hello World", 0, 0, 10, center=1))

    # Save the drawing to a file
    d.save_svg('label.svg')

    # Save the drawing to a file
    # d.savePng('label.png')


if __name__ == '__main__':

    generateLabel()
    print("Done")
