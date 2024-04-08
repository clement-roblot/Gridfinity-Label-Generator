from OCC.Display.SimpleGui import init_display
from OCC.Extend.DataExchange import read_step_file

display, start_display, add_menu, add_function_to_menu = init_display()

# load step file
the_shape = read_step_file("./meca/91255A008_Button Head Hex Drive Screw.STEP")
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


add_menu("camera")
add_function_to_menu("camera", animate_viewpoint)

start_display()