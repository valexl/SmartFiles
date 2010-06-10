# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow_ui.ui'
#
# Created: Thu Jun 10 21:32:37 2010
#      by: PyQt4 UI code generator 4.6.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(765, 729)
        MainWindow.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_search = QtGui.QPushButton(self.frame)
        self.pushButton_search.setObjectName("pushButton_search")
        self.horizontalLayout.addWidget(self.pushButton_search)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.radioButton_request_language = QtGui.QRadioButton(self.frame)
        self.radioButton_request_language.setObjectName("radioButton_request_language")
        self.verticalLayout_3.addWidget(self.radioButton_request_language)
        self.radioButton_neural_net = QtGui.QRadioButton(self.frame)
        self.radioButton_neural_net.setObjectName("radioButton_neural_net")
        self.verticalLayout_3.addWidget(self.radioButton_neural_net)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.lineEdit_search = QtGui.QLineEdit(self.frame)
        self.lineEdit_search.setObjectName("lineEdit_search")
        self.horizontalLayout.addWidget(self.lineEdit_search)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.tableView_entity = QtGui.QTableView(self.frame)
        self.tableView_entity.setObjectName("tableView_entity")
        self.verticalLayout_4.addWidget(self.tableView_entity)
        self.verticalLayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 765, 23))
        self.menubar.setObjectName("menubar")
        self.menu_file = QtGui.QMenu(self.menubar)
        self.menu_file.setObjectName("menu_file")
        self.menu_repo = QtGui.QMenu(self.menu_file)
        self.menu_repo.setObjectName("menu_repo")
        self.menu_users = QtGui.QMenu(self.menu_file)
        self.menu_users.setObjectName("menu_users")
        self.menu_objects = QtGui.QMenu(self.menubar)
        self.menu_objects.setObjectName("menu_objects")
        self.menu_add_entity = QtGui.QMenu(self.menu_objects)
        self.menu_add_entity.setObjectName("menu_add_entity")
        self.menu_mark = QtGui.QMenu(self.menu_objects)
        self.menu_mark.setObjectName("menu_mark")
        self.menu_views = QtGui.QMenu(self.menubar)
        self.menu_views.setObjectName("menu_views")
        self.menu_setting = QtGui.QMenu(self.menubar)
        self.menu_setting.setObjectName("menu_setting")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setIconSize(QtCore.QSize(32, 32))
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.dockWidget_tag = QtGui.QDockWidget(MainWindow)
        self.dockWidget_tag.setObjectName("dockWidget_tag")
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_users = QtGui.QLabel(self.dockWidgetContents)
        self.label_users.setObjectName("label_users")
        self.verticalLayout_5.addWidget(self.label_users)
        self.comboBox_repo_users_metadata = QtGui.QComboBox(self.dockWidgetContents)
        self.comboBox_repo_users_metadata.setObjectName("comboBox_repo_users_metadata")
        self.verticalLayout_5.addWidget(self.comboBox_repo_users_metadata)
        self.treeView_metadata = QtGui.QTableView(self.dockWidgetContents)
        self.treeView_metadata.setObjectName("treeView_metadata")
        self.verticalLayout_5.addWidget(self.treeView_metadata)
        self.dockWidget_tag.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget_tag)
        self.action_exit = QtGui.QAction(MainWindow)
        self.action_exit.setObjectName("action_exit")
        self.action_create_repo = QtGui.QAction(MainWindow)
        self.action_create_repo.setObjectName("action_create_repo")
        self.action_open_repo = QtGui.QAction(MainWindow)
        self.action_open_repo.setObjectName("action_open_repo")
        self.action_delete_repo = QtGui.QAction(MainWindow)
        self.action_delete_repo.setObjectName("action_delete_repo")
        self.action_delete_user_from_repo = QtGui.QAction(MainWindow)
        self.action_delete_user_from_repo.setObjectName("action_delete_user_from_repo")
        self.action_switch_user = QtGui.QAction(MainWindow)
        self.action_switch_user.setObjectName("action_switch_user")
        self.action_add_file = QtGui.QAction(MainWindow)
        self.action_add_file.setObjectName("action_add_file")
        self.action_add_URL = QtGui.QAction(MainWindow)
        self.action_add_URL.setObjectName("action_add_URL")
        self.action_mark_tag = QtGui.QAction(MainWindow)
        self.action_mark_tag.setObjectName("action_mark_tag")
        self.action_mark_field = QtGui.QAction(MainWindow)
        self.action_mark_field.setObjectName("action_mark_field")
        self.action_change_entity = QtGui.QAction(MainWindow)
        self.action_change_entity.setObjectName("action_change_entity")
        self.action_delete_entity = QtGui.QAction(MainWindow)
        self.action_delete_entity.setObjectName("action_delete_entity")
        self.action_view_metadata = QtGui.QAction(MainWindow)
        self.action_view_metadata.setCheckable(True)
        self.action_view_metadata.setChecked(True)
        self.action_view_metadata.setObjectName("action_view_metadata")
        self.action_setting_tags = QtGui.QAction(MainWindow)
        self.action_setting_tags.setObjectName("action_setting_tags")
        self.action_setting_fields = QtGui.QAction(MainWindow)
        self.action_setting_fields.setObjectName("action_setting_fields")
        self.menu_repo.addAction(self.action_create_repo)
        self.menu_repo.addAction(self.action_open_repo)
        self.menu_repo.addAction(self.action_delete_repo)
        self.menu_repo.addSeparator()
        self.menu_users.addAction(self.action_switch_user)
        self.menu_users.addAction(self.action_delete_user_from_repo)
        self.menu_file.addAction(self.menu_repo.menuAction())
        self.menu_file.addAction(self.menu_users.menuAction())
        self.menu_file.addAction(self.action_exit)
        self.menu_add_entity.addAction(self.action_add_file)
        self.menu_add_entity.addAction(self.action_add_URL)
        self.menu_mark.addAction(self.action_mark_tag)
        self.menu_mark.addAction(self.action_mark_field)
        self.menu_objects.addAction(self.menu_add_entity.menuAction())
        self.menu_objects.addAction(self.menu_mark.menuAction())
        self.menu_objects.addSeparator()
        self.menu_objects.addAction(self.action_change_entity)
        self.menu_objects.addAction(self.action_delete_entity)
        self.menu_objects.addSeparator()
        self.menu_views.addAction(self.action_view_metadata)
        self.menu_setting.addAction(self.action_setting_tags)
        self.menu_setting.addAction(self.action_setting_fields)
        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_objects.menuAction())
        self.menubar.addAction(self.menu_views.menuAction())
        self.menubar.addAction(self.menu_setting.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "SmartFiles", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_search.setText(QtGui.QApplication.translate("MainWindow", "Найти", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_request_language.setWhatsThis(QtGui.QApplication.translate("MainWindow", "Поиск на языке запроса. Теги и поля перечисляются через логические операторы: AND, OR, ()", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_request_language.setText(QtGui.QApplication.translate("MainWindow", "На языке запроса", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_neural_net.setWhatsThis(QtGui.QApplication.translate("MainWindow", "Поиск по нейросети. Запрос осуществляется перечислением через пробел тегов. Результат поиска отсортерован по релевантности.", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_neural_net.setText(QtGui.QApplication.translate("MainWindow", "Нейросетью", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_file.setTitle(QtGui.QApplication.translate("MainWindow", "&Файл", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_repo.setTitle(QtGui.QApplication.translate("MainWindow", "&Хранилище", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_users.setTitle(QtGui.QApplication.translate("MainWindow", "&Пользователь", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_objects.setTitle(QtGui.QApplication.translate("MainWindow", "&Объекты", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_add_entity.setTitle(QtGui.QApplication.translate("MainWindow", "&Добавить", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_mark.setTitle(QtGui.QApplication.translate("MainWindow", "&Пометить", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_views.setTitle(QtGui.QApplication.translate("MainWindow", "&Вид", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_setting.setTitle(QtGui.QApplication.translate("MainWindow", "&Метаданные", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.dockWidget_tag.setWindowTitle(QtGui.QApplication.translate("MainWindow", "                                   Метаданные", None, QtGui.QApplication.UnicodeUTF8))
        self.label_users.setText(QtGui.QApplication.translate("MainWindow", "Пользователи хранилища", None, QtGui.QApplication.UnicodeUTF8))
        self.action_exit.setText(QtGui.QApplication.translate("MainWindow", "Выход", None, QtGui.QApplication.UnicodeUTF8))
        self.action_create_repo.setText(QtGui.QApplication.translate("MainWindow", "Создать", None, QtGui.QApplication.UnicodeUTF8))
        self.action_open_repo.setText(QtGui.QApplication.translate("MainWindow", "Открыть", None, QtGui.QApplication.UnicodeUTF8))
        self.action_delete_repo.setText(QtGui.QApplication.translate("MainWindow", "Удалить", None, QtGui.QApplication.UnicodeUTF8))
        self.action_delete_user_from_repo.setText(QtGui.QApplication.translate("MainWindow", "Удалиться из хранилища", None, QtGui.QApplication.UnicodeUTF8))
        self.action_switch_user.setText(QtGui.QApplication.translate("MainWindow", "Сменить пользователя", None, QtGui.QApplication.UnicodeUTF8))
        self.action_add_file.setText(QtGui.QApplication.translate("MainWindow", "Файл", None, QtGui.QApplication.UnicodeUTF8))
        self.action_add_URL.setText(QtGui.QApplication.translate("MainWindow", "URL", None, QtGui.QApplication.UnicodeUTF8))
        self.action_mark_tag.setText(QtGui.QApplication.translate("MainWindow", "Тегом", None, QtGui.QApplication.UnicodeUTF8))
        self.action_mark_field.setText(QtGui.QApplication.translate("MainWindow", "Полем", None, QtGui.QApplication.UnicodeUTF8))
        self.action_change_entity.setText(QtGui.QApplication.translate("MainWindow", "Изменить", None, QtGui.QApplication.UnicodeUTF8))
        self.action_delete_entity.setText(QtGui.QApplication.translate("MainWindow", "Удалить", None, QtGui.QApplication.UnicodeUTF8))
        self.action_view_metadata.setText(QtGui.QApplication.translate("MainWindow", "Метаданные", None, QtGui.QApplication.UnicodeUTF8))
        self.action_setting_tags.setText(QtGui.QApplication.translate("MainWindow", "Теги", None, QtGui.QApplication.UnicodeUTF8))
        self.action_setting_fields.setText(QtGui.QApplication.translate("MainWindow", "Поля", None, QtGui.QApplication.UnicodeUTF8))

