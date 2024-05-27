from PySide6 import QtCore, QtWidgets, QtGui


class StickerForm(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QtWidgets.QVBoxLayout(self)

        self.testLabel = QtWidgets.QLabel("Test label")

        self.layout.addWidget(self.testLabel)




