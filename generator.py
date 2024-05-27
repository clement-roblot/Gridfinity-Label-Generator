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
from PIL import Image, ImageMorph, ImageFilter
import qrcode

from updatedOffscreenRenderer import UpdatedOffscreenRenderer
import time
import math

labelWidth = 370
labelHeight = 130



def addBorder(d, strokeSize = 4, margin = 5, topCornerRadius = 30):
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
    fontSize = 25
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
    aBuilder.Add(aCompound, aHLRToShape.OutLineVCompound())     # Is that useful?

    return aCompound


def keying(imagePath, keyColor = (255, 255, 255)):
    img = Image.open(imagePath)
    img = img.convert("RGBA")
    datas = img.getdata()

    tolerance = 10
    newData = []
    for item in datas:
        if item[0] in range(keyColor[0]-tolerance, keyColor[0]+tolerance) and item[1] in range(keyColor[1]-tolerance, keyColor[1]+tolerance) and item[2] in range(keyColor[2]-tolerance, keyColor[2]+tolerance):
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save(imagePath, "PNG")

def makeLinesThicker(imagePath, thickness = 9):
    img = Image.open(imagePath)
    edges = img.filter(ImageFilter.FIND_EDGES)

    if thickness % 2 == 0:
        thickness += 1

    fatEdges = edges.filter(ImageFilter.MaxFilter(thickness))
    datas = fatEdges.getdata()

    newData = []
    for item in datas:
        if item[3] > 128:
            newData.append((0, 0, 0, 255))
        else:
            newData.append(item)

    fatEdges.putdata(newData)
    fatEdges.save(imagePath, "PNG")

def add3D(d, stepFile, orientation = gp_Dir(1., 0., 0.), hideObstructed = True, margin = 10):

    stepReader = STEPControl_Reader()
    stepReader.ReadFile(stepFile)
    stepReader.TransferRoot()
    myshape = stepReader.Shape()

    try:
        aCompound = renderAngle(myshape, orientation, hideObstructed)
        renderer = UpdatedOffscreenRenderer()
        renderer.DisplayShape(aCompound, color="Black", transparency=True, dump_image_path='.', dump_image_filename="tmp3D.png")

        keying("tmp3D.png")

        makeLinesThicker("tmp3D.png")

        # Add the rendered image to the label
        imageHeight = (labelHeight-2*margin)
        d.append(draw.Image(-(labelWidth/2) + margin, -(labelHeight/2) + margin, imageHeight, imageHeight, "tmp3D.png"))

    except ValueError:
        pass

def addQRCode(d, url, margin = 20):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=0,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save("tmpQrCode.png")

    keying("tmpQrCode.png")

    # Add the rendered image to the label
    imageHeight = (labelHeight-1.5*margin)
    marginFromEdge = ((labelHeight-imageHeight)/2)
    d.append(draw.Image((labelWidth/2) - marginFromEdge - imageHeight, -imageHeight/2, imageHeight, imageHeight, "tmpQrCode.png"))

def generateLabel():

    # Create a new SVG drawing
    d = draw.Drawing(labelWidth, labelHeight, origin='center')

    # Add border to the label
    addBorder(d)

    addText(d, "M3", "Nuts")

    add3D(d, "./meca/91028A411_JIS Hex Nut.STEP", gp_Dir(0., -1., -1.), True)

    addQRCode(d, "https://homebox.fly.dev/item/70017760-264e-449f-b0bf-056b349b9bf6")

    # Add text to the label
    d.append(draw.Text("Hello World", 0, 0, 10, center=1))

    # Save the drawing to a file
    d.save_svg('label.svg')

    # Save the drawing to a file
    # d.savePng('label.png')


if __name__ == '__main__':

    generateLabel()
    print("Done")
