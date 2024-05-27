from PySide6 import QtCore, QtWidgets, QtGui

from stickerForm import StickerForm
from sticker import Sticker

class MainWindow(QtWidgets.QMainWindow):

    stickerList = []

    def __init__(self):
        super().__init__()

        self.mainWidget = QtWidgets.QSplitter(self)
        self.setCentralWidget(self.mainWidget)

        # Left part of the layout
        self.leftWidget = QtWidgets.QWidget(self)
        self.leftWidget.layout = QtWidgets.QVBoxLayout(self.leftWidget)
        self.mainWidget.addWidget(self.leftWidget)

        self.stickerList = QtWidgets.QListWidget(self)
        self.stickerList.currentItemChanged.connect(self.refresh)
        self.leftWidget.layout.addWidget(self.stickerList)

        # Control buttons at the bottom left
        self.bottomButtons = QtWidgets.QWidget(self)
        self.bottomButtons.layout = QtWidgets.QHBoxLayout(self.bottomButtons)
        self.bottomButtons.layout.setContentsMargins(0, 0, 0, 0)

        self.addStickerButton = QtWidgets.QPushButton("+", self)
        # self.addStickerButton.setFixedSize(40, 40)
        self.addStickerButton.clicked.connect(self.newSticker)
        self.bottomButtons.layout.addWidget(self.addStickerButton)

        self.deleteStickerButton = QtWidgets.QPushButton("-", self)
        # self.deleteStickerButton.setFixedSize(40, 40)
        self.bottomButtons.layout.addWidget(self.deleteStickerButton)

        self.printButton = QtWidgets.QPushButton("P", self)
        # self.printButton.setFixedSize(40, 40)
        self.bottomButtons.layout.addWidget(self.printButton)

        self.leftWidget.layout.addWidget(self.bottomButtons)

        # Right part of the layout
        self.stickerForm = StickerForm(self)
        self.mainWidget.addWidget(self.stickerForm)

        self.mainWidget.setSizes([20, 80])
        self.resize(800, 500)

        self.show()

        self.newSticker()
        self.newSticker()
        self.newSticker()

    @QtCore.Slot()
    def newSticker(self):
        self.stickerList.addItem(Sticker())

    @QtCore.Slot()
    def refresh(self):
        self.stickerForm.saveData()
        self.stickerForm.loadData(self.stickerList.currentItem())
        