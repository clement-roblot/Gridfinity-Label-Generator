from OCC.Display.SimpleGui import init_display
from OCC.Extend.DataExchange import read_step_file
from OCC.Core.HLRBRep import HLRBRep_Algo, HLRBRep_HLRToShape

display, start_display, add_menu, add_function_to_menu = init_display("pyside6")

# load step file
the_shape = read_step_file("./meca/91028A411_JIS Hex Nut.STEP")

myAlgo = HLRBRep_Algo()
myAlgo.Add(the_shape)
myAlgo.Update()

aHLRToShape = HLRBRep_HLRToShape(myAlgo)
o = aHLRToShape.OutLineVCompound3d()

display.DisplayShape(the_shape)


def animate_viewpoint():
    display.FitAll()
    display.Context.UpdateCurrentViewer()

    cam = display.View.Camera()  # type: Graphic3d_Camera

    center = cam.Center()
    eye = cam.Eye()

    for i in range(100):
        eye.SetY(eye.Y() + i)
        cam.SetEye(eye)
        display.View.ZFitAll()
        display.Context.UpdateCurrentViewer()

    for i in range(100):
        center.SetZ(center.Z() + i)
        cam.SetCenter(center)
        display.View.ZFitAll()
        display.Context.UpdateCurrentViewer()


def print_xy_click(shp, *kwargs):
    for shape in shp:
        print("Shape selected: ", shape)
    print(kwargs)



# add_menu("camera")
#add_function_to_menu("camera", animate_viewpoint)

display.register_select_callback(print_xy_click)


start_display()