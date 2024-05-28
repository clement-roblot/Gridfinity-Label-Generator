from PySide6 import QtCore, QtWidgets, QtGui
import json

from stickerForm import StickerForm
from sticker import Sticker

class MainWindow(QtWidgets.QMainWindow):

    stickerList = []
    pageWidth = 210
    pageHeight = 297
    currentFileName = ""

    def __init__(self):
        super().__init__()

        self.mainWidget = QtWidgets.QSplitter(self)
        self.setCentralWidget(self.mainWidget)

        self.menuBar = self.menuBar()
        fileMenu = self.menuBar.addMenu("&File")

        # New File Action
        newAction = QtGui.QAction("&New", self)
        newAction.setShortcut("Ctrl+N")
        newAction.triggered.connect(self.newFile)
        fileMenu.addAction(newAction)

        # Open File Action
        openAction = QtGui.QAction("&Open...", self)
        openAction.setShortcut("Ctrl+O")
        openAction.triggered.connect(self.openFile)
        fileMenu.addAction(openAction)

        # Save File Action
        saveAction = QtGui.QAction("&Save", self)
        saveAction.setShortcut("Ctrl+S")
        saveAction.triggered.connect(self.saveFile)
        fileMenu.addAction(saveAction)

        # Save as File Action
        saveAction = QtGui.QAction("&Save as...", self)
        saveAction.setShortcut("Ctrl+S")
        saveAction.triggered.connect(self.saveAsFile)
        fileMenu.addAction(saveAction)

        # Export Action
        exportAction = QtGui.QAction("&Export as pdf", self)
        exportAction.setShortcut("Ctrl+E")
        exportAction.triggered.connect(self.exportFile)
        fileMenu.addAction(exportAction)

        # Quit Action
        quitAction = QtGui.QAction("&Quit", self)
        quitAction.setShortcut("Ctrl+Q")
        quitAction.triggered.connect(self.closeApp)
        fileMenu.addAction(quitAction)

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
        self.addStickerButton.setFixedSize(40, 40)
        self.addStickerButton.clicked.connect(self.newSticker)
        self.bottomButtons.layout.addWidget(self.addStickerButton)

        self.deleteStickerButton = QtWidgets.QPushButton("-", self)
        self.deleteStickerButton.setFixedSize(40, 40)
        self.deleteStickerButton.clicked.connect(self.deleteSticker)
        self.bottomButtons.layout.addWidget(self.deleteStickerButton)

        self.printButton = QtWidgets.QPushButton("🖨️", self)
        self.printButton.setFixedSize(40, 40)
        self.printButton.clicked.connect(self.exportFile)
        self.bottomButtons.layout.addWidget(self.printButton)

        self.leftWidget.layout.addWidget(self.bottomButtons)

        # Right part of the layout
        self.stickerForm = StickerForm(self)
        self.mainWidget.addWidget(self.stickerForm)

        self.mainWidget.setSizes([20, 80])
        self.resize(800, 500)

        self.show()

        self.newSticker()

    @QtCore.Slot()
    def newFile(self):
        self.currentFileName = ""
        self.stickerList.clear()
        self.stickerForm.loadData(None)

    @QtCore.Slot()
    def openFile(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "",
                                                  "JSON Files (*.json)", options=options)
        if fileName:
            self.loadFromFile(fileName)
    
    @QtCore.Slot()
    def saveFile(self):

        if self.currentFileName == "":
            self.saveAsFile()
        else:
            self.saveToFile(self.currentFileName)

    @QtCore.Slot()
    def saveAsFile(self):

        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "",
                                                  "JSON Files (*.json)", options=options)
        if fileName:
            self.saveToFile(fileName)

    def loadFromFile(self, fileName):
        with open(fileName, 'r') as file:

            self.currentFileName = fileName
            self.stickerList.clear()
            self.stickerForm.loadData(None)

            data = json.load(file)
            self.pageWidth = data["pageWidth"]
            self.pageHeight = data["pageHeight"]
            self.stickerList.clear()
            for stickerData in data["stickerList"]:
                self.stickerList.addItem(Sticker(stickerData))


    def saveToFile(self, fileName):
        dataDict = {
            "pageWidth": self.pageWidth,
            "pageHeight": self.pageHeight,
            "stickerList": []
        }

        for i in range(self.stickerList.count()):
            dataDict["stickerList"].append(self.stickerList.item(i).getJson())

        if fileName:
            with open(fileName, 'w') as file:
                json.dump(dataDict, file, indent=4)
                self.currentFileName = fileName

    @QtCore.Slot()
    def exportFile(self):
        print("Export PDF")

    @QtCore.Slot()
    def closeApp(self):
        self.close()

    @QtCore.Slot()
    def newSticker(self):
        self.stickerList.addItem(Sticker())

    @QtCore.Slot()
    def deleteSticker(self):
        if self.stickerList.currentItem() is not None:
            self.stickerList.takeItem(self.stickerList.currentRow())

    @QtCore.Slot()
    def refresh(self):
        if self.stickerList.currentItem() is not None:
            self.stickerForm.saveData()
            self.stickerForm.loadData(self.stickerList.currentItem())
