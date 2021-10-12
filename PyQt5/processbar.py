#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
增加进度条
"""

import sys
from PyQt5.QtWidgets import QWidget, QProgressBar, QPushButton, QApplication, QLabel, QInputDialog
from PyQt5.QtCore import QBasicTimer
import time


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.btn = QPushButton('start', self)
        self.pbar = QProgressBar(self)
        self.btn2 = QPushButton('set time', self)

        self.initUI()
        self.flag =0 #时间变量
        self.step = 0
        self.timer = QBasicTimer()


    def initUI(self):

        self.pbar.setGeometry(30, 200, 200, 25)
        self.btn.move(30, 250)
        self.btn.clicked.connect(self.doAction)
        self.btn2.move(150,250)
        self.btn2.clicked.connect(self.showDialog) ##控制时间的按钮进行action绑定

        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('proceess bar')
        self.show()

    def timerEvent(self, e):
        if self.step >= 100:
            self.timer.stop()

            self.btn.setText('finish')
            return
        time.sleep(self.flag/100) #控制时间的精髓所在 以为进度条是100份，时间/100份，协同进度条步进

        self.step = self.step + 1
        self.pbar.setValue(self.step)

    def doAction(self):
        if self.timer.isActive():
            self.timer.stop()
            self.btn.setText('start')
        else:
            self.timer.start(100, self)
            self.btn.setText('stop')

    def showDialog(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter your time') #可以作为控制视频捕捉时间的进度条
        if ok:
            self.flag = int(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
