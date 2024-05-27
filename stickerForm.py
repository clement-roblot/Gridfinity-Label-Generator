from PySide6 import QtCore, QtWidgets, QtGui


class StickerForm(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QtWidgets.QGridLayout(self)
        currentLayoutLine = 0

        # Sticker size
        self.layout.addWidget(QtWidgets.QLabel("Size:"), currentLayoutLine, 0)
        self.layout.addWidget(QtWidgets.QLabel("width"), currentLayoutLine, 1)
        self.widthField = QtWidgets.QSpinBox(self, minimum=0, maximum=1000, value=37)
        self.layout.addWidget(self.widthField, currentLayoutLine, 2)
        self.layout.addWidget(QtWidgets.QLabel("mm"), currentLayoutLine, 3)
        self.layout.addWidget(QtWidgets.QLabel("height"), currentLayoutLine, 4)
        self.heightField = QtWidgets.QSpinBox(self, minimum=0, maximum=1000, value=13)
        self.layout.addWidget(self.heightField, currentLayoutLine, 5)
        self.layout.addWidget(QtWidgets.QLabel("mm"), currentLayoutLine, 6)

        currentLayoutLine += 1

        # Rounded corners top
        self.layout.addWidget(QtWidgets.QLabel("Top corner:"), currentLayoutLine, 0)
        self.layout.addWidget(QtWidgets.QLabel("left"), currentLayoutLine, 1)
        self.topLeftRoundedCorner = QtWidgets.QSpinBox(self, minimum=0, maximum=100, value=4)
        self.layout.addWidget(self.topLeftRoundedCorner, currentLayoutLine, 2)
        self.layout.addWidget(QtWidgets.QLabel("mm"), currentLayoutLine, 3)
        self.layout.addWidget(QtWidgets.QLabel("rigth"), currentLayoutLine, 4)
        self.topRightRoundedCorner = QtWidgets.QSpinBox(self, minimum=0, maximum=100, value=4)
        self.layout.addWidget(self.topRightRoundedCorner, currentLayoutLine, 5)
        self.layout.addWidget(QtWidgets.QLabel("mm"), currentLayoutLine, 6)

        currentLayoutLine += 1

        # Rounded corners bottom
        self.layout.addWidget(QtWidgets.QLabel("Bottom corner:"), currentLayoutLine, 0)
        self.layout.addWidget(QtWidgets.QLabel("left"), currentLayoutLine, 1)
        self.bottomLeftRoundedCorner = QtWidgets.QSpinBox(self, minimum=0, maximum=100, value=0)
        self.layout.addWidget(self.bottomLeftRoundedCorner, currentLayoutLine, 2)
        self.layout.addWidget(QtWidgets.QLabel("mm"), currentLayoutLine, 3)
        self.layout.addWidget(QtWidgets.QLabel("rigth"), currentLayoutLine, 4)
        self.bottomRightRoundedCorner = QtWidgets.QSpinBox(self, minimum=0, maximum=100, value=0)
        self.layout.addWidget(self.bottomRightRoundedCorner, currentLayoutLine, 5)
        self.layout.addWidget(QtWidgets.QLabel("mm"), currentLayoutLine, 6)

        currentLayoutLine += 1

        # Lines of text
        self.layout.addWidget(QtWidgets.QLabel("Line 1:"), currentLayoutLine, 0)
        self.textLine1 = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.textLine1, currentLayoutLine, 1, 1, -1)

        currentLayoutLine += 1

        self.layout.addWidget(QtWidgets.QLabel("Line 2:"), currentLayoutLine, 0)
        self.textLine2 = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.textLine2, currentLayoutLine, 1, 1, -1)

        currentLayoutLine += 1

        # QR Code URL
        self.layout.addWidget(QtWidgets.QLabel("QR code:"), currentLayoutLine, 0)
        self.qrCodeUrl = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.qrCodeUrl, currentLayoutLine, 1, 1, -1)

        currentLayoutLine += 1

        # 3D model
        self.layout.addWidget(QtWidgets.QLabel("3D model:"), currentLayoutLine, 0)
        self.modelPath = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.modelPath, currentLayoutLine, 1, 1, 5)
        self.modelBrowsButton = QtWidgets.QPushButton(self, text="Browse")
        self.layout.addWidget(self.modelBrowsButton, currentLayoutLine, 6)

        currentLayoutLine += 1

        # 3D view
        self.graphicsView = QtWidgets.QGraphicsView(self)
        self.scene = QtWidgets.QGraphicsScene(self)
        self.graphicsView.setScene(self.scene)
        self.layout.addWidget(self.graphicsView, currentLayoutLine, 0, 4, 4)

        # Load PNG image from disk (temporary)
        pixmap = QtGui.QPixmap("/home/karlito/creation/gridfinity/labelGenerator/tmp3D.png")
        self.scene.addPixmap(pixmap)
        self.graphicsView.fitInView(self.scene.itemsBoundingRect(), QtCore.Qt.KeepAspectRatio)

        # 3d view controls
        self.layout.addWidget(QtWidgets.QLabel("Pitch:"), currentLayoutLine, 4)
        self.pitchSlider = QtWidgets.QSlider(self, orientation=QtCore.Qt.Horizontal)
        self.layout.addWidget(self.pitchSlider, currentLayoutLine, 5, 1, 2)
        
        self.layout.addWidget(QtWidgets.QLabel("Roll:"), currentLayoutLine+1, 4)
        self.rollSlider = QtWidgets.QSlider(self, orientation=QtCore.Qt.Horizontal)
        self.layout.addWidget(self.rollSlider, currentLayoutLine+1, 5, 1, 2)

        self.layout.addWidget(QtWidgets.QLabel("Yaw:"), currentLayoutLine+2, 4)
        self.yawSlider = QtWidgets.QSlider(self, orientation=QtCore.Qt.Horizontal)
        self.layout.addWidget(self.yawSlider, currentLayoutLine+2, 5, 1, 2)

        self.hideObstructedCheckbox = QtWidgets.QCheckBox(self, text="Hide obstructed lines", checked=True)
        self.layout.addWidget(self.hideObstructedCheckbox, currentLayoutLine+3, 4, 1, 3)


