# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainForm.ui'
#
# Created: Wed Jun  2 20:03:23 2010
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,960,600).size()).expandedTo(MainWindow.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setGeometry(QtCore.QRect(0,39,960,537))
        self.centralwidget.setObjectName("centralwidget")

        self.vboxlayout = QtGui.QVBoxLayout(self.centralwidget)
        self.vboxlayout.setObjectName("vboxlayout")

        self.splitter_2 = QtGui.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName("splitter_2")

        self.widget = QtGui.QWidget(self.splitter_2)
        self.widget.setObjectName("widget")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.widget)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.label_3 = QtGui.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.vboxlayout1.addWidget(self.label_3)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")

        self.pushButton = QtGui.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.hboxlayout.addWidget(self.pushButton)

        self.lineEdit = QtGui.QLineEdit(self.widget)
        self.lineEdit.setObjectName("lineEdit")
        self.hboxlayout.addWidget(self.lineEdit)
        self.vboxlayout1.addLayout(self.hboxlayout)

        self.splitter = QtGui.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")

        self.widget1 = QtGui.QWidget(self.splitter)
        self.widget1.setObjectName("widget1")

        self.vboxlayout2 = QtGui.QVBoxLayout(self.widget1)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.label = QtGui.QLabel(self.widget1)
        self.label.setObjectName("label")
        self.vboxlayout2.addWidget(self.label)

        self.treeView = QtGui.QTreeView(self.widget1)
        self.treeView.setObjectName("treeView")
        self.vboxlayout2.addWidget(self.treeView)

        self.widget2 = QtGui.QWidget(self.splitter)
        self.widget2.setObjectName("widget2")

        self.vboxlayout3 = QtGui.QVBoxLayout(self.widget2)
        self.vboxlayout3.setObjectName("vboxlayout3")

        self.label_2 = QtGui.QLabel(self.widget2)
        self.label_2.setObjectName("label_2")
        self.vboxlayout3.addWidget(self.label_2)

        self.tableView = QtGui.QTableView(self.widget2)
        self.tableView.setObjectName("tableView")
        self.vboxlayout3.addWidget(self.tableView)
        self.vboxlayout.addWidget(self.splitter_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,960,27))
        self.menubar.setObjectName("menubar")

        self.menu = QtGui.QMenu(self.menubar)
        self.menu.setObjectName("menu")

        self.menu_3 = QtGui.QMenu(self.menu)
        self.menu_3.setObjectName("menu_3")

        self.menu_4 = QtGui.QMenu(self.menu)
        self.menu_4.setObjectName("menu_4")

        self.menu_2 = QtGui.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")

        self.menu_5 = QtGui.QMenu(self.menu_2)
        self.menu_5.setObjectName("menu_5")

        self.menu_7 = QtGui.QMenu(self.menu_2)
        self.menu_7.setObjectName("menu_7")

        self.menu_6 = QtGui.QMenu(self.menubar)
        self.menu_6.setObjectName("menu_6")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setGeometry(QtCore.QRect(0,576,960,24))
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setGeometry(QtCore.QRect(0,27,10,12))
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea,self.toolBar)

        self.toolBar_2 = QtGui.QToolBar(MainWindow)
        self.toolBar_2.setGeometry(QtCore.QRect(10,27,950,12))
        self.toolBar_2.setObjectName("toolBar_2")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea,self.toolBar_2)

        self.action_5 = QtGui.QAction(MainWindow)
        self.action_5.setObjectName("action_5")

        self.action_7 = QtGui.QAction(MainWindow)
        self.action_7.setObjectName("action_7")

        self.action_8 = QtGui.QAction(MainWindow)
        self.action_8.setObjectName("action_8")

        self.action_9 = QtGui.QAction(MainWindow)
        self.action_9.setObjectName("action_9")

        self.action_10 = QtGui.QAction(MainWindow)
        self.action_10.setObjectName("action_10")

        self.action_11 = QtGui.QAction(MainWindow)
        self.action_11.setObjectName("action_11")

        self.action_12 = QtGui.QAction(MainWindow)
        self.action_12.setObjectName("action_12")

        self.actionURL = QtGui.QAction(MainWindow)
        self.actionURL.setObjectName("actionURL")

        self.action_13 = QtGui.QAction(MainWindow)
        self.action_13.setObjectName("action_13")

        self.action_14 = QtGui.QAction(MainWindow)
        self.action_14.setObjectName("action_14")

        self.action_16 = QtGui.QAction(MainWindow)
        self.action_16.setObjectName("action_16")

        self.action_17 = QtGui.QAction(MainWindow)
        self.action_17.setObjectName("action_17")

        self.action_18 = QtGui.QAction(MainWindow)
        self.action_18.setObjectName("action_18")

        self.action_19 = QtGui.QAction(MainWindow)
        self.action_19.setObjectName("action_19")

        self.action_21 = QtGui.QAction(MainWindow)
        self.action_21.setObjectName("action_21")

        self.action_22 = QtGui.QAction(MainWindow)
        self.action_22.setObjectName("action_22")
        self.menu_3.addAction(self.action_7)
        self.menu_3.addAction(self.action_9)
        self.menu_3.addAction(self.action_8)
        self.menu_4.addAction(self.action_10)
        self.menu_4.addAction(self.action_11)
        self.menu.addAction(self.menu_3.menuAction())
        self.menu.addAction(self.menu_4.menuAction())
        self.menu.addSeparator()
        self.menu.addAction(self.action_5)
        self.menu_5.addAction(self.action_12)
        self.menu_5.addAction(self.actionURL)
        self.menu_7.addAction(self.action_21)
        self.menu_7.addAction(self.action_22)
        self.menu_2.addAction(self.menu_5.menuAction())
        self.menu_2.addAction(self.menu_7.menuAction())
        self.menu_2.addAction(self.action_13)
        self.menu_2.addAction(self.action_14)
        self.menu_2.addSeparator()
        self.menu_2.addAction(self.action_16)
        self.menu_6.addAction(self.action_17)
        self.menu_6.addAction(self.action_18)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_6.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Быстрый поиск", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "Найти", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Метаданные", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Объекты хранилища", None, QtGui.QApplication.UnicodeUTF8))
        self.menu.setTitle(QtGui.QApplication.translate("MainWindow", "&Файл", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_3.setTitle(QtGui.QApplication.translate("MainWindow", "&Хранилище", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_4.setTitle(QtGui.QApplication.translate("MainWindow", "&Пользователь", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_2.setTitle(QtGui.QApplication.translate("MainWindow", "&Объекты", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_5.setTitle(QtGui.QApplication.translate("MainWindow", "&Добавить", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_7.setTitle(QtGui.QApplication.translate("MainWindow", "&Пометить", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_6.setTitle(QtGui.QApplication.translate("MainWindow", "Метаданные", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar_2.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar_2", None, QtGui.QApplication.UnicodeUTF8))
        self.action_5.setText(QtGui.QApplication.translate("MainWindow", "Выход", None, QtGui.QApplication.UnicodeUTF8))
        self.action_7.setText(QtGui.QApplication.translate("MainWindow", "Создать", None, QtGui.QApplication.UnicodeUTF8))
        self.action_8.setText(QtGui.QApplication.translate("MainWindow", "Удалить текущее", None, QtGui.QApplication.UnicodeUTF8))
        self.action_9.setText(QtGui.QApplication.translate("MainWindow", "Открыть", None, QtGui.QApplication.UnicodeUTF8))
        self.action_10.setText(QtGui.QApplication.translate("MainWindow", "Сменить", None, QtGui.QApplication.UnicodeUTF8))
        self.action_11.setText(QtGui.QApplication.translate("MainWindow", "Изменить", None, QtGui.QApplication.UnicodeUTF8))
        self.action_12.setText(QtGui.QApplication.translate("MainWindow", "Файл", None, QtGui.QApplication.UnicodeUTF8))
        self.actionURL.setText(QtGui.QApplication.translate("MainWindow", "URL", None, QtGui.QApplication.UnicodeUTF8))
        self.action_13.setText(QtGui.QApplication.translate("MainWindow", "Изменить", None, QtGui.QApplication.UnicodeUTF8))
        self.action_14.setText(QtGui.QApplication.translate("MainWindow", "Удалить", None, QtGui.QApplication.UnicodeUTF8))
        self.action_16.setText(QtGui.QApplication.translate("MainWindow", "Найти", None, QtGui.QApplication.UnicodeUTF8))
        self.action_17.setText(QtGui.QApplication.translate("MainWindow", "Удалить", None, QtGui.QApplication.UnicodeUTF8))
        self.action_18.setText(QtGui.QApplication.translate("MainWindow", "Изменить", None, QtGui.QApplication.UnicodeUTF8))
        self.action_19.setText(QtGui.QApplication.translate("MainWindow", "Пометить объект", None, QtGui.QApplication.UnicodeUTF8))
        self.action_21.setText(QtGui.QApplication.translate("MainWindow", "Тегом", None, QtGui.QApplication.UnicodeUTF8))
        self.action_22.setText(QtGui.QApplication.translate("MainWindow", "Полем", None, QtGui.QApplication.UnicodeUTF8))

