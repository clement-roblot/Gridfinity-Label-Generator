from OCC.Display.OCCViewer import Viewer3d
from OCC.Core.Graphic3d import Graphic3d_Camera
import time
import os

# This is a temporary fix to still use the old 7.7.2 lib of OCC
# and still get some proper direct export to file like on the master branch of OCC


class UpdatedOffscreenRenderer(Viewer3d):
    """The offscreen renderer is inherited from Viewer3d.
    The DisplayShape method is overridden to export to image
    each time it is called.
    """

    def __init__(self, screen_size=(1080, 1080)):
        Viewer3d.__init__(self)
        # create the renderer
        self.Create()
        self.SetSize(screen_size[0], screen_size[1])
        self.SetModeShaded()
        self.set_bg_gradient_color([255, 255, 255], [255, 255, 255])
        
        # self.display_triedron()
        self.capture_number = 0

    def DisplayShape(
        self,
        shapes,
        material=None,
        texture=None,
        color=None,
        transparency=None,
        update=True,
        dump_image=True,
        dump_image_path=None,
        dump_image_filename=None,
    ):
        # call the "original" DisplayShape method
        r = super(UpdatedOffscreenRenderer, self).DisplayShape(
            shapes, material, texture, color, transparency, update
        )  # always update

        cam = self.View.Camera()
        center = cam.Center()

        cam.SetProjectionType(Graphic3d_Camera.Projection_Orthographic)

        eye = cam.Eye()
        eye.SetX(0.0)
        eye.SetZ(0.0)
        eye.SetZ(100.0)
        cam.SetEye(eye)

        self.View.FitAll()

        if dump_image or (
            os.getenv("PYTHONOCC_OFFSCREEN_RENDERER_DUMP_IMAGE") == "1"
        ):  # dump to jpeg file
            timestamp = ("%f" % time.time()).split(".")[0]

            if os.getenv("PYTHONOCC_OFFSCREEN_RENDERER_DUMP_IMAGE_PATH"):
                path = os.getenv("PYTHONOCC_OFFSCREEN_RENDERER_DUMP_IMAGE_PATH")
                if not os.path.isdir(path):
                    raise IOError(f"{path} is not a valid path")
            elif dump_image_path is not None:
                if not os.path.isdir(dump_image_path):
                    raise IOError(f"{dump_image_path} is not a valid path")
                path = dump_image_path
            else:
                path = os.getcwd()
            if dump_image_filename is None:
                self.capture_number += 1
                image_filename = "capture-%i-%s.jpeg" % (
                    self.capture_number,
                    timestamp.replace(" ", "-"),
                )
                image_full_name = os.path.join(path, image_filename)
            else:
                image_full_name = os.path.join(path, dump_image_filename)
            self.View.Dump(image_full_name)
            if not os.path.isfile(image_full_name):
                raise IOError("OffscreenRenderer failed to render image to file")
            print(f"OffscreenRenderer content dumped to {image_full_name}")
        return r
