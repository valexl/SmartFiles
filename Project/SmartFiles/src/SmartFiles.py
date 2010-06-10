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


#from EntityManager.Field import Field
#from EntityManager.Tag import Tag
#from EntityManager.Entity import Entity
#from EntityManager.EntityManager import EntityManager
#from RepoManager.RepoManager import RepoManager
#
#from ProcessingRequest.ProcessingRequest import ProcessingRequest




#import MainForm


height = 500
width = 1000
SQLRequest = "SELECT entity.* FROM entity "

        
class StartWindow(QtGui.QWidget):
    def __init__(self,parent=None):
        try:
            QtGui.QWidget.__init__(self,parent)
            self.setGeometry(500,400,0,0)
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
            
            
            #hbox_layout = QtGui.QHBoxLayout()
            button_add_user = QtGui.QPushButton('Добавить')
            vbox_layout.addWidget(button_add_user)
#            button_delete_user = QtGui.QPushButton('Удалить')
#            vbox_layout.addWidget(button_delete_user)
            #vbox_layout.addLayout(hbox_layout)
            
            self.connect(button_ok,QtCore.SIGNAL('clicked()'),self.__startSF)
            self.connect(button_add_user,QtCore.SIGNAL('clicked()'),self.__createUser)
            self.connect(button_exit,QtCore.SIGNAL('clicked()'),self.close)
#            self.connect(button_delete_user,QtCore.SIGNAL('clicked()'),self.__deleteUser)
            self.info_window = QtGui.QMessageBox()
            self.setLayout(vbox_layout)
            print(self.geometry())
            #
            
            InstallUser.initHomeDir()
        except InstallUser.ExceptionNoUsers as err:
            print(err)
            self.info_window.setText('''Не зарегистрировано не одного пользователя.
Добавьте пользователя для работы в системе.''')
            self.info_window.show()
            print('добавьте пользователя для работы в системе')
        
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
            print('А юзер то не найден')
            print(err)
        except RepoManager.ExceptionRepoIsNull as err:
            print('Необходимо создать пользователя!')
            print(err)
#        except Exception as err:
#            print('траблы с базой')
#            print(err)
            
    def __switchUser(self):
        '''
            переключение пользователя. Закрывается главное окно и отображается окно запуска.
        '''
        self.mainWindow.close()
        del(self.mainWindow)
        self.show()
        
        
    def __starting(self,user_repo):
        '''
            запуск главного окна программы
        '''
        self.mainWindow =MainWindow(user_repo) 
        self.mainWindow.show()
        self.connect(self.mainWindow,QtCore.SIGNAL('switchUser()'),self.__switchUser)
        self.connect(self.mainWindow,QtCore.SIGNAL('createUser(user)'),InstallUser.addUser)
        self.connect(self.mainWindow,QtCore.SIGNAL('updateUser(user)'),InstallUser.updateUser)
        self.close()
        
        
    def __createUser(self):
#        '''
#            Сбор информации необходимой для создание нового пользователя.   
#        '''
#        try:
            self.edit_window = EditUserWindow('create')
            self.edit_window.show()
            self.connect(self.edit_window,QtCore.SIGNAL("createUser(user)"),self.__saveUser)
#        except Exception as err:
#            print(err)
        
    def __saveUser(self,user_repo):
        '''
            сохранение пользователя 
        '''
        print('__saveUser')
        try:
           
            InstallUser.addUser(user_repo)
            self.__starting(user_repo)
        except InstallUser.ExceptionUserExist as err:
            print(err)
            
            
    def __deleteUser(self):
        try:
            self.edit_window = EditUserWindow('delete')
            self.edit_window.show()
            self.connect(self.edit_window,QtCore.SIGNAL("createUser(user)"),self.__deletingUser)
        except Exception as err:
            print(err)
        
        
        
if __name__ == '__main__':
    
    app = QtGui.QApplication(sys.argv)
    user = User('valexl',111,SystemInfo.user_type_admin)
    
    #main = MainWindow(user)
    main =  StartWindow()
    main.show()
    sys.exit(app.exec_())
    main._db.close()