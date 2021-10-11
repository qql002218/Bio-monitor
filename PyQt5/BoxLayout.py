#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
布局管理之框布局
这一块了解了原理，但是后边可能用不到
"""
import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication

# 关键的两个类： QHBoxLayout, QVBoxLayout 这一块是相对于之前的绝对布局，如果我们拉动窗口的大小，画布上的units位置会不变 这个是相对的

"""
操作方法：
创建一个hbox：行  之前加一个弹性因子 addStretch(1)，后续的两个按钮会被挤压在右侧 在行处增加两个button， 
创建一个vbox： 列 先加一个弹性因子addStretch（1），在在列增加行，保证行被积压在下侧，由此实现两个按钮在右下角
"""


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        okbtn = QPushButton("ok", self)
        cancel = QPushButton("cancel", self)
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okbtn)
        hbox.addWidget(cancel)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle("buttons")
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
