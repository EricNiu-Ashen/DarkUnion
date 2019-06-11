# -*- coding: utf-8 -*-
# @Time : 2019/6/11 19:22
# @Author : EricNiu
# @FileName: Main.py
# @Software: PyCharm

from MainWindow import *


def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QWidget()
    ui = UiMainWindow()
    ui.setup_ui(main_window)
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()