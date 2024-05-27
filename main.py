#!/usr/bin/env python3

import sys
from PySide6 import QtWidgets

import mainWindow


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    
    widget = mainWindow.MainWindow()

    sys.exit(app.exec())
