#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
增加对话框
"""
import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QInputDialog, QLineEdit, QApplication


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.btn = QPushButton('Dialog', self) #由于要在类中复用btn 与linetext，在此定义为类对象
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.showDialog) #按钮绑定事件
        self.le = QLineEdit(self)
        self.le.move(130, 22)

        self.setGeometry(300, 300, 290,150)
        self.setWindowTitle('Input Dialog')
        self.show()

    def showDialog(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter your name')
        if ok:
            self.le.setText(str(text))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
