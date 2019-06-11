# -*- coding: utf-8 -*-
# @Time : 2019/5/8 11:34
# @Author : EricNiu
# @FileName: MainWindow.py
# @Software: PyCharm
# Created by: PyQt5 UI code generator 5.11.3

import sys
from PyQt5 import QtCore, QtWidgets
from Akuma import *


class UiMainWindow(object):
    # Qt自动生成的前端 不用管
    def __init__(self):
        super().__init__()
        self.mode_select = 0
        self.auto_run = None
        self.tmp_run = None
        self.stop_flag = 0

    def setup_ui(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(300, 230)
        MainWindow.setFocusPolicy(QtCore.Qt.TabFocus)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")


        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(180, 20, 115, 30))
        self.radioButton.setObjectName("radioButton")
        self.radioButton.toggled.connect(lambda: self.select_handle(self.radioButton))

        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setGeometry(QtCore.QRect(180, 50, 115, 30))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_2.toggled.connect(lambda: self.select_handle(self.radioButton_2))

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(180, 140, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.toggle()
        self.pushButton.clicked.connect(lambda: self.start_click_handle())

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(180, 180, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(lambda: self.stop_click_handle())

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(180, 100, 93, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(lambda: self.create_template())

        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(20, 20, 140, 190))
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setText("あれは誰だ 誰だ 誰だ" + "\n" + "あれはデビル デビルマン デビルマン")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "恶魔の力"))

        self.radioButton.setText(_translate("MainWindow", "组队模式"))
        self.radioButton_2.setText(_translate("MainWindow", "业/灵/单"))
        self.pushButton.setText(_translate("MainWindow", "开始"))
        self.pushButton_2.setText(_translate("MainWindow", "停止"))
        self.pushButton_3.setText(_translate("MainWindow", "制作模板"))

    def select_handle(self, btn):
        if btn.text() == "组队模式":
            if btn.isChecked() and btn.isCheckable():
                self.textBrowser.setText("组队模式，队长或队员都可以。")
                self.auto_run = Team()
                self.mode_select = 1

        if btn.text() == "业/灵/单":
            if btn.isChecked() and btn.isCheckable():
                self.textBrowser.setText("单刷业原火/御灵/八岐大蛇。")
                self.auto_run = Solo()
                self.mode_select = 2

    def start_click_handle(self):
        self.stop_flag = 0
        if self.mode_select == 0:
            self.textBrowser.setText("错误:没有选择模式")
        else:
            self.pushButton_3.setHidden(True)
            if self.mode_select == 1:
                self.radioButton_2.setHidden(True)
            elif self.mode_select == 2:
                self.radioButton.setHidden(True)

            try:
                self.auto_run.start()
            except IndexError:
                self.stop_flag = 1
                self.textBrowser.setText("错误:无法捕获游戏窗口，请确认游戏运行。")
            except pygetwindow.PyGetWindowException:
                self.stop_flag = 1
                self.textBrowser.setText("错误:无法捕获游戏窗口，请确认是否取得管理员权限。")

            while True:
                if self.stop_flag == 1:
                    break
                else:
                    try:
                        self.auto_run.capture()
                    except OSError:
                        # 部分情况下程序会失去截图的权限发生错误 比如有UAC弹窗的时候
                        self.textBrowser.setText("错误:发生未知意外，程序中断，请重新开始。")
                        break
                    # 截取样本-判断-打印结果-处理结果 循环
                    QtWidgets.QApplication.processEvents()
                    self.auto_run.judge()
                    QtWidgets.QApplication.processEvents()
                    self.textBrowser.setText(self.auto_run.ready_info + "\n" + self.auto_run.finish_info)
                    QtWidgets.QApplication.processEvents()
                    self.auto_run.handle()
                    QtWidgets.QApplication.processEvents()
                    time.sleep(0.6)  # 这里其实是采样频率
                    QtWidgets.QApplication.processEvents()

    def stop_click_handle(self):
        self.textBrowser.setText("あれは誰だ 誰だ 誰だ" + "\n" + "あれはデビル デビルマン デビルマン")
        self.pushButton_3.setHidden(False)
        self.radioButton.setHidden(False)
        self.radioButton_2.setHidden(False)
        self.stop_flag = 1

    def create_template(self):
        self.tmp_run = Team()
        try:
            self.tmp_run.start()
        except IndexError:
            self.textBrowser.setText("错误:无法捕获游戏窗口，请确认游戏运行。")
        except pygetwindow.PyGetWindowException:
            self.textBrowser.setText("错误:无法捕获游戏窗口，请确认是否取得管理员权限。")

        time.sleep(0.3)
        QtWidgets.QApplication.processEvents()

        try:
            self.tmp_run.capture_template()
        except AttributeError:
            self.textBrowser.setText("错误:捕获游戏窗口失败，请确认游戏正常运行。")
        except OSError:
            self.textBrowser.setText("错误:发生未知意外，程序中断，请稍后重试。")
        else:
            QtWidgets.QApplication.processEvents()
            self.textBrowser.setText("模板截图完成" + "\n" + "请将合适的模板重命名后移动至source文件夹。")
            del self.tmp_run


if __name__ == '__main__':
    print("前端和一些逻辑")
