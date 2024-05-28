#!/usr/bin/env python3
import drawsvg as draw
from OCC.Core.HLRBRep import HLRBRep_Algo, HLRBRep_HLRToShape
from OCC.Core.HLRAlgo import HLRAlgo_Projector
from OCC.Core.gp import gp_Ax2, gp_Pnt, gp_Dir
from OCC.Core.TopoDS import TopoDS_Compound
from OCC.Core.BRep import BRep_Builder
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.TopoDS import TopoDS_Compound
from OCC.Core.BRep import BRep_Builder
from PIL import Image, ImageFilter, ImageDraw, ImageFont, ImageOps
import qrcode
import os
import math
import sys
import time
import json

from updatedOffscreenRenderer import UpdatedOffscreenRenderer

dpi = 300
defaultFont = None

def renderAngle(shape, orientation = gp_Dir(1., 0., 0.), hideObstructed = True):

    myAlgo = HLRBRep_Algo() # 0.00s

    # orientation sets the orientation of the Z vector
    # X and Y are automaticaly calculated but those are the ones going crazy
    # this is why we set the X dir to be fixed to gp_Dir(1., 0., 0.)
    aProjector = HLRAlgo_Projector(gp_Ax2(gp_Pnt(0., 0, 0), orientation, gp_Dir(1., 0., 0.))) # 0.00s
    myAlgo.Add(shape) # 0.00s
    myAlgo.Projector(aProjector) # 0.00s

    myAlgo.Update() # 0.03s

    if hideObstructed:
        myAlgo.Hide()       # Hide the obsructed lines (very slow!) : 1.36s

    aHLRToShape = HLRBRep_HLRToShape(myAlgo) # 0.00s

    aCompound = TopoDS_Compound() # 0.00s
    aBuilder = BRep_Builder() # 0.00s
    aBuilder.MakeCompound(aCompound) # 0.00s
    aBuilder.Add(aCompound, aHLRToShape.VCompound()) # 0.00s
    aBuilder.Add(aCompound, aHLRToShape.OutLineVCompound())     # Is that useful? 0.00s

    return aCompound

def makeLinesThicker(imagePath):

    img = Image.open(imagePath)
    img = img.convert("L")

    edges = img.filter(ImageFilter.FIND_EDGES)

    # Remove 1px border around the image edges
    # Because the edge detection triggers on the edges of the image
    edges = edges.crop((1, 1, edges.width - 1, edges.height - 1))

    thickness = 5
    matrix = [1] * thickness**2

    # Run twice becaus PIL doesn't allow kernels bigger than 5x5
    edges = edges.filter(ImageFilter.Kernel((thickness, thickness), matrix, 1, 0))
    edges = edges.filter(ImageFilter.Kernel((thickness, thickness), matrix, 1, 0))

    edges = ImageOps.invert(edges)

    return edges

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

    start_time = time.time()

    stepReader = STEPControl_Reader()       # 0.00s
    stepReader.ReadFile(stepFile)       # 0.00s
    stepReader.TransferRoot()       # 0.04s
    myshape = stepReader.Shape()    # 0.00s

    try:
        aCompound = renderAngle(myshape, orientation, hideObstructed)   # 1.39
        renderer = UpdatedOffscreenRenderer()   # 0.03s
        renderer.DisplayShape(aCompound, color="Black", transparency=True, dump_image_path='.', dump_image_filename="tmp3D.png")    # 0.03s
    except ValueError:
        pass

def getTextSize(text):

    global defaultFont

    if text == "":
        return (0, 0)

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
    print(f"top left {topLeftRoundedCorner}")
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

    global defaultFont
    d.text((l1PosX, verticalSpacing+lineWidth), label["textLine1"], font=defaultFont, fill=(0, 0, 0, 255))
    d.text((l2PosX, l1Height+(2*verticalSpacing)), label["textLine2"], font=defaultFont, fill=(0, 0, 0, 255))

    imagesMargin = (lineWidth+10)
    imagesHeight = (heightPoints - (2*imagesMargin))

    # Render the 3D model
    render3D(label["modelPath"], convert_angles_to_direction(label["alpha"], label["beta"]), label["hideObstructed"])   # 1.6s

    modelImage = makeLinesThicker("tmp3D.png")   # 0.49s

    modelImage.thumbnail((imagesHeight, imagesHeight), Image.Resampling.LANCZOS)
    img.paste(modelImage, (imagesMargin, imagesMargin))

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


def generateLabelSheets(labelDataList, dstPath="out.pdf"):

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

    outSheet.save(dstPath, save_all=True)

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("Usage: python3 generator.py <config file>")
        sys.exit(1)

    config_file = sys.argv[1]
    with open(config_file, 'r') as file:
        config_data = json.load(file)
    
        generateLabelSheets(config_data)

    print("Done")
