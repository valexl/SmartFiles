'''
Created on 07.06.2010

@author: valexl
'''
from PyQt4 import QtGui, QtCore
from RepoManager.SystemInfo import SystemInfo
from EntityManager.Tag import Tag
from EntityManager.Field import Field

        
class EditMetadataWindow(QtGui.QWidget):
    #переделать окно поотдельности. одно для тегов, другое для полей. Сделать базовое окно редактирования и от 
    #него наследуясь переделать окна. (это если такого плана дизайн будет не временным, а постоянным).
    def __init__(self,user_repo,entity_id,type_metadata='tag',
                 field_type=SystemInfo.field_type_str,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self._type_metadata=type_metadata
        self._user_repo = user_repo
        self._entity_id = entity_id
        
        vbox_layout = QtGui.QVBoxLayout()
        self.info_window = QtGui.QMessageBox()
        hbox_layout = QtGui.QHBoxLayout()
        self._metadata_name = QtGui.QLineEdit(self)
        label = QtGui.QLabel(self)
        hbox_layout.addWidget(label)
        hbox_layout.addWidget(self._metadata_name)
        vbox_layout.addLayout(hbox_layout)
        
        
        if self._type_metadata=='tag':
            label.setText('Имя тега ')
        else:
            label.setText('Имя поля ')
            #self._metadata_name.setText(metadata_name)
            
            
            hbox_layout = QtGui.QHBoxLayout()
            label = QtGui.QLabel('Значение',self)
            self._field_value = QtGui.QLineEdit(self)
            hbox_layout.addWidget(label)
            hbox_layout.addWidget(self._field_value)
            vbox_layout.addLayout(hbox_layout)
            
            hbox_layout = QtGui.QHBoxLayout()
            label = QtGui.QLabel('Тип поля',self)
            self._type_field = QtGui.QComboBox(self)
            self._type_field.addItem(SystemInfo.field_type_str)
            self._type_field.addItem(SystemInfo.field_type_int)
            hbox_layout.addWidget(label)
            hbox_layout.addWidget(self._type_field)
            vbox_layout.addLayout(hbox_layout)

        hbox_layout = QtGui.QHBoxLayout()
                    
        label = QtGui.QLabel('Описание',self)
        self._description = QtGui.QLineEdit(self)
        hbox_layout.addWidget(label)
        hbox_layout.addWidget(self._description)
        vbox_layout.addLayout(hbox_layout)
            
        
        hbox_layout = QtGui.QHBoxLayout()
        button_ok = QtGui.QPushButton('Ок',self)
        button_cancel = QtGui.QPushButton('Отмена',self)
        hbox_layout.addWidget(button_ok)
        hbox_layout.addWidget(button_cancel)
        vbox_layout.addLayout(hbox_layout)
        
        self.setLayout(vbox_layout)
        
        self.connect(button_ok,QtCore.SIGNAL('clicked()'),self.__create)
        self.connect(button_cancel,QtCore.SIGNAL('clicked()'),self.close)
    
    
    def __create(self):
        if not self._metadata_name.text()=='':
            if self._type_metadata=='tag':
                new_tag = Tag(tag_name=self._metadata_name.text(),
                              user_name=self._user_repo.name,
                              description=self._description.text())
                self.emit(QtCore.SIGNAL('mark(entity_id,metadata_obj)'),self._entity_id, new_tag)
                self.__canceled()
            elif self._type_metadata=='field':
                if not self._field_value.text()=='':
                    new_field = Field(field_name=self._metadata_name.text(),
                                      user_name=self._user_repo.name,
                                      field_value=self._field_value.text(),
                                      value_type= self._type_field.currentText(),
                                      field_description=self._description.text())
                    self.emit(QtCore.SIGNAL('mark(entity_id,metadata_obj)'),self._entity_id,new_field)
                    self.__canceled()
                else:
                    self.info_window.setText('''Необходимо ввести для поля значение
            ''')
                    self.info_window.show()
                    
        else:
            self.info_window.setText('поле с именем' + self._type_metadata + 'пустое') 
            self.info_window.show()
            print('поле с именем ' + self._type_metadata + ' пустое')
        
        
        
    def __canceled(self):
        '''
            закрытие окна редактировани метаданных
        '''
        self.close()
        del(self)
    