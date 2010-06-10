'''
Created on 07.06.2010

@author: valexl
'''
import datetime
from PyQt4 import QtGui, QtCore
from RepoManager.User import User
from RepoManager.RepoManager import RepoManager

class EditUserWindow(QtGui.QWidget):
    def __init__(self,status='create',user=None,parent=None):
        
        QtGui.QWidget.__init__(self,parent)
        self._status = status
        self._user = user
        vbox_layout = QtGui.QVBoxLayout()
        
        self.info_window = QtGui.QMessageBox()
        label = QtGui.QLabel('Имя пользователя',self)
        self._edit_user_name = QtGui.QLineEdit(self)
        if not self._status == 'create':
            self._edit_user_name.setText(user.name)
        vbox_layout.addWidget(label)
        vbox_layout.addWidget(self._edit_user_name)
        
        if self._status == 'update':
            label = QtGui.QLabel('введите новый пароль',self)
            self._edit_old_password = QtGui.QLineEdit(self)
            self._edit_old_password.setEchoMode(2)
            vbox_layout.addWidget(label)
            vbox_layout.addWidget(self._edit_old_password)
            label = QtGui.QLabel('введите старый пароль',self)
        else:
            label = QtGui.QLabel('Пароль',self)
            
        self._edit_password = QtGui.QLineEdit(self)
        self._edit_password.setEchoMode(2)
        vbox_layout.addWidget(label)
        vbox_layout.addWidget(self._edit_password)
        
        
        label = QtGui.QLabel('Описание',self)
        self._edit_description = QtGui.QLineEdit(self)
        vbox_layout.addWidget(label)
        vbox_layout.addWidget(self._edit_description)
        
        button_ok = QtGui.QPushButton('Ок',self)
        self.connect(button_ok,QtCore.SIGNAL("clicked()"),self.__pressButtonOk)
        button_cancel = QtGui.QPushButton('Отмена',self)
        self.connect(button_cancel,QtCore.SIGNAL("clicked()"),self.__canceled)
        
        
        hbox_layout = QtGui.QHBoxLayout()
        hbox_layout.addWidget(button_ok)
        hbox_layout.addWidget(button_cancel)
        vbox_layout.addLayout(hbox_layout)
     
        if status=='update':
            self._edit_user_name.setDisabled(1)
        elif status=='delete':
            self._edit_password.setDisabled(1)
            self._edit_description.setDisabled(1)
            
            
     
        self.setLayout(vbox_layout)
        
    def __pressButtonOk(self):
        print('EditUserWindow --- pressButtonOk')
        if self._status == 'create':
            self.__createUser()
        elif self._status == 'update':
            self.__updateUser()
        else:
            self.__deleteUser()
        self.__canceled()
        
        
    def __createUser(self):
        user_name = self._edit_user_name.text()
        password = hash(self._edit_password.text())
        user = User(user_name= user_name,password=password,description=self._edit_description.text(),date_time=datetime.datetime.now())
        self.emit(QtCore.SIGNAL('createUser(user)'),user)
        self.__canceled()
    
    
    def __updateUser(self):
        old_password = hash(self._edit_old_password.text()) 
        if old_password == self._user.password:
            user = User(user_name=self._edit_user_name.text(),password=self._edit_password.text(),description=self._edit_description.text())
            self.emit(QtCore.SIGNAL('updateUser(user)'),user)
            self.__canceled()
        else:
            print(old_password)
            print(self._user.password)
            self.info_window.setText('''неправильный пароль
            ''')
            self.info_window.show()
            raise RepoManager.ExceptionErrorPasswordUser('не правильный пароль')
    
    def __deleteUser(self):
        user = User(self._edit_user_name.text())
        #user_name = self._edit_user_name.text() 
        self.emit(QtCore.SIGNAL('deleteUser(user_name)'),user)
        self.__canceled()
         
    def __canceled(self):
        print('EditUserWindow --- pressButtonCancel')
        self.close()
        del(self)
    
#        
#class SearchWindow(QtGui.QWidget):
#    '''
#        окно расширенного поиска
#        пока не сделано
#    '''
#    def __init__(self,parent=None):
#        QtGui.QWidget.__init__(self,parent)
#        
        