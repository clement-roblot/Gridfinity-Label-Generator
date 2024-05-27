from PySide6 import QtCore, QtWidgets, QtGui

from stickerForm import StickerForm

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.mainWidget = QtWidgets.QSplitter(self)
        self.setCentralWidget(self.mainWidget)

        # Left part of the layout
        self.leftWidget = QtWidgets.QWidget(self)
        self.leftWidget.layout = QtWidgets.QVBoxLayout(self.leftWidget)
        self.mainWidget.addWidget(self.leftWidget)

        self.stickerList = QtWidgets.QListWidget(self)
        self.stickerList.addItem("Sticker 1")
        self.stickerList.addItem("Sticker 2")
        self.stickerList.addItem("Sticker 3")

        self.leftWidget.layout.addWidget(self.stickerList)

        # Control buttons at the bottom left
        self.bottomButtons = QtWidgets.QWidget(self)
        self.bottomButtons.layout = QtWidgets.QHBoxLayout(self.bottomButtons)

        self.addStickerButton = QtWidgets.QPushButton("+", self)
        self.bottomButtons.layout.addWidget(self.addStickerButton)

        self.deleteStickerButton = QtWidgets.QPushButton("-", self)
        self.bottomButtons.layout.addWidget(self.deleteStickerButton)

        self.printButton = QtWidgets.QPushButton("P", self)
        self.bottomButtons.layout.addWidget(self.printButton)

        self.leftWidget.layout.addWidget(self.bottomButtons)

        # Right part of the layout
        self.stickerForm = StickerForm(self)
        self.mainWidget.addWidget(self.stickerForm)

        self.mainWidget.setSizes([20, 80])
        self.resize(1200, 700)

        self.show()
