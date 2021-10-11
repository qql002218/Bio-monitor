#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
增加 图标

增加 按钮

按钮事件绑定

消息框

界面中心化
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QPushButton
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口的大小
        self.setGeometry(300, 300, 300, 300)  # 坐标
        # 设置窗口标题
        self.setWindowTitle('BIO-monitor')
        # 设置窗口图标
        self.setWindowIcon(QIcon('../AVI_process/dijia.png'))

        self.center()

        # 静态方法设置显示工具提示的字体
        QToolTip.setFont(QFont('SansSerif', 10))
        # self.setToolTip('this is a <b>QWeight</b> wight')

        # 创建一个btn
        btn = QPushButton('Button', self)  # 第一个参数是为按钮命名  第二个是关联点击对象
        btn.setToolTip('this is a <b>BTN</b> wight')
        btn.move(50, 200)
        # 创建一个退出按钮
        qbtn = QPushButton('QuitBtn', self)
        qbtn.resize(qbtn.sizeHint())
        qbtn.clicked.connect(QCoreApplication.instance().quit)  # 点击事件绑定
        qbtn.move(200, 200)

        btn.resize(btn.sizeHint())
        # 显示窗口
        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', '确定要退出吗?', QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # 将窗口固定到界面的中心
    def center(self):
        # 获得窗口
        qr = self.frameGeometry()
        # 获得屏幕的中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 显示到屏幕的中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    # 创建应用程序和对象
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
