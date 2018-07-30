import MySQLdb
import MySQLdb.cursors
import matplotlib

matplotlib.use('Qt5Agg')
from PyQt5.QtGui import QColor
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
import sys
import os
from numpy.matlib import *
from PyQt5.QtCore import Qt
import csv
from matplotlib.font_manager import fontManager
import re
from matplotlib.text import Annotation
from numpy import arange, sin, pi
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import numpy as np


# from PyQt5 import QtWidgets
# import sys
# import MySQLdb
# from PyQt5 import QtCore, QtGui, QtWidgets
# from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
# from PyQt5.QtWidgets import QDialog, QMessageBox, QWidget, QDesktopWidget
# from PyQt5.QtWidgets import QScrollArea
# import sqlite3
# import numpy as np
# from numpy import arange, sin, pi
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.figure import Figure
# import matplotlib.pyplot as plt
# from PyQt5.QtWidgets import QApplication
# import matplotlib
# from matplotlib.externals import six
# from matplotlib.backends import qt_compat
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.figure import Figure
# import pylab as pl
# import random
# import tkinter.ttk as ttk
# import matplotlib, threading
# matplotlib.use('TkAgg')
# import scipy as sc
# import decimal as dc
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# from matplotlib.figure import Figure
# from mpl_toolkits.mplot3d import Axes3D
# import tkinter as tki


class MainWindow(QtWidgets.QMainWindow):
    parentclicked = QtCore.pyqtSignal(object)
    parent_close_call = QtCore.pyqtSignal(bool)
    has_child_paint = False
    current_child_paint = None
    current_axes = None

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi()
        self.child_Paint = None
        self.parentclicked.connect(self.send_axes)
        self.parent_close_call.connect(self.close_child_paint)
        self.current_figure = self.figure

        self.current_page_and_index = {"page": 0, "index": 0}

        self.axe_0_code_annotation = [{"code": [], "annotation": []}]
        self.axe_1_code_annotation = [{"code": [], "annotation": []}, {"code": [], "annotation": []}]

        self.axe_2_code_annotation = [{"code": [], "annotation": []},
                                      {"code": [], "annotation": []},
                                      {"code": [], "annotation": []}]

        self.axe_3_code_annotation = [{"code": [], "annotation": []},
                                      {"code": [], "annotation": []},
                                      {"code": [], "annotation": []},
                                      {"code": [], "annotation": []}]

        self.axe_4_code_annotation = [{"code": [], "annotation": []},
                                      {"code": [], "annotation": []},
                                      {"code": [], "annotation": []},
                                      {"code": [], "annotation": []},
                                      {"code": [], "annotation": []},
                                      {"code": [], "annotation": []},
                                      {"code": [], "annotation": []},
                                      {"code": [], "annotation": []},
                                      {"code": [], "annotation": []},
                                      {"code": [], "annotation": []},
                                      {"code": [], "annotation": []},
                                      {"code": [], "annotation": []}]

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(1048, 738)
        self.setMinimumHeight(738)
        # 将界面放在桌面中心
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        self.file_menu = QtWidgets.QMenu('&File', self)
        self.file_menu.addAction('导出代码', self.main_export_code, QtCore.Qt.CTRL+QtCore.Qt.Key_E)
        self.file_menu.addAction('保存', self.save_pic, QtCore.Qt.CTRL + QtCore.Qt.Key_S)

        self.file_menu.addAction('退出', self.fileQuit, QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.centralwidget = QtWidgets.QWidget()
        self.gridLayout = QtWidgets.QGridLayout()

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setSpacing(0)

        self.treeWidget = QtWidgets.QTreeWidget()
        self.treeWidget.setHeaderHidden(True)
        self.treeWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.treeWidget.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.treeWidget.setLineWidth(0)
        self.treeWidget.headerItem().setText(0, "sss")
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(18)
        self.treeWidget.headerItem().setFont(0, font)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0).setText(0, "已有模版")
        self.treeWidget.topLevelItem(0).child(0).setText(0, "模版1")
        self.treeWidget.topLevelItem(0).child(1).setText(0, "模版2")
        self.treeWidget.topLevelItem(0).child(2).setText(0, "模版3")
        self.treeWidget.topLevelItem(0).child(3).setText(0, "模版4")
        self.treeWidget.topLevelItem(1).setText(0, "自定义模版")
        self.treeWidget.itemSelectionChanged.connect(self.change_stacked_widget)
        self.treeWidget.setSortingEnabled(__sortingEnabled)

        self.horizontalLayout.addWidget(self.treeWidget)

        self.stackedWidget = QtWidgets.QStackedWidget()
        self.stackedWidget.setEnabled(True)
        self.stackedWidget.setFrameShape(QtWidgets.QFrame.Box)
        self.stackedWidget.setLineWidth(0)
        self.stackedWidget.setObjectName("stackedWidget")

        self.page = QtWidgets.QWidget()
        self.right_layout = QtWidgets.QVBoxLayout()

        self.figure = plt.figure(figsize=(10, 10), dpi=100, facecolor="#f0f0f0")

        # plt.subplots_adjust(left=0.09, bottom=0.08, right=0.94, top=0.95, wspace=0.1, hspace=0.1)
        self.figure.set_clip_on(False)
        self.figure.add_callback(self.call_back)
        self.canvas = self.figure.canvas
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.hide()
        # self.canvas.setMinimumWidth(700)
        self.current_figure = self.figure
        self.canvas.mpl_connect('button_press_event', self.show_Child_Paint)
        self.canvas.mpl_connect("resize_event", self.canvas_resize)
        self.axe = self.figure.add_subplot(111)
        self.current_figure = self.figure

        # 在右边布局中添加画布
        self.right_layout.addWidget(self.canvas)
        self.page.setLayout(self.right_layout)
        self.stackedWidget.addWidget(self.page)
        # 保存模板图片
        self.button = QPushButton("点击保存图片")
        self.right_layout.addWidget(self.button)
        self.button.clicked.connect(self.toolbar.save_figure)

        self.setCentralWidget(self.centralwidget)

        # 第二页，有两个子图
        self.page_2 = QtWidgets.QWidget()
        self.right_layout_2 = QtWidgets.QVBoxLayout()
        self.figure_2 = plt.figure(figsize=(10, 10), dpi=100, facecolor="#f0f0f0")
        self.figure_2.set_clip_on(False)
        self.figure_2.add_callback(self.call_back)

        self.canvas_2 = self.figure_2.canvas
        self.toolbar_2 = NavigationToolbar(self.canvas_2, self)
        self.toolbar_2.hide()
        cid = self.canvas_2.mpl_connect('button_press_event', self.show_Child_Paint)
        self.canvas_2.mpl_connect("resize_event", self.canvas_resize)
        self.axe_2_1 = self.figure_2.add_subplot(121)

        x = np.arange(0, 5, 0.1);
        y = np.sin(x)
        self.axe_2_1.plot(x, y)
        self.axe2_2 = self.figure_2.add_subplot(122)

        # 在右边布局中添加画布
        self.right_layout_2.addWidget(self.canvas_2)

        self.page_2.setLayout(self.right_layout_2)
        self.stackedWidget.addWidget(self.page_2)
        # 保存模板图片
        self.button = QPushButton("点击保存图片")
        self.right_layout_2.addWidget(self.button)
        self.button.clicked.connect(self.toolbar_2.save_figure)

        self.setCentralWidget(self.centralwidget)

        # 第三页，有三个子图
        self.page_3 = QtWidgets.QWidget()

        self.right_layout_3 = QtWidgets.QVBoxLayout()
        self.figure_3 = plt.figure(figsize=(10, 10), dpi=100, facecolor="#f0f0f0")
        self.figure_3.set_clip_on(False)
        self.figure_3.add_callback(self.call_back)

        self.canvas_3 = self.figure_3.canvas
        self.toolbar_3 = NavigationToolbar(self.canvas_3, self)
        self.toolbar_3.hide()
        cid = self.canvas_3.mpl_connect('button_press_event', self.show_Child_Paint)
        self.canvas_3.mpl_connect("resize_event", self.canvas_resize)
        self.axe_3_1 = self.figure_3.add_subplot(211)

        x = np.arange(0, 5, 0.1);
        y = np.sin(x)
        self.axe_3_1.plot(x, y)
        self.axe_3_2 = self.figure_3.add_subplot(223)
        self.axe_3_3 = self.figure_3.add_subplot(224)

        # 在右边布局中添加画布
        self.right_layout_3.addWidget(self.canvas_3)
        self.right_layout_3.setStretch(1, 1)
        self.right_layout_3.setStretch(3, 8)
        self.right_layout_3.setStretch(2, 1)

        self.page_3.setLayout(self.right_layout_3)
        self.stackedWidget.addWidget(self.page_3)
        # 保存模板图片
        self.button = QPushButton("点击保存图片")
        self.right_layout_3.addWidget(self.button)
        self.button.clicked.connect(self.toolbar_3.save_figure)

        self.setCentralWidget(self.centralwidget)

        # 第4页，有四个子图的页
        self.page_4 = QtWidgets.QWidget()

        self.right_layout_4 = QtWidgets.QVBoxLayout()
        self.figure_4 = plt.figure(figsize=(10, 10), dpi=100, facecolor="#f0f0f0")
        self.figure_4.set_clip_on(False)
        self.figure_4.add_callback(self.call_back)
        self.canvas_4 = self.figure_4.canvas
        self.toolbar_4 = NavigationToolbar(self.canvas_4, self)
        self.toolbar_4.hide()

        cid = self.canvas_4.mpl_connect('button_press_event', self.show_Child_Paint)
        self.canvas_4.mpl_connect("resize_event", self.canvas_resize)
        self.axe_4_1 = self.figure_4.add_subplot(221)

        x = np.arange(0, 5, 0.1);
        y = np.sin(x)
        self.axe_4_1.plot(x, y)
        self.axe_4_2 = self.figure_4.add_subplot(222)
        self.axe_4_3 = self.figure_4.add_subplot(223)
        self.axe_4_4 = self.figure_4.add_subplot(224)

        # 在右边布局中添加画布
        self.right_layout_4.addWidget(self.canvas_4)
        self.page_4.setLayout(self.right_layout_4)
        self.stackedWidget.addWidget(self.page_4)
        # 保存模板图片
        self.button = QPushButton("点击保存图片")
        self.right_layout_4.addWidget(self.button)
        self.button.clicked.connect(self.toolbar_4.save_figure)

        self.setCentralWidget(self.centralwidget)
        # 自定义页
        self.page_5 = QtWidgets.QWidget()
        # 设置第5个页面布局
        self.right_layout_5 = QtWidgets.QVBoxLayout()

        # 第一层是两个水平放置的下拉框，用来选择行数和列数
        self.top_widget = QtWidgets.QWidget()
        toplayout = QtWidgets.QHBoxLayout()
        toplayout.addStretch()

        self.row_label = QtWidgets.QLabel("行数:")
        toplayout.addWidget(self.row_label)

        self.row_comboBox = QtWidgets.QComboBox()
        self.row_comboBox.setMinimumWidth(70)
        self.row_comboBox.addItem("1")
        self.row_comboBox.addItem("2")
        self.row_comboBox.addItem("3")
        self.row_comboBox.currentIndexChanged.connect(self.set_axes_by_row_column)
        toplayout.addWidget(self.row_comboBox)

        self.column_label = QtWidgets.QLabel("列数:")
        toplayout.addWidget(self.column_label)

        self.column_comboBox = QtWidgets.QComboBox()
        self.column_comboBox.setMinimumWidth(70)
        self.column_comboBox.addItem("1")
        self.column_comboBox.addItem("2")
        self.column_comboBox.addItem("3")
        self.column_comboBox.addItem("4")
        self.column_comboBox.currentIndexChanged.connect(self.set_axes_by_row_column)
        toplayout.addWidget(self.column_comboBox)
        toplayout.addStretch()

        self.top_widget.setLayout(toplayout)
        self.right_layout_5.addWidget(self.top_widget)

        # 第二层就是canvas用来画图。

        self.figure_5 = plt.figure(figsize=(10, 10), dpi=100, facecolor="#f0f0f0")
        self.figure_5.set_clip_on(False)
        self.figure_5.add_callback(self.call_back)

        self.canvas_5 = self.figure_5.canvas
        self.toolbar_5 = NavigationToolbar(self.canvas_5, self)
        self.toolbar_5.hide()
        self.axe_5_1 = self.figure_5.add_subplot(111)
        self.canvas_5.mpl_connect('button_press_event', self.show_Child_Paint)
        self.canvas_5.mpl_connect("resize_event", self.canvas_resize)

        # 在右边布局中添加画布
        self.right_layout_5.addWidget(self.canvas_5)
        self.right_layout_5.setStretch(1, 1)
        self.right_layout_5.setStretch(2, 9)

        self.page_5.setLayout(self.right_layout_5)
        self.stackedWidget.addWidget(self.page_5)

        # 添加第二个布局
        self.horizontalLayout.addWidget(self.stackedWidget)

        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 9)

        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.centralwidget.setLayout(self.gridLayout)
        self.setCentralWidget(self.centralwidget)

        self.stackedWidget.setCurrentIndex(0)
        # 保存模板图片
        self.button = QPushButton("点击保存图片")
        self.right_layout_5.addWidget(self.button)
        self.button.clicked.connect(self.toolbar_5.save_figure)

        self.setCentralWidget(self.centralwidget)

    def main_export_code(self):
        filename = QFileDialog.getSaveFileName(self, '导出代码', os.getenv("HOME"),
                                               filter="Text files (*.txt);;Python files (*.py)")
        if filename[0] != "":
            try:
                with open(filename[0], "w", encoding='utf-8') as f:
                    current_index = self.current_page_and_index["page"]
                    f.write("# coding=utf-8\n")
                    f.write("# -*- coding: utf-8 -*- ")
                    f.write("# 导入需要的包\n")
                    f.write("import MySQLdb\n")
                    f.write("import MySQLdb.cursors\n")
                    f.write("import matplotlib\n")
                    f.write("matplotlib.use('Qt5Agg')\n")
                    f.write("from PyQt5.QtGui import QColor\n")
                    f.write("from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar\n")
                    f.write("from PyQt5.QtWidgets import *\n")
                    f.write("from PyQt5 import QtCore, QtGui\n")
                    f.write("from PyQt5 import QtWidgets\n")
                    f.write("import sys\n")
                    f.write("import os\n")
                    f.write("from numpy.matlib import *\n")
                    f.write("from PyQt5.QtCore import Qt\n")
                    f.write("import csv\n")
                    f.write("from matplotlib.font_manager import fontManager\n")
                    f.write("import re\n")
                    f.write("from matplotlib.text import Annotation\n")
                    f.write("from numpy import arange, sin, pi\n")
                    f.write("import matplotlib.pyplot as plt\n")
                    f.write("from matplotlib.pyplot import cm\n")
                    f.write("import numpy as np\n")
                    f.write("# 初始化布局\n")
                    f.write("figure = plt.figure(figsize=(10, 10), dpi=100, facecolor='#f0f0f0')\n")
                    if current_index == 0:
                        f.write("# 构造子图\n")
                        f.write("axe_0_0 = figure.add_subplot(111)\n")
                        f.write("# 开始画图\n")
                        if self.axe_0_code_annotation[0]["code"]:
                            for key, line in enumerate(self.axe_0_code_annotation[0]["code"]):
                                f.write(line+"\n")
                        if self.axe_0_code_annotation[0]["annotation"]:
                            for key, line in enumerate(self.axe_0_code_annotation[0]["annotation"]):
                                f.write(line+"\n")
                    elif current_index == 1:
                        f.write("# 构造子图\n")
                        f.write("axe_1_0 = figure.add_subplot(121)\n")
                        f.write("axe_1_1 = figure.add_subplot(122)\n")
                        f.write("# 开始画图\n")
                        for i in range(2):
                            if self.axe_1_code_annotation[i]["code"]:
                                for key, line in enumerate(self.axe_1_code_annotation[i]["code"]):
                                    f.write(line + "\n")
                            if self.axe_1_code_annotation[i]["annotation"]:
                                for key, line in enumerate(self.axe_1_code_annotation[i]["annotation"]):
                                    f.write(line + "\n")

                    elif current_index == 2:
                        f.write("# 构造子图\n")
                        f.write("axe_2_0 = figure.add_subplot(211)\n")
                        f.write("axe_2_1 = figure.add_subplot(223)\n")
                        f.write("axe_2_2 = figure.add_subplot(224)\n")
                        f.write("# 开始画图\n")
                        for i in range(3):
                            if self.axe_2_code_annotation[i]["code"]:
                                for key, line in enumerate(self.axe_2_code_annotation[i]["code"]):
                                    f.write(line + "\n")
                            if self.axe_2_code_annotation[i]["annotation"]:
                                for key, line in enumerate(self.axe_2_code_annotation[i]["annotation"]):
                                    f.write(line + "\n")
                    elif current_index == 3:
                        f.write("# 构造子图\n")
                        f.write("axe_3_0 = figure.add_subplot(221)\n")
                        f.write("axe_3_1 = figure.add_subplot(222)\n")
                        f.write("axe_3_2 = figure.add_subplot(223)\n")
                        f.write("axe_3_3 = figure.add_subplot(224)\n")
                        f.write("# 开始画图\n")
                        for i in range(4):
                            if self.axe_3_code_annotation[i]["code"]:
                                for key, line in enumerate(self.axe_3_code_annotation[i]["code"]):
                                    f.write(line + "\n")
                            if self.axe_3_code_annotation[i]["annotation"]:
                                for key, line in enumerate(self.axe_3_code_annotation[i]["annotation"]):
                                    f.write(line + "\n")
                    elif current_index == 4:
                        num_row = int(self.row_comboBox.currentText())
                        num_column = int(self.column_comboBox.currentText())
                        all = num_row * num_column

                        f.write("# 构造子图\n")
                        for i in range(all):
                            f.write("axe_4_" + str(i) + " = figure.add_subplot(" + str(num_row) + str(num_column) + str(i+1)+")\n")
                            if self.axe_4_code_annotation[i]["code"]:
                                for key, line in enumerate(self.axe_4_code_annotation[i]["code"]):
                                    f.write(line + "\n")
                            if self.axe_4_code_annotation[i]["annotation"]:
                                for key, line in enumerate(self.axe_4_code_annotation[i]["annotation"]):
                                    f.write(line + "\n")
                    f.write("plt.show()")
                    QMessageBox.information(self, "", self.tr("导出代码成功"))
            except Exception as e:
                QMessageBox.information(self, "", self.tr("导出代码失败"))

    def change_stacked_widget(self):
        templetName = str(self.treeWidget.currentItem().text(0))
        if templetName == "所有模版":
            self.current_page_and_index["page"] = 0
            self.current_figure = self.figure
            pass
        elif templetName == "模版1":
            self.stackedWidget.setCurrentIndex(0)
            self.current_page_and_index["page"] = 0
            self.current_figure = self.figure
        elif templetName == "模版2":
            self.stackedWidget.setCurrentIndex(1)
            self.current_page_and_index["page"] = 1
            self.current_figure = self.figure_2
        elif templetName == "模版3":
            self.stackedWidget.setCurrentIndex(2)
            self.current_page_and_index["page"] = 2
            self.current_figure = self.figure_3
        elif templetName == "模版4":
            self.stackedWidget.setCurrentIndex(3)
            self.current_page_and_index["page"] = 3
            self.current_figure = self.figure_4
        elif templetName == "自定义模版":
            self.stackedWidget.setCurrentIndex(4)
            self.current_page_and_index["page"] = 4
            self.current_figure = self.figure_5
            self.set_axes_by_row_column()

    def show_Child_Paint(self, event):
        if not event.inaxes:
            plt.tight_layout()
        else:
            if event.button == 1:
                if not event.inaxes.get_visible():
                    return
                if not MainWindow.has_child_paint:
                    self.child_Paint = Child_Paint()
                    MainWindow.current_child_paint = self.child_Paint
                    self.child_Paint.showNormal()
                    self.child_Paint.change_parent_has_child_paint.connect(self.change_has_child_paint)
                    self.child_Paint.update_parent_export_code_annotation.connect(self.all_code_annotation)
                    self.current_axes = event.inaxes
                    self.current_page_and_index["index"] = self.current_figure.axes.index(event.inaxes)

                    self.parentclicked.emit(event.inaxes)
                    self.child_Paint.show()
                    MainWindow.has_child_paint = True
                else:
                    MainWindow.current_child_paint.activateWindow()
                    MainWindow.current_child_paint.showNormal()
                    self.current_page_and_index["index"] = self.current_figure.axes.index(event.inaxes)

                    self.parentclicked.emit(event.inaxes)

            elif event.button == 3:
                if event.inaxes.get_visible():
                    event.inaxes.set_visible(False)
                    event.inaxes.figure.canvas.draw()
                else:
                    event.inaxes.set_visible(True)
                    event.inaxes.figure.canvas.draw()
            else:
                pass

    def change_axe_prefix(self, code_or_annotation):
        new_prefix = "axe_"+str(self.current_page_and_index['page'])+"_"+str(self.current_page_and_index['index'])
        new_result = []
        for key, line in enumerate(code_or_annotation):
            newline = line.replace("axe", new_prefix)
            new_result.append(newline)
        return new_result


    def all_code_annotation(self, listof_code_or_annotation):
        page = self.current_page_and_index["page"]
        index = self.current_page_and_index["index"]
        if "code" in listof_code_or_annotation:
            new_code = self.change_axe_prefix(listof_code_or_annotation["code"])
            if page == 0:
                self.axe_0_code_annotation[index]["code"] = new_code
            elif page == 1:
                self.axe_1_code_annotation[index]["code"] = new_code
            elif page == 2:
                self.axe_2_code_annotation[index]["code"] = new_code
            elif page == 3:
                self.axe_3_code_annotation[index]["code"] = new_code
            elif page == 4:
                self.axe_4_code_annotation[index]["code"] = new_code

        if "annotation" in listof_code_or_annotation:
            new_annotation = self.change_axe_prefix(listof_code_or_annotation["annotation"])
            if page == 0:
                self.axe_0_code_annotation[index]["annotation"] = new_annotation
            elif page == 1:
                self.axe_1_code_annotation[index]["annotation"] = new_annotation
            elif page == 2:
                self.axe_2_code_annotation[index]["annotation"] = new_annotation
            elif page == 3:
                self.axe_3_code_annotation[index]["annotation"] = new_annotation
            elif page == 4:
                self.axe_4_code_annotation[index]["annotation"] = new_annotation

    def send_axes(self, axe):
        self.child_Paint.child_axes = axe
        self.child_Paint.init_parent()

    def call_back(self):
        plt.tight_layout()

    # 没有event参数，程序会报错，不能运行
    def canvas_resize(self, event):
        pass

    def fileQuit(self):
        self.close()

    def closeEvent(self, event):
        self.parent_close_call.emit(True)

    def change_has_child_paint(self):
        MainWindow.has_child_paint = False
        MainWindow.current_child_paint = None

    def close_child_paint(self):
        if MainWindow.current_child_paint == None:
            pass
        else:
            MainWindow.current_child_paint.close()

    def set_axes_by_row_column(self):
        num_row = int(self.row_comboBox.currentText())
        num_column = int(self.column_comboBox.currentText())
        self.figure_5.clf()
        for axes_item in range(num_row * num_column):
            single_axes = self.figure_5.add_subplot(num_row, num_column, axes_item + 1)
        self.figure_5.canvas.draw()

    def save_pic(self):
        templetName = str(self.treeWidget.currentItem().text(0))
        if templetName == "所有模版":
            self.toolbar.save_figure()
        elif templetName == "模版1":
            self.toolbar.save_figure()
        elif templetName == "模版2":
            self.toolbar_2.save_figure()
        elif templetName == "模版3":
            self.toolbar_3.save_figure()
        elif templetName == "模版4":
            self.toolbar_4.save_figure()
        elif templetName == "自定义模版":
            self.toolbar_5.save_figure()


class Child_Paint(QMainWindow):
    childclicked = QtCore.pyqtSignal(str)
    change_parent_has_child_paint = QtCore.pyqtSignal(bool)
    tight_parent_layout = QtCore.pyqtSignal(bool)
    update_parent_export_code_annotation = QtCore.pyqtSignal(object)
    paint_code = []
    lock = None

    def __init__(self, parent=None):
        super(Child_Paint, self).__init__(parent)
        # 用来接收父界面的axes参数
        self.child_axes = None
        self.parent_current_canvas = None
        self.AllData = []
        self.value = re.compile(r'^[-+]?[0-9]+\.[0-9]+$')
        self.value1 = re.compile(r'^[-+]?[0-9]+[\.]?[0-9]?$')
        self.current_annotation = None
        self.background = None
        self.all_annotation = []
        self.all_annotation_contentlist = []
        self.parent_all_annotation = []
        self.current_annotation_index = None
        self.current_press_position = None

        self.main_widget = QtWidgets.QWidget(self)
        self.allView = QtWidgets.QHBoxLayout(self.main_widget)

        self.leftView = QtWidgets.QVBoxLayout()
        self.rightView = QtWidgets.QVBoxLayout()

        self.allView.addLayout(self.leftView)
        self.allView.addLayout(self.rightView)
        self.allView.setStretch(0, 1)
        self.allView.setStretch(1, 9)

        # 设置左面布局
        self.leftView.setContentsMargins(10, 0, 10, 0)
        self.leftView.setSpacing(8)

        # 下拉框选择画图类型
        self.comboBox = QtWidgets.QComboBox()
        self.comboBox.addItem("折线图")
        self.comboBox.addItem("柱状图")
        self.comboBox.addItem("饼图")
        self.comboBox.addItem("散点图")
        self.comboBox.addItem("等高线")
        self.comboBox.addItem("sin函数")
        self.comboBox.addItem("cos函数")
        self.comboBox.addItem("tan函数")
        self.comboBox.addItem("log函数")
        self.comboBox.addItem("其他")

        self.comboBox.currentIndexChanged.connect(self.set_button_text)
        self.leftView.addWidget(self.comboBox)

        self.import_data_button = QtWidgets.QPushButton()
        self.import_data_button.setObjectName("pushButton")
        self.import_data_button.setText("导入数据文件")
        self.import_data_button.clicked.connect(self.import_data)
        self.leftView.addWidget(self.import_data_button)

        # 题名那一行
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.title = QtWidgets.QLabel()
        self.title.setObjectName("label")
        self.title.setText("题名    ")
        self.horizontalLayout.addWidget(self.title)

        self.title_text = QtWidgets.QLineEdit()
        self.title_text.setPlaceholderText("")
        self.horizontalLayout.addWidget(self.title_text)
        self.title_text.textChanged.connect(self.set_title)
        self.leftView.addLayout(self.horizontalLayout)

        # x轴坐标那一行
        self.x_line_layout = QtWidgets.QHBoxLayout()
        self.x_label = QtWidgets.QLabel()
        self.x_label.setObjectName("x轴坐标")
        self.x_label.setText("x轴坐标 ")
        self.x_line_layout.addWidget(self.x_label)

        self.x_label_text = QtWidgets.QLineEdit()
        self.x_line_layout.addWidget(self.x_label_text)
        self.x_label_text.textChanged.connect(self.set_x_label)
        self.leftView.addLayout(self.x_line_layout)

        self.x_scale_layout = QHBoxLayout()
        self.x_scale_label = QLabel()
        self.x_scale_label.setText("x轴范围 ")
        self.x_scale_layout.addWidget(self.x_scale_label)

        self.x_left_scale_text = QLineEdit()
        self.x_right_scale_text = QLineEdit()
        self.x_left_scale_text.textChanged.connect(self.scale_x_y)
        self.x_right_scale_text.textChanged.connect(self.scale_x_y)
        self.x_scale_layout.addWidget(self.x_left_scale_text)
        self.x_scale_layout.addWidget(self.x_right_scale_text)

        self.leftView.addLayout(self.x_scale_layout)

        # y轴坐标那一行
        self.y_line_layout = QtWidgets.QHBoxLayout()
        self.y_label = QtWidgets.QLabel()
        self.y_label.setObjectName("label_6")
        self.y_label.setText("y轴坐标 ")
        self.y_line_layout.addWidget(self.y_label)

        self.y_label_text = QtWidgets.QLineEdit()
        self.y_line_layout.addWidget(self.y_label_text)
        self.y_label_text.textChanged.connect(self.set_y_label)
        self.leftView.addLayout(self.y_line_layout)

        self.y_scale_layout = QHBoxLayout()
        self.y_scale_label = QLabel()
        self.y_scale_label.setText("y轴范围 ")
        self.y_scale_layout.addWidget(self.y_scale_label)

        self.y_left_scale_text = QLineEdit()
        self.y_right_scale_text = QLineEdit()
        self.y_left_scale_text.textChanged.connect(self.scale_x_y)
        self.y_right_scale_text.textChanged.connect(self.scale_x_y)
        self.y_scale_layout.addWidget(self.y_left_scale_text)
        self.y_scale_layout.addWidget(self.y_right_scale_text)

        self.leftView.addLayout(self.y_scale_layout)

        # 字体那一行
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.label_2 = QtWidgets.QLabel()
        self.label_2.setObjectName("label_2")
        self.label_2.setText("字体    ")
        self.horizontalLayout_4.addWidget(self.label_2)

        self.fontComboBox = QtWidgets.QComboBox()
        self.fontComboBox.addItems([font.name for font in fontManager.ttflist if
                                    os.path.exists(font.fname) and os.stat(font.fname).st_size > 1e6])
        self.fontComboBox.currentIndexChanged.connect(self.set_font)
        self.horizontalLayout_4.addWidget(self.fontComboBox)
        self.leftView.addLayout(self.horizontalLayout_4)

        # 颜色选择
        self.horizontalLayout_color = QtWidgets.QHBoxLayout()
        self.label_color = QtWidgets.QLabel()
        self.label_color.setObjectName("label_color")
        self.label_color.setText("颜色    ")
        self.horizontalLayout_color.addWidget(self.label_color)

        self.color = QColor(0, 0, 0)
        self.color_picker = QPushButton(self)
        self.color_picker.setStyleSheet("QWidget { background-color: %s }" % self.color.name())
        self.color_picker.clicked.connect(self.show_color)
        self.horizontalLayout_color.addWidget(self.color_picker)
        self.leftView.addLayout(self.horizontalLayout_color)

        # 图例那一行
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.label_4 = QtWidgets.QLabel()
        self.label_4.setText("图例    ")
        self.horizontalLayout_6.addWidget(self.label_4)

        self.legend_code = QtWidgets.QLineEdit()
        self.legend_code.setPlaceholderText("$图例1$,$图例2$,..")
        self.horizontalLayout_6.addWidget(self.legend_code)
        self.leftView.addLayout(self.horizontalLayout_6)

        # 清除按钮
        self.clearButton = QtWidgets.QPushButton()
        self.clearButton.setText("清除")
        self.clearButton.clicked.connect(self.clear_all)
        self.leftView.addWidget(self.clearButton)

        # 高级按钮
        self.advancedButton = QtWidgets.QPushButton()
        self.advancedButton.setText("高级")
        self.leftView.addWidget(self.advancedButton)
        self.advancedButton.clicked.connect(self.show_advanced_window)

        # 画图按钮
        self.paint = QtWidgets.QPushButton()
        self.paint.setText("折线图")
        self.paint.clicked.connect(self.paint_graph)
        self.leftView.addWidget(self.paint)

        self.figure = plt.figure(figsize=(10, 10), dpi=100)
        self.figure.set_clip_on(False)
        self.figure.add_callback(self.call_back)

        self.canvas = self.figure.canvas
        self.canvas.mpl_connect('resize_event', self.canvas_resize)

        # sinx
        self.sinx = QtWidgets.QPushButton()
        self.sinx.setText("sinx")
        self.sinx.clicked.connect(self.sin_x)
        self.leftView.addWidget(self.sinx)

        self.figure = plt.figure(figsize=(10, 10), dpi=100)
        self.figure.set_clip_on(False)
        self.figure.add_callback(self.call_back)

        self.canvas = self.figure.canvas
        self.canvas.mpl_connect('resize_event', self.canvas_resize)

        # cosx
        self.cosx = QtWidgets.QPushButton()
        self.cosx.setText("cosx")
        self.cosx.clicked.connect(self.cos_x)
        self.leftView.addWidget(self.cosx)

        self.figure = plt.figure(figsize=(10, 10), dpi=100)
        self.figure.set_clip_on(False)
        self.figure.add_callback(self.call_back)

        self.canvas = self.figure.canvas
        self.canvas.mpl_connect('resize_event', self.canvas_resize)

        # tanx
        self.tanx = QtWidgets.QPushButton()
        self.tanx.setText("tanx")
        self.tanx.clicked.connect(self.tan_x)
        self.leftView.addWidget(self.tanx)

        self.figure = plt.figure(figsize=(10, 10), dpi=100)
        self.figure.set_clip_on(False)
        self.figure.add_callback(self.call_back)

        self.canvas = self.figure.canvas
        self.canvas.mpl_connect('resize_event', self.canvas_resize)

        # exponential function
        self.exponential = QtWidgets.QPushButton()
        self.exponential.setText("指数函数")
        self.exponential.clicked.connect(self.exponential_function)
        self.leftView.addWidget(self.exponential)

        self.figure = plt.figure(figsize=(10, 10), dpi=100)
        self.figure.set_clip_on(False)
        self.figure.add_callback(self.call_back)

        self.canvas = self.figure.canvas
        self.canvas.mpl_connect('resize_event', self.canvas_resize)

        # logarithmic Function
        self.logarithmic = QtWidgets.QPushButton()
        self.logarithmic.setText("对数函数")
        self.logarithmic.clicked.connect(self.logarithmic_function)
        self.leftView.addWidget(self.logarithmic)

        self.figure = plt.figure(figsize=(10, 10), dpi=100)
        self.figure.set_clip_on(False)
        self.figure.add_callback(self.call_back)

        self.canvas = self.figure.canvas
        self.canvas.mpl_connect('resize_event', self.canvas_resize)

        # Nike Function
        self.nike = QtWidgets.QPushButton()
        self.nike.setText("对勾函数")
        self.nike.clicked.connect(self.nike_function)
        self.leftView.addWidget(self.nike)

        self.figure = plt.figure(figsize=(10, 10), dpi=100)
        self.figure.set_clip_on(False)
        self.figure.add_callback(self.call_back)

        self.canvas = self.figure.canvas
        self.canvas.mpl_connect('resize_event', self.canvas_resize)

        # parabola
        self.parabola = QtWidgets.QPushButton()
        self.parabola.setText("抛物线")
        self.parabola.clicked.connect(self.parabola_x)
        self.leftView.addWidget(self.parabola)
        self.leftView.addStretch()

        self.figure = plt.figure(figsize=(10, 10), dpi=100)
        self.figure.set_clip_on(False)
        self.figure.add_callback(self.call_back)

        self.canvas = self.figure.canvas
        self.canvas.mpl_connect('resize_event', self.canvas_resize)

        # 新拷贝过来的
        self.canvas.mpl_connect("button_press_event", self.add_annotation)
        self.canvas.mpl_connect("pick_event", self.pick_annotation)
        self.canvas.mpl_connect("key_press_event", self.delete_annotation)
        self.canvas.mpl_connect("motion_notify_event", self.move_annotation)
        self.canvas.mpl_connect("button_release_event", self.release_button)

        self.axe = self.figure.add_subplot(111)

        # 在右边布局中添加画布
        self.rightView.addWidget(self.canvas)

        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.hide()

        self.button = QPushButton("点击保存图片")
        self.rightView.addWidget(self.button)
        self.button.clicked.connect(self.toolbar.save_figure)

        self.setCentralWidget(self.main_widget)

        self.code_and_data = QtWidgets.QWidget()
        self.code_and_data_layout = QtWidgets.QHBoxLayout()
        self.code_and_data.setLayout(self.code_and_data_layout)
        self.rightView.addWidget(self.code_and_data)

        # 数据库连接信息
        self.databaseDock = QDockWidget(self.tr("数据库信息"))
        self.databaseDock.setMaximumWidth(200)
        self.databaseDock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.databaseWidget = QtWidgets.QWidget()
        self.databaseLayout = QVBoxLayout()
        self.databaseWidget.setLayout(self.databaseLayout)

        self.databaseAddress = QLineEdit("127.0.0.1")
        self.databaseAddress.setPlaceholderText("地址如:127.0.0.1")
        self.databaseLayout.addWidget(self.databaseAddress)

        self.databasePort = QLineEdit("3306")
        self.databasePort.setPlaceholderText("端口")
        self.databaseLayout.addWidget(self.databasePort)

        self.databaseUser = QLineEdit("root")
        self.databaseUser.setPlaceholderText("用户名")
        self.databaseLayout.addWidget(self.databaseUser)

        self.databasePasswd = QLineEdit("123456")
        self.databasePasswd.setPlaceholderText("密码")
        self.databaseLayout.addWidget(self.databasePasswd)

        self.databaseName = QLineEdit("data")
        self.databaseName.setPlaceholderText("数据库名")
        self.databaseLayout.addWidget(self.databaseName)

        self.databaseCharset = QLineEdit("utf8")
        self.databaseCharset.setPlaceholderText("字符集")
        self.databaseLayout.addWidget(self.databaseCharset)

        self.databaseTable = QLineEdit("AllData")
        self.databaseTable.setPlaceholderText("表名")
        self.databaseLayout.addWidget(self.databaseTable)

        self.databaseConnect = QPushButton()
        self.databaseConnect.setText("连接")
        self.databaseConnect.clicked.connect(self.databese_connect)
        self.databaseLayout.addWidget(self.databaseConnect)

        self.databaseDock.setWidget(self.databaseWidget)
        self.code_and_data_layout.addWidget(self.databaseDock)
        self.databaseDock.hide()

        # 代码停靠窗口
        self.codeDock = QDockWidget(self.tr("输入代码"))
        self.codeDock.setAllowedAreas(Qt.RightDockWidgetArea)
        self.codeDock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.codeDock.setMinimumHeight(300)
        self.codeDock.setMinimumWidth(100)

        # 右边代码布局(垂直方向)，由文本框和一个按钮组成
        self.codeWidget = QtWidgets.QWidget()
        self.codeLayout = QtWidgets.QVBoxLayout()
        self.codeWidget.setLayout(self.codeLayout)

        self.codeText = QPlainTextEdit()
        self.codeText.setPlaceholderText("只可使用axes对象，例:self.axe.set_xlabel('x坐标')")
        self.codeLayout.addWidget(self.codeText)

        self.run_export = QWidget()
        self.run_export_layout = QHBoxLayout()

        self.runcode = QPushButton("运行")
        self.runcode.clicked.connect(self.run_code)
        self.run_export_layout.addWidget(self.runcode)

        self.exportCode = QPushButton("导出代码")
        self.exportCode.clicked.connect(self.export_code)
        self.run_export_layout.addWidget(self.exportCode)

        self.run_export.setLayout(self.run_export_layout)
        self.codeLayout.addWidget(self.run_export)

        self.codeDock.setWidget(self.codeWidget)
        # self.code_and_data_layout.addWidget(self.codeDock)
        self.code_and_data_layout.addWidget(self.codeDock)

        self.codeDock.hide()

        # 用户数据停靠窗口
        self.dataDock = QDockWidget(self.tr("全部数据已存在self.AllData中,可通过下标访问。"))
        self.dataDock.setAllowedAreas(Qt.RightDockWidgetArea)
        self.dataDock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.dataTable = QtWidgets.QTableWidget(0, 0)

        self.dataDock.setWidget(self.dataTable)
        self.dataDock.setMinimumHeight(300)
        self.dataDock.setMinimumWidth(100)
        self.code_and_data_layout.addWidget(self.dataDock)
        # self.code_and_data.addDockWidget(Qt.BottomDockWidgetArea, self.dataDock)
        self.dataDock.hide()

        self.setWindowTitle("Paint")
        self.setMinimumSize(1300, 768)
        # self.showMaximized()
        # self.setWindowState(QtCore.Qt.WindowMaximized)
        # self.screen = QtGui.QDesktopWidget().screenGeometry()
        # self.setGeometry(0, 0, self.screen.width(), self.screen.height())
        # self.setWindowFlags(QtCore.Qt.Dialog)
        # self.showFullScreen()

    def show_advanced_window(self):
        if self.codeDock.isHidden() | self.dataDock.isHidden() | self.databaseDock.isHidden():
            self.codeDock.show()
            self.dataDock.show()
            self.databaseDock.show()
        else:
            self.codeDock.hide()
            self.dataDock.hide()
            self.databaseDock.hide()

    def databese_connect(self):
        self.AllData = []
        self.dataTable.disconnect()
        self.dataTable.setRowCount(0)
        self.dataTable.setColumnCount(0)
        if (self.databaseAddress.text() != "") & \
                (self.databasePort.text() != "") & \
                (self.databaseUser.text() != "") & \
                (self.databasePasswd.text() != "") & \
                (self.databaseName.text() != "") & \
                (self.databaseCharset.text() != "") & \
                (self.databaseTable.text() != ""):

            try:
                conn = MySQLdb.connect(host=self.databaseAddress.text(),
                                       port=int(self.databasePort.text()),
                                       user=self.databaseUser.text(),
                                       passwd=self.databasePasswd.text(),
                                       db=self.databaseName.text(),
                                       charset=self.databaseCharset.text(),
                                       cursorclass=MySQLdb.cursors.SSCursor)
                cursor = conn.cursor()
                print("连接成功")
                query = "select * from " + self.databaseTable.text()
                cursor.execute(query)
                m = 0
                for row_data in cursor:
                    max_column = 0
                    if len(row_data) > max_column:
                        for i in range(len(row_data)):
                            self.dataTable.setHorizontalHeaderItem(i + max_column, QTableWidgetItem(
                                str("AllData[" + str(i + max_column) + "]")))
                        max_column = len(row_data)
                        self.dataTable.setColumnCount(max_column)
                    row = self.dataTable.rowCount()
                    self.dataTable.insertRow(row)
                    for column, stuff in enumerate(row_data):
                        item = QTableWidgetItem(str(stuff))
                        self.dataTable.setItem(row, column, item)
                    self.dataTable.setVerticalHeaderItem(m, QTableWidgetItem(str(m)))
                    m += 1

                num_of_row = self.dataTable.rowCount()
                num_of_column = self.dataTable.columnCount()

                for each_column in range(num_of_column):
                    item_list = []
                    for each_row in range(num_of_row):
                        item = self.dataTable.item(each_row, each_column).text()
                        item_list.append(self.to_number(item))
                    self.AllData.append(item_list)
                self.dataTable.itemChanged.connect(self.updata_data)

                conn.close()
            except Exception as e:
                print(e)
                QMessageBox.information(self, "发生错误", self.tr("请检查连接信息是否正确"))
        else:
            QMessageBox.information(self, "", self.tr("连接信息不完整，请补充"))

    def show_color(self):
        self.col = QColorDialog.getColor()
        if self.col.isValid():
            self.color_picker.setStyleSheet("QWidget { background-color: %s }" % self.col.name())
            self.color = QColor(self.col.name())

    def text_to_number(self, text):
        if text.isdigit():
            return True
        elif self.value1.match(text):
            return True
        else:
            return False

    def scale_x_y(self):
        pre_x_left_lim, pre_x_right_lim = self.axe.get_xlim()
        pre_y_bottom_lim, pre_y_top_lim = self.axe.get_ylim()

        self.x1 = str(self.x_left_scale_text.text())
        if self.text_to_number(self.x1):
            self.axe.set_xlim(left=self.to_number(self.x1))
            self.child_axes.set_xlim(left=self.to_number(self.x1))

        self.x2 = self.x_right_scale_text.text()
        if self.text_to_number(self.x2):
            self.axe.set_xlim(right=self.to_number(self.x2))
            self.child_axes.set_xlim(right=self.to_number(self.x2))

        self.y1 = self.y_left_scale_text.text()
        if self.text_to_number(self.y1):
            self.axe.set_ylim(bottom=self.to_number(self.y1))
            self.child_axes.set_ylim(bottom=self.to_number(self.y1))

        self.y2 = self.y_right_scale_text.text()
        if self.text_to_number(self.y2):
            self.axe.set_ylim(top=self.to_number(self.y2))
            self.child_axes.set_ylim(top=self.to_number(self.y2))

        plt.tight_layout()
        self.canvas.draw()
        self.child_axes.figure.canvas.draw()

    def set_text(self, new_text):
        self.title.setText(new_text)
        plt.tight_layout()

    def sendToParent(self):
        str = self.inf.text()
        self.childclicked.emit(str)

    def set_title(self):
        csfont = {'fontname': 'FangSong'}
        self.axe.set_title(self.title_text.text(), **csfont)
        plt.tight_layout()
        self.canvas.draw()

        # 设置parent axes
        self.child_axes.set_title(self.title_text.text(), **csfont)
        self.child_axes.figure.canvas.draw()

    def set_x_label(self):
        csfont = {'fontname': 'FangSong'}
        self.axe.set_xlabel(self.x_label_text.text(), **csfont)
        plt.tight_layout()
        self.canvas.draw()

        self.child_axes.set_xlabel(self.x_label_text.text(), **csfont)
        plt.tight_layout()
        self.child_axes.figure.canvas.draw()

    def set_y_label(self):
        csfont = {'fontname': 'FangSong'}
        self.axe.set_ylabel(self.y_label_text.text(), **csfont)
        plt.tight_layout()
        self.canvas.draw()

        self.child_axes.set_ylabel(self.y_label_text.text(), **csfont)
        plt.tight_layout()
        self.child_axes.figure.canvas.draw()

    def clear_all(self):
        self.axe.cla()
        self.axe.set_frame_on(True)
        self.axe.set_autoscale_on(True)
        self.axe.set_xlim(0, 1)
        self.axe.set_ylim(0, 1)
        self.canvas.draw()

        self.child_axes.cla()
        self.child_axes.set_frame_on(True)
        self.child_axes.set_autoscale_on(True)
        self.child_axes.set_xlim(0, 1)
        self.child_axes.set_ylim(0, 1)
        self.child_axes.figure.canvas.draw()

        self.title_text.clear()
        self.x_label_text.clear()
        self.y_label_text.clear()
        self.dataTable.clear()
        self.dataTable.setRowCount(0)
        self.dataTable.setColumnCount(0)
        self.all_annotation = []
        self.parent_all_annotation = []

    def set_font(self):
        font = self.fontComboBox.currentText()
        csfont = {'fontname': font}
        plt.title(self.title_text.text(), **csfont)
        self.child_axes.set_title(self.title_text.text(), **csfont)

        plt.xlabel(self.x_label_text.text(), **csfont)
        self.child_axes.set_xlabel(self.x_label_text.text(), **csfont)

        plt.ylabel(self.y_label_text.text(), **csfont)
        self.child_axes.set_ylabel(self.y_label_text.text(), **csfont)
        self.canvas.draw()
        self.child_axes.figure.canvas.draw()

    def init_parent(self):
        self.all_annotation = []
        self.parent_all_annotation = []
        self.axe.cla()
        self.axe.set_frame_on(True)
        self.axe.set_xlabel(self.child_axes.get_xlabel())
        self.x_label_text.setText(self.child_axes.get_xlabel())

        self.axe.set_ylabel(self.child_axes.get_ylabel())
        self.y_label_text.setText(self.child_axes.get_ylabel())

        self.axe.set_title(self.child_axes.get_title())
        self.title_text.setText(self.child_axes.get_title())
        self.canvas.draw()

    def import_data(self):
        self.AllData = []
        self.dataTable.disconnect()
        if self.dataDock.isHidden():
            self.dataDock.show()
        self.dataTable.setRowCount(0)
        self.dataTable.setColumnCount(0)
        path = QFileDialog.getOpenFileName(self, "打开CSV文件", os.getenv('HOME'), 'csv(*.csv)')
        if path[0] != '':
            with open(path[0], newline='') as csv_file:
                # self.dataTable.setRowCount(0)
                # self.dataTable.setColumnCount(2)
                my_file = csv.reader(csv_file, delimiter=',', quotechar="|")
                m = 0
                for row_data in my_file:
                    max_column = 0
                    if len(row_data) > max_column:
                        for i in range(len(row_data) - max_column):
                            self.dataTable.setHorizontalHeaderItem(i + max_column, QTableWidgetItem(
                                str("AllData[" + str(i + max_column) + "]")))
                        max_column = len(row_data)
                        self.dataTable.setColumnCount(max_column)
                    row = self.dataTable.rowCount()
                    self.dataTable.insertRow(row)
                    for column, stuff in enumerate(row_data):
                        item = QTableWidgetItem(stuff)
                        self.dataTable.setItem(row, column, item)
                    self.dataTable.setVerticalHeaderItem(m, QTableWidgetItem(str(m)))
                    m += 1
                csv_file.close()
        num_of_row = self.dataTable.rowCount()
        num_of_column = self.dataTable.columnCount()

        for each_column in range(num_of_column):
            item_list = []
            for each_row in range(num_of_row):
                item = self.dataTable.item(each_row, each_column).text()
                item_list.append(self.to_number(item))
            self.AllData.append(item_list)
        self.dataTable.itemChanged.connect(self.updata_data)

    def to_number(self, num):
        if num.isdigit():
            return int(num)
        elif self.value1.match(num):
            return float(num)
        else:
            return num

    def set_button_text(self):
        graph_type = self.comboBox.currentText()
        self.paint.setText(graph_type)
        if graph_type == "其他":
            self.sinx.show()
            self.cosx.show()
            self.tanx.show()
            self.nike.show()
            self.logarithmic.show()
            self.exponential.show()
            self.parabola.show()
            self.paint.hide()

        else:
            self.sinx.hide()
            self.cosx.hide()
            self.tanx.hide()
            self.exponential.hide()
            self.nike.hide()
            self.logarithmic.hide()
            self.parabola.hide()
            self.paint.show()

    def export_code(self):
        filename = QFileDialog.getSaveFileName(self, '导出代码', os.getenv("HOME"),
                                               filter="Text files (*.txt);;Python files (*.py)")
        if filename[0] != "":
            try:
                with open(filename[0], "w") as f:
                    # 输出需要导入的包
                    f.write(
                        "import matplotlib.pyplot as plt\nfrom matplotlib.pyplot import cm\nimport numpy as np" + "\n")
                    f.write("fig = plt.figure(figsize=(10,10), dpi=100)" + "\n")
                    f.write("axe = fig.add_subplot(111)" + "\n")

                    # 设置字体
                    f.write("font = {'fontname': '" + self.fontComboBox.currentText() + "'}" + "\n")
                    # 设置数据
                    f.write("axe.set_xlabel('" + self.x_label_text.text() + "', **font)" + "\n")
                    f.write("axe.set_ylabel('" + self.y_label_text.text() + "', **font)" + "\n")
                    f.write("axe.set_title('" + self.title_text.text() + "', **font)" + "\n")
                    f.write("AllData=[]" + "\n")
                    for i in range(len(self.AllData)):
                        f.write("data" + str(i) + " = " + str(self.AllData[i]) + "\n")
                        f.write("AllData.append(data" + str(i) + ")" + "\n")
                    f.write("legend = '" + self.legend_code.text() + "'" + "\n")

                    # 设置颜色
                    f.write("color = iter(cm.rainbow(np.linspace(0, 1, len(AllData))))" + "\n")
                    f.write("c = next(color)" + "\n")
                    # 开始画图
                    paint_type = self.paint.text()
                    if paint_type == "折线图":
                        f.write("legend_length = len(legend.split(','))" + "\n")
                        f.write("for index in range(len(ALlData)):" + "\n")
                        f.write("    c = next(color)" + "\n")
                        f.write("    try:" + "\n")
                        f.write("       if legend.rstrip() == '':" + "\n")
                        f.write("           axe.plot(AllData[2 * index], AllData[2 * index + 1], '*-', color=c)" + "\n")
                        f.write("       else:" + "\n")
                        f.write("           if legend_length > index:" + "\n")
                        f.write(
                            "               axe.plot(AllData[2 * index], AllData[2 * index + 1], '*-', label=legend.split(',')[index], color=c)" + "\n")
                        f.write("               axe.legend()" + "\n")
                        f.write("           else:" + "\n")
                        f.write(
                            "               axe.plot(AllData[2 * index], AllData[2 * index + 1], '*-', color=c)" + "\n")
                        f.write("    except:" + "\n")
                        f.write("        continue" + "\n")
                        for item in self.all_annotation:
                            f.write(
                                "axe.annotate('" + item.get_text() + "', " + "xy=" + str(item.xy) + ", xytext=(" + str(
                                    item.xytext) + ",arrowprops=dict(facecolor='black', shrink=0.05),picker=2" + "\n")

                    elif paint_type == "散点图":
                        f.write("try:" + "\n")
                        f.write("   if legend.rstrip() == '':" + "\n")
                        f.write("       axe.scatter(AllData[0], AllData[1], color=c)" + "\n")
                        f.write("   else:" + "\n")
                        f.write("       s = axe.scatter(AllData[0], AllData[1], color=c)" + "\n")
                        f.write(
                            "       axe.legend((s,), (legend,), scatterpoints=1, loc='lower left',ncol=2, fontsize=8)" + "\n")
                        f.write("except:" + "\n")
                        f.write("    pass" + "\n")
                        for item in self.all_annotation:
                            f.write(
                                "axe.annotate('" + item.get_text() + "', " + "xy=" + str(item.xy) + ", xytext=(" + str(
                                    item.xytext) + ",arrowprops=dict(facecolor='black', shrink=0.05),picker=2" + "\n")


                    elif paint_type == "柱状图":
                        f.write("size = 1 / len(AllData)" + "\n")
                        f.write("legend_length = len(legend.split(','))" + "\n")
                        f.write("for index in range(len(AllData)):" + "\n")
                        f.write("    c = next(color)" + "\n")
                        f.write("    try:" + "\n")
                        f.write("        if legend.rstrip() == '':" + "\n")
                        f.write(
                            "            axe.bar(np.arange(len(AllData[index])) + index * size, AllData[index], size, color=c)" + "\n")
                        f.write("        else:" + "\n")
                        f.write("            if legend_length > index:" + "\n")
                        f.write(
                            "                axe.bar(np.arange(len(AllData[index])) + index * size, AllData[index], size, color=c, label=legend.split(',')[index])" + "\n")
                        f.write("                axe.legend()" + "\n")
                        f.write("            else:" + "\n")
                        f.write(
                            "                axe.bar(np.arange(len(AllData[index])) + index * size, AllData[index], size, color=c)" + "\n")
                        f.write("    except:" + "\n")
                        f.write("        continue" + "\n")
                        f.write("axe.set_xticks(np.arange(len(AllData[0])) + 0.35)" + "\n")
                        for item in self.all_annotation:
                            f.write(
                                "axe.annotate('" + item.get_text() + "', " + "xy=" + str(item.xy) + ", xytext=(" + str(
                                    item.xytext) + ",arrowprops=dict(facecolor='black', shrink=0.05),picker=2" + "\n")


                    elif paint_type == "饼图":
                        f.write("axe.pie(AllData[0], labels=AllData[1])" + "\n")
                        f.write("axe.legend()" + "\n")
                        for item in self.all_annotation:
                            f.write(
                                "axe.annotate('" + item.get_text() + "', " + "xy=" + str(item.xy) + ", xytext=(" + str(
                                    item.xytext) + ",arrowprops=dict(facecolor='black', shrink=0.05),picker=2" + "\n")

                    f.write("plt.tight_layout()" + "\n")
                    f.write("plt.show()" + "\n" + "\n")
                QMessageBox.information(self, "", self.tr("导出代码成功"))
            except Exception as e:
                print(e)
                QMessageBox.information(self, "", self.tr("导出代码失败"))
        else:
            pass

    # 取左侧列表中的属性值
    def get_property_code(self):
        self.paint_code.append(str("axe_font = {'fontname': '" + self.fontComboBox.currentText() + "'}"))
        self.paint_code.append(str("axe.set_title('"+self.title_text.text()+"', **axe_font)"))
        self.paint_code.append(str("axe.set_xlabel('"+self.x_label_text.text()+"', **axe_font)"))
        self.paint_code.append(str("axe.set_ylabel('"+self.y_label_text.text()+"', **axe_font)"))

        x11 = str(self.x_left_scale_text.text())
        if self.text_to_number(x11):
            self.paint_code.append(str("axe.set_xlim(left=" + str(self.to_number(x11)) + ")"))

        x22 = self.x_right_scale_text.text()
        if self.text_to_number(x22):
            self.paint_code.append(str("axe.set_xlim(right=" + str(self.to_number(x22)) + ")"))

        y11 = self.y_left_scale_text.text()
        if self.text_to_number(y11):
            self.paint_code.append(str("axe.set_ylim(bottom=" + str(self.to_number(y11)) + ")"))

        y22 = self.y_right_scale_text.text()
        if self.text_to_number(y22):
            self.paint_code.append(str("axe.set_ylim(top=" + str(self.to_number(y22)) + ")"))

        # 添加数据
        self.paint_code.append(str("axe_AllData = []"))
        for i in range(len(self.AllData)):
            self.paint_code.append(str("axe_data" + str(i) + " = " + str(self.AllData[i])))
            self.paint_code.append(str("axe_AllData.append(axe_data" + str(i) + ")"))
        # 添加图例
        self.paint_code.append(str("axe_legend = '" + self.legend_code.text() + "'"))

    def paint_graph(self):
        self.paint_code = []
        self.get_property_code()
        paint_type = self.paint.text()
        self.axe.cla()
        self.child_axes.cla()
        rows = self.dataTable.rowCount()
        if rows > 0:
            font = self.fontComboBox.currentText()
            csfont = {'fontname': font}
            if paint_type == "折线图":
                self.axe.cla()
                self.axe.set_frame_on(True)
                self.axe.set_autoscale_on(True)
                color = iter(cm.rainbow(np.linspace(0, 1, len(self.AllData))))
                legend_length = len(self.legend_code.text().split(","))
                for index in range(len(self.AllData)):
                    c = next(color)
                    try:
                        if self.legend_code.text().rstrip() == "":
                            self.axe.plot(self.AllData[2 * index], self.AllData[2 * index + 1], '*-', color=c)
                            self.child_axes.plot(self.AllData[2 * index], self.AllData[2 * index + 1], '*-', color=c)
                        else:
                            if legend_length > index:
                                self.axe.plot(self.AllData[2 * index], self.AllData[2 * index + 1], '*-',
                                              label=self.legend_code.text().split(",")[index], color=c)
                                self.axe.legend()
                                self.child_axes.plot(self.AllData[2 * index], self.AllData[2 * index + 1], '*-',
                                                     label=self.legend_code.text().split(",")[index], color=c)
                                self.child_axes.legend()
                            else:
                                self.axe.plot(self.AllData[2 * index], self.AllData[2 * index + 1], '*-', color=c)
                                self.child_axes.plot(self.AllData[2 * index], self.AllData[2 * index + 1], '*-',
                                                     color=c)
                    except:
                        continue
                self.child_axes.set_frame_on(True)
                plt.tight_layout()
                self.paint_code.append(str("axe.set_frame_on(True)"))
                self.paint_code.append(str("axe.set_autoscale_on(True)"))
                self.paint_code.append(str("axe_color = iter(cm.rainbow(np.linspace(0, 1, len(axe_AllData))))"))
                self.paint_code.append(str("axe_legend_length = len(axe_legend.split(','))"))
                self.paint_code.append(str("for axe_index in range(len(axe_AllData)):"))
                self.paint_code.append(str("    axe_c = next(axe_color)"))
                self.paint_code.append(str("    try:"))
                self.paint_code.append(str("        if axe_legend.rstrip() == '':"))
                self.paint_code.append(str("            axe.plot(axe_AllData[2 * axe_index], axe_AllData[2 * axe_index + 1], '*-', color=axe_c)"))
                self.paint_code.append(str("        else:"))
                self.paint_code.append(str("            if axe_legend_length > axe_index:"))
                self.paint_code.append(str("                axe.plot(axe_AllData[2 * axe_index], axe_AllData[2 * axe_index + 1], '*-',"))
                self.paint_code.append(str("                    label=axe_legend.split(',')[axe_index], color=axe_c)"))
                self.paint_code.append(str("                axe.legend()"))
                self.paint_code.append(str("            else:"))
                self.paint_code.append(str("                axe.plot(axe_AllData[2 * axe_index], axe_AllData[2 * axe_index + 1], '*-', color=axe_c)"))
                self.paint_code.append(str("    except:"))
                self.paint_code.append(str("        continue"))
                self.paint_code.append(str("plt.tight_layout()"))

            elif paint_type == "散点图":
                self.axe.cla()
                self.axe.set_frame_on(True)
                self.child_axes.set_frame_on(True)
                color = iter(cm.rainbow(np.linspace(0, 1, len(self.AllData))))
                c = next(color)
                try:
                    if self.legend_code.text().rstrip() == "":
                        self.axe.scatter(self.AllData[0], self.AllData[1], color=c)
                        # self.axe.scatter(self.AllData[2], self.AllData[3], color=c)
                        self.child_axes.scatter(self.AllData[0], self.AllData[1], color=c)
                    else:
                        s = self.axe.scatter(self.AllData[0], self.AllData[1], color=c)
                        self.axe.legend((s,), (self.legend_code.text(),), scatterpoints=1, loc='lower left', ncol=2,
                                        fontsize=8)
                        ps = self.child_axes.scatter(self.AllData[0], self.AllData[1], color=c)
                        self.child_axes.legend((ps,), (self.legend_code.text(),), scatterpoints=1, loc='lower left',
                                               ncol=2,
                                               fontsize=8)
                except:
                    pass
                self.paint_code.append(str("axe.set_frame_on(True)"))
                self.paint_code.append(str("axe.set_autoscale_on(True)"))
                self.paint_code.append(str("axe_color = iter(cm.rainbow(np.linspace(0, 1, len(axe_AllData))))"))
                self.paint_code.append(str("axe_c = next(axe_color)"))
                self.paint_code.append(str("try:"))
                self.paint_code.append(str("    if axe_legend.rstrip() == '':"))
                self.paint_code.append(str("        axe.scatter(axe_AllData[0], axe_AllData[1], color=axe_c)"))
                self.paint_code.append(str("    else:"))
                self.paint_code.append(str("        axe_s = axe.scatter(axe_AllData[0], axe_AllData[1], color=axe_c)"))
                self.paint_code.append(str("        axe.legend((axe_s,), (axe_legend,), scatterpoints=1, loc='lower left', ncol=2,fontsize=8)"))
                self.paint_code.append(str("except:"))
                self.paint_code.append(str("    pass"))
                self.paint_code.append(str("plt.tight_layout()"))

            elif paint_type == "柱状图":
                self.axe.cla()
                self.axe.set_frame_on(True)
                self.child_axes.set_frame_on(True)
                self.axe.set_autoscale_on(True)
                color = iter(cm.rainbow(np.linspace(0, 1, len(self.AllData))))
                # self.axe.bar(np.arange(len(self.AllData[1])), self.AllData[0], 0.35)
                # self.axe.bar(np.arange(len(self.AllData[1]))+0.35, self.AllData[1], 0.35)
                legend_length = len(self.legend_code.text().split(","))
                size = 1 / len(self.AllData)
                for index in range(len(self.AllData)):
                    c = next(color)
                    try:
                        if self.legend_code.text().rstrip() == "":
                            self.axe.bar(np.arange(len(self.AllData[index])) + index * size, self.AllData[index], size,
                                         color=c)
                            self.child_axes.bar(np.arange(len(self.AllData[index])) + index * size, self.AllData[index],
                                                size, color=c)
                        else:
                            if legend_length > index:
                                self.axe.bar(np.arange(len(self.AllData[index])) + index * size, self.AllData[index],
                                             size, color=c, label=self.legend_code.text().split(",")[index])
                                self.axe.legend()
                                self.child_axes.bar(np.arange(len(self.AllData[index])) + index * size,
                                                    self.AllData[index], size, color=c,
                                                    label=self.legend_code.text().split(",")[index])

                                self.child_axes.legend()
                            else:
                                self.axe.bar(np.arange(len(self.AllData[index])) + index * size, self.AllData[index],
                                             size, color=c)
                                self.child_axes.bar(np.arange(len(self.AllData[index])) + index * size,
                                                    self.AllData[index], size, color=c)
                    except:
                        continue
                self.axe.set_xticks(np.arange(len(self.AllData[0])) + 0.35)
                plt.tight_layout()
                self.child_axes.set_xticks(np.arange(len(self.AllData[0])) + 0.35)

                self.paint_code.append(str("axe.set_frame_on(True)"))
                self.paint_code.append(str("axe.set_autoscale_on(True)"))
                self.paint_code.append(str("axe_color = iter(cm.rainbow(np.linspace(0, 1, len(axe_AllData))))"))
                self.paint_code.append(str("axe_legend_length = len(axe_legend.split(','))"))
                self.paint_code.append(str("axe_size = 1 / len(axe_AllData)"))
                self.paint_code.append(str("for axe_index in range(len(axe_AllData)):"))
                self.paint_code.append(str("    axe_c = next(axe_color)"))
                self.paint_code.append(str("    try:"))
                self.paint_code.append(str("        if axe_legend.rstrip() == '':"))
                self.paint_code.append(str("            axe.bar(np.arange(len(axe_AllData[axe_index])) + axe_index * axe_size, axe_AllData[axe_index], axe_size,color=axe_c)"))
                self.paint_code.append(str("        else:"))
                self.paint_code.append(str("            if axe_legend_length > axe_index:"))
                self.paint_code.append(str("                axe.bar(np.arange(len(axe_AllData[axe_index])) + axe_index * axe_size, axe_AllData[axe_index],\
                                 axe_size, color=axe_c, label=axe_legend.split(',')[axe_index])"))
                self.paint_code.append(str("                axe.legend()"))
                self.paint_code.append(str("            else:"))
                self.paint_code.append(str("                axe.bar(np.arange(len(axe_AllData[axe_index])) + axe_index * axe_size, axe_AllData[axe_index], axe_size, color=axe_c)"))
                self.paint_code.append(str("    except:"))
                self.paint_code.append(str("        continue"))
                self.paint_code.append(str("axe.set_xticks(np.arange(len(axe_AllData[0])) + 0.35)"))
                self.paint_code.append(str("plt.tight_layout()"))
            elif paint_type == "饼图":
                self.axe.cla()
                self.axe.set_title(self.title_text.text(), **csfont)
                self.axe.figure.canvas.draw()
                self.axe.pie(self.AllData[0], labels=self.AllData[1])
                self.child_axes.pie(self.AllData[0], labels=self.AllData[1])
                self.child_axes.set_title(self.title_text.text())
                self.axe.legend()
                self.child_axes.legend()
                plt.tight_layout()
                self.paint_code.append(str("axe.pie(axe_AllData[0], labels=axe_AllData[1])"))
                self.paint_code.append(str("axe.legend()"))
                self.paint_code.append(str("plt.tight_layout()"))

            elif paint_type == "等高线":
                self.axe.cla()
                self.axe.set_title(self.title_text.text(), **csfont)
                self.axe.figure.canvas.draw()
                x = self.AllData[0]
                y = self.AllData[1]
                [X, Y] = meshgrid(x, y)
                z = X ** 2 + Y ** 2
                self.axe.contour(x, y, z)
                self.child_axes.contour(x, y, z)
                self.child_axes.set_title(self.title_text.text())
                self.axe.legend()
                self.child_axes.legend()
                plt.tight_layout()
                self.paint_code.append(str("[axe_X, axe_Y] = meshgrid(axe_AllData[0], axe_AllData[1])"))
                self.paint_code.append(str("axe_z = axe_X ** 2 + axe_Y ** 2"))
                self.paint_code.append(str("axe.contour(axe_X, axe_Y, axe_z)"))
                self.paint_code.append(str("plt.tight_layout()"))
                self.paint_code.append(str(""))
            elif paint_type == "sin函数":
                self.axe.cla()
                self.axe.set_title(self.title_text.text(), **csfont)
                self.axe.figure.canvas.draw()
                x = self.AllData[0]
                self.axe.plot(x, sin(x), color=self.color.name())
                self.child_axes.plot(x, sin(x), color=self.color.name())
                self.child_axes.set_title(self.title_text.text())
                self.axe.legend()
                self.child_axes.legend()
                plt.tight_layout()

                self.paint_code.append(str("axe.plot(axe_AllData[0], sin(axe_AllData[0]), color='"+str(self.color.name() + "')")))
                self.paint_code.append(str("\nplt.tight_layout()\n"))
            elif paint_type == "cos函数":
                self.axe.cla()
                self.axe.set_title(self.title_text.text(), **csfont)
                self.axe.figure.canvas.draw()
                x = self.AllData[0]
                self.axe.plot(x, cos(x), color=self.color.name())
                self.child_axes.plot(x, cos(x), color=self.color.name())
                self.child_axes.set_title(self.title_text.text())
                self.axe.legend()
                self.child_axes.legend()
                plt.tight_layout()

                self.paint_code.append(str("axe.plot(axe_AllData[0], cos(axe_AllData[0]), color='"+str(self.color.name() + "')")))
                self.paint_code.append(str("plt.tight_layout()"))
            elif paint_type == "tan函数":
                self.axe.cla()
                self.axe.set_title(self.title_text.text(), **csfont)
                self.axe.figure.canvas.draw()
                x = self.AllData[0]
                self.axe.plot(x, tan(x), color=self.color.name())
                self.child_axes.plot(x, tan(x), color=self.color.name())
                self.child_axes.set_title(self.title_text.text())
                self.axe.legend()
                self.child_axes.legend()
                plt.tight_layout()
                self.paint_code.append(str("axe.plot(axe_AllData[0], tan(axe_AllData[0]), color='"+str(self.color.name() + "')")))
                self.paint_code.append(str("plt.tight_layout()"))
            elif paint_type == "log函数":
                self.axe.cla()
                self.axe.set_title(self.title_text.text(), **csfont)
                self.axe.figure.canvas.draw()
                x = self.AllData[0]
                self.axe.plot(x, log(x), color=self.color.name())
                self.child_axes.plot(x, log(x), color=self.color.name())
                self.child_axes.set_title(self.title_text.text())
                self.axe.legend()
                self.child_axes.legend()
                plt.tight_layout()
                self.paint_code.append(str("axe.plot(axe_AllData[0], log(axe_AllData[0]), color='"+str(self.color.name() + "')")))
                self.paint_code.append(str("\nplt.tight_layout()\n"))

            plt.tight_layout()
            self.canvas.draw()
            self.child_axes.figure.canvas.draw()
            self.submit_parent_code("code")
        else:
            QMessageBox.information(self, "", self.tr("请导入数据，或使用高级功能"))

    def run_code(self):
        if self.codeText.toPlainText() != "":
            try:
                self.axe.cla()
                self.child_axes.cla()
                for each_line_code in self.codeText.toPlainText().split("\n"):
                    exec(each_line_code.strip())
                    exec(each_line_code.strip().replace("self.axe", "self.child_axes", 1))
                self.canvas.draw()
                self.child_axes.figure.canvas.draw()
            except:
                QMessageBox.critical(self, "出现错误", self.tr("请检查代码"))
        else:
            QMessageBox.information(self, "", self.tr("请输入运行代码"))

    def closeEvent(self, *args, **kwargs):
        self.change_parent_has_child_paint.emit(False)

    def call_back(self):
        plt.tight_layout()

    def canvas_resize(self, event):
        plt.tight_layout()

    def updata_data(self, current_item):
        self.AllData[current_item.column()][current_item.row()] = self.to_number(current_item.text())



    # 新函数
    def pick_annotation(self, event):
        if type(event.artist) == Annotation:
            self.current_annotation = event.artist
            self.current_annotation_index = self.all_annotation.index(self.current_annotation)
            self.current_press_position = event.mouseevent.xdata, event.mouseevent.ydata
        else:
            self.current_annotation = None

    def get_annotation_content_list(self):
        self.all_annotation_contentlist = []
        for key, anno in enumerate(self.parent_all_annotation):
            an = "axe.annotate('"+anno.get_text()+"', xy="+str(anno.xy)+", xytext="+str(anno.get_position())+\
                ",arrowprops=dict(facecolor='black', shrink=0.05),picker=2)"
            self.all_annotation_contentlist.append(an)
        return self.all_annotation_contentlist

    def submit_parent_code(self, code_type):
        if code_type == "code":
            self.update_parent_export_code_annotation.emit({"code": self.paint_code})
        else:
            self.update_parent_export_code_annotation.emit({"annotation": self.get_annotation_content_list()})

    def add_annotation(self, event):
        if event.inaxes is None:
            return
        if event.button == 3:
            self.current_press_position = event.xdata, event.ydata
            text, ok = QtWidgets.QInputDialog.getText(self, "输入注释", "注释点:(" + str(round(event.xdata, 3)) + "," + str(
                round(event.ydata, 3)) + ")", QLineEdit.Normal)
            if ok:
                if text.rstrip() == "":
                    QMessageBox.critical(self, "", self.tr("注释内容不能为空"))
                    return
                annotation = self.axe.annotate(text, xy=(event.xdata, event.ydata),
                                               arrowprops=dict(facecolor='black', shrink=0.05),
                                               picker=2)
                self.all_annotation.append(annotation)

                self.canvas.draw()
                parent_annotation = self.child_axes.annotate(text, xy=(event.xdata, event.ydata),
                                                             arrowprops=dict(facecolor='black', shrink=0.05),
                                                             picker=2)
                self.parent_all_annotation.append(parent_annotation)
                self.submit_parent_code("annotation")
                self.child_axes.figure.canvas.draw()
            else:
                return
        elif event.button == 1 and not self.current_annotation is None:
            if Child_Paint.lock is not None:
                return
            contains, attrd = self.current_annotation.contains(event)
            if not contains:
                return
            if self.current_press_position is None:
                return
            Child_Paint.lock = self
            self.current_annotation.set_animated(True)
            self.canvas.draw()
            self.background = self.canvas.copy_from_bbox(self.axe.bbox)
            self.axe.draw_artist(self.current_annotation)
            self.canvas.blit(self.axe.bbox)

    def move_annotation(self, event):
        if Child_Paint.lock is not self:
            return
        if event.inaxes is None:
            return
        if event.inaxes is not None and self.current_annotation is not None:
            self.current_annotation.set_position((event.xdata, event.ydata))
            self.current_annotation.xytext = (event.xdata, event.ydata)
            self.canvas.restore_region(self.background)
            self.axe.draw_artist(self.current_annotation)
            self.canvas.blit(self.axe.bbox)

    def release_button(self, event):
        if Child_Paint.lock is not self:
            return
        if event.button == 1 and not self.current_annotation is None:

            if self.current_press_position == (event.xdata, event.ydata):
                Child_Paint.lock = None
                self.current_annotation.set_animated(False)
                self.background = None
                self.current_press_position = None
                self.canvas.draw()
                return
            Child_Paint.lock = None
            self.current_annotation.set_animated(False)
            self.background = None
            self.canvas.draw()
            self.parent_all_annotation[self.current_annotation_index].set_position((event.xdata, event.ydata))
            self.parent_all_annotation[self.current_annotation_index].xytext = (event.xdata, event.ydata)
            self.submit_parent_code("annotation")
            self.child_axes.draw_artist(self.parent_all_annotation[self.current_annotation_index])
            self.child_axes.figure.canvas.draw()

    def delete_annotation(self, event):
        if event.key == "backspace" and not self.current_annotation is None:
            self.all_annotation.pop(self.current_annotation_index)

            self.current_annotation.remove()
            self.canvas.draw()
            self.current_annotation = None
            self.parent_all_annotation[self.current_annotation_index].remove()
            self.child_axes.figure.canvas.draw()
            self.parent_all_annotation.pop(self.current_annotation_index)
            self.submit_parent_code("annotation")
        self.current_press_position = None

    def sin_x(self, event):
        self.axe.cla()
        X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
        S = np.sin(X)
        self.axe.plot(X, S, color=self.color.name())

        plt.tight_layout()
        self.canvas.draw()

        self.child_axes.cla()
        self.child_axes.plot(X, S, color=self.color.name())
        self.child_axes.set_frame_on(True)
        plt.tight_layout()
        self.child_axes.figure.canvas.draw()

    def cos_x(self, event):
        self.axe.cla()
        X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
        S = np.cos(X)
        self.axe.plot(X, S, color=self.color.name())
        plt.tight_layout()
        self.canvas.draw()
        self.child_axes.cla()
        self.child_axes.plot(X, S, color=self.color.name())
        self.child_axes.set_frame_on(True)
        plt.tight_layout()
        self.child_axes.figure.canvas.draw()

    def tan_x(self, event):
        self.axe.cla()
        X = np.linspace(0, np.pi, 256, endpoint=True)
        S = np.tan(X)
        self.axe.plot(X, S)
        plt.tight_layout()
        self.canvas.draw()
        self.child_axes.cla()
        self.child_axes.plot(X, S, color=self.color.name())
        self.child_axes.set_frame_on(True)
        plt.tight_layout()
        self.child_axes.figure.canvas.draw()

    def exponential_function(self, event):
        self.axe.cla()
        X = np.linspace(-4, 4, 100, endpoint=True)
        self.axe.plot(X, pow(e, X), color=self.color.name())
        plt.tight_layout()
        self.canvas.draw()
        self.child_axes.cla()
        self.child_axes.plot(X, pow(e, X), color=self.color.name())
        self.child_axes.set_frame_on(True)
        plt.tight_layout()
        self.child_axes.figure.canvas.draw()

    def logarithmic_function(self, event):
        self.axe.cla()
        X = np.linspace(-4, 4, 100, endpoint=True)
        self.axe.plot(X, log(X), color=self.color.name())
        plt.tight_layout()
        self.canvas.draw()
        self.child_axes.cla()
        self.child_axes.plot(X, log(X), color=self.color.name())
        self.child_axes.set_frame_on(True)
        plt.tight_layout()
        self.child_axes.figure.canvas.draw()

    def nike_function(self, event):
        self.axe.cla()
        X = np.linspace(-4, 4, 100, endpoint=True)
        self.axe.plot(X, X + 1 / X, color=self.color.name())
        plt.tight_layout()
        self.canvas.draw()
        self.child_axes.cla()
        self.child_axes.plot(X, X + 1 / X, color=self.color.name())
        self.child_axes.set_frame_on(True)
        plt.tight_layout()
        self.child_axes.figure.canvas.draw()

    def parabola_x(self, event):
        self.axe.cla()
        X1 = np.linspace(-4, 4, 100, endpoint=True)
        self.axe.plot(X1, (X1 ** 2) / 9, color=self.color.name())
        plt.tight_layout()
        self.canvas.draw()
        self.child_axes.cla()
        self.child_axes.plot(X1, (X1 ** 2) / 9, color=self.color.name())
        self.child_axes.set_frame_on(True)
        plt.tight_layout()
        self.child_axes.figure.canvas.draw()


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     main = Child_Paint()
#     main.show()
#     main.run
#     sys.exit(app.exec_())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.setWindowTitle("基于python的图表自动生成系统")
    MainWindow.show()
    sys.exit(app.exec_())
