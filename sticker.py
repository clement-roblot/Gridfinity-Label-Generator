from PySide6 import QtCore, QtWidgets, QtGui


class Sticker(QtWidgets.QListWidgetItem):

    width = 37
    height = 13

    topLeftRoundedCorner = 4
    topRightRoundedCorner = 4
    bottomLeftRoundedCorner = 0
    bottomRightRoundedCorner = 0

    textLine1 = ""
    textLine2 = ""
    qrCodeUrl = ""
    modelPath = "/home/karlito/creation/gridfinity/labelGenerator/meca/91028A411_JIS Hex Nut.STEP"

    pitch = 0
    roll = 0
    yaw = 0
    
    hideObstructed = True

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setText("Sticker")

    @QtCore.Slot()
    def valueChanged(self):

        if self.textLine1 == "":
            self.setText("Sticker")
            return
        
        self.setText(self.textLine1 + " " + self.textLine2)

