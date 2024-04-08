#!/usr/bin/env python3
import drawsvg as draw
from OCC.Core.HLRBRep import HLRBRep_Algo, HLRBRep_HLRToShape
from OCC.Core.HLRAlgo import HLRAlgo_Projector
from OCC.Core.gp import gp_Ax2, gp_Pnt, gp_Dir
from OCC.Core.TopoDS import TopoDS_Compound
from OCC.Core.BRep import BRep_Builder
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Display.SimpleGui import init_display


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


def addNut(d):
    # Add drawing of a mechanical nut to the label
    nutRadius = 5

    # https://dev.opencascade.org/content/cad-file-2d-projection-how-get-just-outlining-edges
    # https://stackoverflow.com/questions/66929762/extract-volume-from-a-step-file
    # https://forum.freecad.org/viewtopic.php?t=79648&start=10

    # Using anaconda: http://analysissitus.org/forum/index.php?threads/pythonocc-getting-started-guide.19/

    # Handle(HLRBRep_Algo) myAlgo = new HLRBRep_Algo();
    # HLRAlgo_Projector aProjector = HLRAlgo_Projector(gp_Ax2(gp_Pnt(0., y1, shapeCenterHeight), gp_Dir(0., 1., 0)));
    # myAlgo->Add(shape);
    # myAlgo->Projector(aProjector);
    # myAlgo->Update();
    # myAlgo->Hide();

    # HLRBRep_HLRToShape aHLRToShape(myAlgo);

    # TopoDS_Compound aCompound;
    # BRep_Builder aBuilder;
    # aBuilder.MakeCompound(aCompound);
    # aBuilder.Add(aCompound, aHLRToShape.VCompound());
    # aBuilder.Add(aCompound, aHLRToShape.OutLineVCompound();

    # Handle(AIS_Shape) HNDL_spheres = new AIS_Shape(compoundShape);
    # myContext->Display(HNDL_spheres,1,-1,false,false);


    # TODO: This looks usefull: get_sorted_hlr_edges

    stepReader = STEPControl_Reader()
    stepReader.ReadFile('./meca/91255A008_Button Head Hex Drive Screw.STEP')
    stepReader.TransferRoot()
    myshape = stepReader.Shape()

    myAlgo = HLRBRep_Algo()
    aProjector = HLRAlgo_Projector(gp_Ax2(gp_Pnt(0., 0, 0), gp_Dir(0., 1., 0)))
    myAlgo.Add(myshape)
    myAlgo.Projector(aProjector)
    myAlgo.Update()
    myAlgo.Hide()

    aHLRToShape = HLRBRep_HLRToShape(myAlgo)

    aCompound = TopoDS_Compound()
    aBuilder = BRep_Builder()
    aBuilder.MakeCompound(aCompound)
    aBuilder.Add(aCompound, aHLRToShape.VCompound())
    aBuilder.Add(aCompound, aHLRToShape.OutLineVCompound())


    display, start_display, add_menu, add_function_to_menu = init_display()
    
    display.DisplayShape(aCompound, update=True)

    start_display()







    







    

def generateLabel():

    # Create a new SVG drawing
    d = draw.Drawing(labelWidth, labelHeight, origin='center')

    # Add border to the label
    addBorder(d)

    addText(d, "M3-8 Screws", "Hex Button")

    addNut(d)

    # Add text to the label
    d.append(draw.Text("Hello World", 0, 0, 10, center=1))

    # Save the drawing to a file
    d.save_svg('label.svg')

    # Save the drawing to a file
    # d.savePng('label.png')


if __name__ == '__main__':

    generateLabel()
    print("Done")
