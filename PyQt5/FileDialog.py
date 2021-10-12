#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
增加文本读取框，可用于后期的日志读取
"""
import sys
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QFileDialog, QApplication
from PyQt5.QtGui import QIcon


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.textEidt = QTextEdit()
        self.setCentralWidget(self.textEidt)

        self.statusBar()

        openFile = QAction(QIcon('../AVI_process/dijia.png'),'Open',self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new file')
        openFile.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(openFile)

        self.setGeometry(300,300,300,300)
        self.setWindowTitle('File Dialog')
        self.show()


    def showDialog(self):

        fname = QFileDialog.getOpenFileName(self,'OpenFile','/home')
        if fname[0]:
            f = open(fname[0],'r')

            with f:
                data = f.read()
                self.textEidt.setText(data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
