#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
增加状态栏，菜单栏
"""

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QTextEdit, QAction
from PyQt5.QtGui import QIcon


class Example(QMainWindow):  # 这里继承的是QMainWindow
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        textEdit = QTextEdit()
        self.setCentralWidget(textEdit)

        exitActioon = QAction(QIcon('../AVI_process/dijia.png'), 'EXIT', self)  # 增加图标，动作的名称
        exitActioon.setShortcut('Ctrl+Q')  # 动作快捷键
        exitActioon.setStatusTip('Exit application')  # 底部状态显示
        exitActioon.triggered.connect(self.close)  # 动作本体

        self.statusBar()  # 状态条，文本格式

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitActioon)
        ha = menubar.addMenu('&Haha')
        ha.addAction(exitActioon)

        toolbar = self.addToolBar('Exit')  # 工作条 带ui的
        toolbar.addAction(exitActioon)

        self.setGeometry(300, 300, 350, 250)

        self.setWindowTitle('StatusBar')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
