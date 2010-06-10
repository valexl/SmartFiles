'''
Created on 07.06.2010

@author: valexl
'''
import datetime
from PyQt4 import QtGui, QtCore
from RepoManager.User import User
from RepoManager.RepoManager import RepoManager

class EditUserWindow(QtGui.QDialog):
    def __init__(self,user=None,parent=None):
        
        QtGui.QDialog.__init__(self,parent)
        self.setGeometry(400,500,0,0)
        self.setModal(1)
        
        self._user = user
        vbox_layout = QtGui.QVBoxLayout()
        
        self.info_window = QtGui.QMessageBox()
        label = QtGui.QLabel('Имя пользователя',self)
        self._edit_user_name = QtGui.QLineEdit(self)
        if self._user:
            self._edit_user_name.setText(user.name)
            self._edit_user_name.setDisabled(1)
        
        vbox_layout.addWidget(label)
        vbox_layout.addWidget(self._edit_user_name)
        
        if not self._user == None:
            label = QtGui.QLabel('старый пароль',self)
            self._edit_old_password = QtGui.QLineEdit(self)
            self._edit_old_password.setEchoMode(2)
            vbox_layout.addWidget(label)
            vbox_layout.addWidget(self._edit_old_password)
        
        label = QtGui.QLabel('Пароль',self)    
        self._edit_password = QtGui.QLineEdit(self)
        self._edit_password.setEchoMode(2)
        vbox_layout.addWidget(label)
        vbox_layout.addWidget(self._edit_password)
        
        label = QtGui.QLabel('Проверка пароля',self)
        self._edit_test_password = QtGui.QLineEdit(self)
        self._edit_test_password.setEchoMode(2)
        vbox_layout.addWidget(label)
        vbox_layout.addWidget(self._edit_test_password)
        
        
        label = QtGui.QLabel('Описание',self)
        self._edit_description = QtGui.QLineEdit(self)
        vbox_layout.addWidget(label)
        vbox_layout.addWidget(self._edit_description)
        
        button_ok = QtGui.QPushButton('Ок',self)
        button_cancel = QtGui.QPushButton('Отмена',self)
        hbox_layout = QtGui.QHBoxLayout()
        hbox_layout.addWidget(button_ok)
        hbox_layout.addWidget(button_cancel)   
        vbox_layout.addLayout(hbox_layout)
        
        self.setLayout(vbox_layout)
        
        self.connect(button_ok,QtCore.SIGNAL("clicked()"),self.__pressButtonOk)
        self.connect(button_cancel,QtCore.SIGNAL("clicked()"),self.close)
        
        
    def __pressButtonOk(self):
        '''
            создание или модификация существующего пользователя
        '''
        if self._user:
            self.__updateUser()
        else:
            self.__createUser()
        
        
    def __createUser(self):
        '''
            создание пользователя
        '''
        user_name = self._edit_user_name.text()
        password = self._edit_password.text() 
        if password ==self._edit_test_password.text():
            if not password=='':
                password = hash(password)
                user = User(user_name= user_name,password=password,description=self._edit_description.text(),date_time=datetime.datetime.now())
                self.emit(QtCore.SIGNAL('createUser(user)'),user)
                self.close()
            else:
                self.info_window.setText('Поле пароль не может быть пустым')
                self.info_window.show()
        else:
            self.info_window.setText('''Значение в полях "пароль" и "проверка пароля" дложно быть одинаковым.
Введите заново пароль.
            ''')
            self.info_window.show()
            self._edit_test_password.setText('')
            self._edit_password.setText('')
    
    def __updateUser(self):
        old_password = hash(self._edit_old_password.text()) 
        if old_password == self._user.password:
            user = User(user_name=self._edit_user_name.text(),password=self._edit_password.text(),description=self._edit_description.text())
            self.emit(QtCore.SIGNAL('updateUser(user)'),user)
            self.close()
        else:
            print(old_password)
            print(self._user.password)
            self.info_window.setText('''неправильный пароль
            ''')
            self.info_window.show()
            raise RepoManager.ExceptionErrorPasswordUser('не правильный пароль')
    
    