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
from PIL import Image, ImageMorph, ImageFilter, ImageDraw, ImageFont
import qrcode
import os
import cairosvg
import svgwrite
import math
import sys
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import mm

from updatedOffscreenRenderer import UpdatedOffscreenRenderer
import time
import math

dpi = 300
defaultFont = None

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
    
    d.append(draw.Text(textLine1, fontSize, 0, -marginFromCenter, center=1, style="font-family:Times New Roman"))
    d.append(draw.Text(textLine2, fontSize, 0, marginFromCenter+fontSize, center=1, style="font-family:Times New Roman"))


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

def convert_angles_to_direction(alpha_deg, beta_deg):
    # Convert degrees to radians
    alpha_rad = math.radians(alpha_deg)
    beta_rad = math.radians(beta_deg)

    # Convert spherical coordinates to Cartesian coordinates
    x = math.sin(beta_rad) * math.cos(alpha_rad)
    y = math.sin(beta_rad) * math.sin(alpha_rad)
    z = math.cos(beta_rad)

    # Create the direction
    direction = gp_Dir(x, y, z)

    return direction

def render3D(stepFile, orientation = gp_Dir(1., 0., 0.), hideObstructed = True):

    stepReader = STEPControl_Reader()
    stepReader.ReadFile(stepFile)
    stepReader.TransferRoot()
    myshape = stepReader.Shape()

    try:
        aCompound = renderAngle(myshape, orientation, hideObstructed)
        renderer = UpdatedOffscreenRenderer()
        renderer.DisplayShape(aCompound, color="Black", transparency=True, dump_image_path='.', dump_image_filename="tmp3D.png")
    except ValueError:
        pass

def add3D(d, stepFile, orientation = gp_Dir(1., 0., 0.), hideObstructed = True, margin = 10):

    render3D(stepFile, orientation, hideObstructed)

    keying("tmp3D.png")

    makeLinesThicker("tmp3D.png")

    # Add the rendered image to the label
    imageHeight = (labelHeight-2*margin)
    d.append(draw.Image(-(labelWidth/2) + margin, -(labelHeight/2) + margin, imageHeight, imageHeight, "tmp3D.png"))


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

def generateTestLabel():

    # Create a new SVG drawing
    d = draw.Drawing(labelWidth, labelHeight, origin='center')

    # Add border to the label
    addBorder(d)

    addText(d, "M3", "Nuts")

    add3D(d, "./meca/91028A411_JIS Hex Nut.STEP", gp_Dir(0., -1., -1.), True)

    addQRCode(d, "https://homebox.fly.dev/item/70017760-264e-449f-b0bf-056b349b9bf6")

    # Save the drawing to a file
    d.save_svg('label.svg')
    # d.save_png('label.png')

def getTextSize(text):
    ascent, descent = defaultFont.getmetrics()

    text_width = defaultFont.getmask(text).getbbox()[2]
    text_height = defaultFont.getmask(text).getbbox()[3] + descent

    return (text_width, text_height)

def generateLabel(label):

    widthPoints = int(label["width"] * dpi / 25.4)
    heightPoints = int(label["height"] * dpi / 25.4)
    topLeftRoundedCorner = int(label["topLeftRoundedCorner"] * dpi / 25.4)
    topRightRoundedCorner = int(label["topRightRoundedCorner"] * dpi / 25.4)
    bottomLeftRoundedCorner = int(label["bottomLeftRoundedCorner"] * dpi / 25.4)
    bottomRightRoundedCorner = int(label["bottomRightRoundedCorner"] * dpi / 25.4)

    img = Image.new("RGB", size=(widthPoints, heightPoints), color=(255, 255, 255, 0))

    # Draw the border
    d = ImageDraw.Draw(img)

    lineWidth = 10
    hl = lineWidth/2
    d.line([(topLeftRoundedCorner, hl), (widthPoints-topRightRoundedCorner, hl)] , fill="black", width=lineWidth) 
    d.line([(widthPoints-hl, topRightRoundedCorner), (widthPoints-hl, heightPoints - bottomRightRoundedCorner)] , fill="black", width=lineWidth) 
    d.line([(widthPoints - bottomRightRoundedCorner, heightPoints-hl), (bottomLeftRoundedCorner, heightPoints-hl)] , fill="black", width=lineWidth) 
    d.line([(hl, heightPoints - bottomLeftRoundedCorner), (hl, topLeftRoundedCorner)] , fill="black", width=lineWidth) 

    d.arc([(0, 0), (topLeftRoundedCorner*2, topLeftRoundedCorner*2)], 180, 270, fill="black", width=lineWidth)
    d.arc([(widthPoints-(2*topRightRoundedCorner), 0), (widthPoints, (2*topRightRoundedCorner))], 270, 360, fill="black", width=lineWidth)
    d.arc([(0, heightPoints-(2*bottomLeftRoundedCorner)), (2*bottomLeftRoundedCorner, heightPoints)], 90, 180, fill="black", width=lineWidth)
    d.arc([(widthPoints-(2*bottomRightRoundedCorner), heightPoints-(2*bottomRightRoundedCorner)), (widthPoints, heightPoints)], 0, 90, fill="black", width=lineWidth)

    # Write the text
    l1Width, l1Height = getTextSize(label["textLine1"])
    l2Width, l2Height = getTextSize(label["textLine2"])

    l1PosX = ((widthPoints-l1Width)/2)
    l2PosX = ((widthPoints-l2Width)/2)
    verticalSpacing = ((heightPoints-l1Height-l2Height-lineWidth-lineWidth)/3)

    d.text((l1PosX, verticalSpacing+lineWidth), label["textLine1"], font=defaultFont, fill=(0, 0, 0, 255))
    d.text((l2PosX, l1Height+(2*verticalSpacing)), label["textLine2"], font=defaultFont, fill=(0, 0, 0, 255))

    imagesMargin = (lineWidth+10)
    imagesHeight = (heightPoints - (2*imagesMargin))

    # Render the 3D model
    render3D(label["modelPath"], convert_angles_to_direction(label["alpha"], label["beta"]), label["hideObstructed"])
    keying("tmp3D.png")
    makeLinesThicker("tmp3D.png")

    modelImage = Image.open("tmp3D.png")
    modelImage.thumbnail((imagesHeight, imagesHeight), Image.Resampling.LANCZOS)
    img.paste(modelImage, (imagesMargin, imagesMargin), mask=modelImage)

    # Draw the QR code
    # box_size is the pixel size of each square of the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=0,
    )
    qr.add_data(label["qrCodeUrl"])
    qr.make(fit=True)

    qrCode = qr.make_image(fill_color="black", back_color="white")

    qrCode.thumbnail((imagesHeight, imagesHeight), Image.Resampling.LANCZOS)
    img.paste(qrCode, (widthPoints-imagesHeight-imagesMargin, imagesMargin))

    return img


def generateLabelSheets(labelDataList):

    global defaultFont
    if "font" in labelDataList:
        defaultFont = ImageFont.truetype(labelDataList["font"], 40)
    else:
        defaultFont = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 40)

    labels = []
    for label in labelDataList["stickerList"]:
        labels.append(generateLabel(label))

    sheetWidthPoints = int(labelDataList["pageWidth"] * dpi / 25.4)
    sheetHeightPoints = int(labelDataList["pageHeight"] * dpi / 25.4)

    outSheet = Image.new("RGB", size=(sheetWidthPoints, sheetHeightPoints), color=(255, 255, 255, 0))

    margin = 50
    xOffset = margin
    yOffset = margin
    for i, label in enumerate(labels):
        outSheet.paste(label, (xOffset, yOffset))
        xOffset += 500
        if xOffset >= sheetWidthPoints:
            xOffset = margin
            yOffset += 500

    outSheet.save("out.pdf", save_all=True)

if __name__ == '__main__':

    # generateTestLabel()
    generateLabelSheets({
        "pageWidth": 210,
        "pageHeight": 297,
        "font": "/usr/share/fonts/truetype/msttcorefonts/times.ttf",
        "stickerList": [
            {
                "width": 37,
                "height": 13,
                "topLeftRoundedCorner": 4,
                "topRightRoundedCorner": 4,
                "bottomLeftRoundedCorner": 0,
                "bottomRightRoundedCorner": 0,
                "textLine1": "Stiky 1",
                "textLine2": "Line2",
                "qrCodeUrl": "https://homebox.fly.dev/item/70017760-264e-449f-b0bf-056b349b9bf6",
                "modelPath": "/home/karlito/creation/gridfinity/labelGenerator/meca/91028A411_JIS Hex Nut.STEP",
                "alpha": 120,
                "beta": 87,
                "hideObstructed": True
            },
            {
                "width": 37,
                "height": 13,
                "topLeftRoundedCorner": 4,
                "topRightRoundedCorner": 4,
                "bottomLeftRoundedCorner": 0,
                "bottomRightRoundedCorner": 0,
                "textLine1": "Kikoo",
                "textLine2": "Salut",
                "qrCodeUrl": "https://homebox.fly.dev/item/70017760-264e-449f-b0bf-056b349b9bf6",
                "modelPath": "/home/karlito/creation/gridfinity/labelGenerator/meca/91028A411_JIS Hex Nut.STEP",
                "alpha": 120,
                "beta": 87,
                "hideObstructed": True
            }
        ]
    })
    print("Done")
