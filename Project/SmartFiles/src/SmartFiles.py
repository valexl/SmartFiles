'''
Created on 17.05.2010

@author: valexl
'''
import sys
from PyQt4 import QtGui,QtCore

from  MainMenu import SmartFilesMainWindow as MainWindow

from RepoManager.SystemInfo import SystemInfo
from RepoManager.User import User
from RepoManager.InstallUser import InstallUser
from RepoManager.RepoManager import RepoManager 

from EditWindows.EditUserWindow import EditUserWindow

from RepoManager.InstallUser import InstallUser


        
class StartWindow(QtGui.QWidget):
    def __init__(self,parent=None):
        try:
            QtGui.QWidget.__init__(self,parent)

#            self.setGeometry(500,400,0,0)
            vbox_layout = QtGui.QVBoxLayout()
            
            hbox_layout = QtGui.QHBoxLayout()
            label = QtGui.QLabel('Логин  ',self)
            self._edit_login = QtGui.QLineEdit(self)
            hbox_layout.addWidget(label)
            hbox_layout.addWidget(self._edit_login)
            vbox_layout.addLayout(hbox_layout)
            
            hbox_layout = QtGui.QHBoxLayout()
            label = QtGui.QLabel('Пароль',self)
            self._edit_password = QtGui.QLineEdit(self)
            self._edit_password.setEchoMode(2)
            hbox_layout.addWidget(label)
            hbox_layout.addWidget(self._edit_password)
            vbox_layout.addLayout(hbox_layout)
            
            hbox_layout = QtGui.QHBoxLayout()
            button_ok=QtGui.QPushButton('Войти')
            button_exit=QtGui.QPushButton('Выход')
            hbox_layout.addWidget(button_ok)
            hbox_layout.addWidget(button_exit)
            vbox_layout.addLayout(hbox_layout)
            
            button_add_user = QtGui.QPushButton('Добавить')
            vbox_layout.addWidget(button_add_user)
            
            self.connect(button_ok,QtCore.SIGNAL('clicked()'),self.__startSF)
            self.connect(button_add_user,QtCore.SIGNAL('clicked()'),self.__createUser)
            self.connect(button_exit,QtCore.SIGNAL('clicked()'),self.close)

            self.info_window = QtGui.QMessageBox()
            self.setLayout(vbox_layout)
            self.info_windo = QtGui.QMessageBox(self)
            self.main_window = None
            
            InstallUser.initHomeDir()
        except InstallUser.ExceptionNoUsers as err:
            print(err)
            self.info_window.setText('''Программа запущена в первый раз.
Для работы с программой необходимо зарегестрировать хотя бы одного пользователя.''')
            self.info_window.show()
            #print('добавьте пользователя для работы в системе')
        
    def __startSF(self):
        '''
            Идентификация пользователя. В случае успеха запуск программы.
        '''        
        try:
            user_name = self._edit_login.text()
            password = hash(self._edit_password.text())
            user_repo = InstallUser.identificationUser(user_name,password)
            self.__starting(user_repo)
            self._edit_password.setText('')
        except InstallUser.ExceptionUserNotFound as err:
            self.info_window.setText('Ошибка логина или пароля')
            self.info_window.show()
            print(err)    
        except InstallUser.ExceptionRepoIsNull as err:
            self.info_window.setText('''Не найдено ни одного пользователя в системе.
Необходимо создать пользователя''')
            self.info_window.show()
            print(err)
        except Exception as err:
            self.info_window.setText('какие то не учтенные траблы')
            self.info_window.show()
            print(err)
            
    def __switchUser(self):
        '''
            переключение пользователя. Закрывается главное окно и отображается окно запуска.
        '''
        #self.main_window.close()
        del(self.main_window)
        self.show()
        
        
    def __starting(self,user_repo):
        '''
            запуск главного окна программы
        '''
        #if self.main_window == None:
        self.main_window = MainWindow(user_repo) 
        self.main_window.show()
        self.connect(self.main_window,QtCore.SIGNAL('switchUser()'),self.__switchUser)
        self.connect(self.main_window,QtCore.SIGNAL('createUser(user)'),InstallUser.addUser)
        self.connect(self.main_window,QtCore.SIGNAL('updateUser(user)'),InstallUser.updateUser)
        #
        self.close()
        
        
    def __createUser(self):
        '''
            Сбор информации необходимой для создание нового пользователя.   
        '''
        try:
            self.edit_window = EditUserWindow()
            self.edit_window.show()
            self.connect(self.edit_window,QtCore.SIGNAL("createUser(user)"),self.__saveUser)
        except Exception as err:
            print(err)
        
    def __saveUser(self,user_repo):
        '''
            сохранение пользователя 
        '''
        try:
           
            InstallUser.addUser(user_repo)
            self.__starting(user_repo)
        except InstallUser.ExceptionUserExist as err:
            print(err)
            
        
        
        
if __name__ == '__main__':
    print('111111')
    app = QtGui.QApplication(sys.argv)
   
    main =  StartWindow()
    main.show()
    print('start StartWindow')
#    sys.exit(app.exec_())
    app.exec_()
    