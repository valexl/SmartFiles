'''
Created on 20.05.2010

@author: valexl
'''
import sys
import os
import shutil
from PyQt4 import QtGui,QtCore,QtSql
from ProcessingRequest import cleareExtraSpace, cleareSpaceAboutOperator 

from EntityManager import EntityManager
from User import User
from Field import Field
from Tag import Tag
import SystemInfo
from RepoManager import RepoManager
#from SmartFiles import MainMenu

#    def __create(self):
#        pass
#    def __delete(self):
#        pass
#    def __update(self):
#        pass
#    
#    def __pressButtonOk(self):
#        '''
#            выполнить действие (создание/удаление/модификация)
#        '''
#        print('кажись хурма получилась')
#        if self._status == 'create':
#            print('create Entity')
#            self.__create()
#        elif self._status == 'delete':
#            self.__delete()
#        else:
#            self.__update()
#       # pass

class EditEntityWindow(QtGui.QWidget):
    def __init__(self, path_repo, user_name, object_type, status='create', file_path=None,id=None, parent=None):
                
        QtGui.QWidget.__init__(self,parent)
        self._object_type = object_type
        self._path_to_repo = path_repo
        self._user_name = user_name
        self._file_path = file_path
        self._status = status
        self._entity_id=id
         
        vbox_layout = QtGui.QVBoxLayout()
        
        #создание виджетов и их расположение на layout
        label = QtGui.QLabel('Заголовок',self)
        self._edit_title = QtGui.QLineEdit(self)
        vbox_layout.addWidget(label)
        vbox_layout.addWidget(self._edit_title)
        
        if self._object_type == SystemInfo.entity_link_type:
            label = QtGui.QLabel('URL',self)
            self._edit_URL = QtGui.QLineEdit(self)
            vbox_layout.addWidget(label)
            vbox_layout.addWidget(self._edit_URL)
        
        label = QtGui.QLabel('Теги',self)
        self._edit_tags = QtGui.QLineEdit(self)
        vbox_layout.addWidget(label)
        vbox_layout.addWidget(self._edit_tags)
        
        label = QtGui.QLabel('Поля',self)
        self._edit_fields = QtGui.QLineEdit(self)
        vbox_layout.addWidget(label)
        vbox_layout.addWidget(self._edit_fields)
        
        label = QtGui.QLabel('Заметки',self)
        self._edit_description = QtGui.QLineEdit(self)
        vbox_layout.addWidget(label)
        vbox_layout.addWidget(self._edit_description)
                    
        button_ok = QtGui.QPushButton('Ок',self)
        button_cancel = QtGui.QPushButton('Отмена',self)
        
        hbox_layout = QtGui.QHBoxLayout()
        hbox_layout.addWidget(button_ok)
        hbox_layout.addWidget(button_cancel)
        vbox_layout.addLayout(hbox_layout)
        #помещение layout на форму
        self.setLayout(vbox_layout)
        
        self.connect(button_cancel,QtCore.SIGNAL('clicked()'),self.__canceled)
        self.connect(button_ok,QtCore.SIGNAL('clicked()'),self.__pressButtonOk)
                
        
    def __canceled(self):
        '''
            завершение работы
        '''
        self.close()
        del(self)
        

    def __pressButtonOk(self):
        '''
            выполнить действие (создание/удаление/модификация)
        '''
        if self._status == 'create':
            print('create Entity')
            self.__create()
        elif self._status == 'delete':
            self.__delete()
        else:
            self.__update()
            
            
    def __getFields(self):
        '''
            возращает список объектов полей
        '''
        list_fields=[]
        fields = self._edit_fields.text()
        if self._object_type == SystemInfo.entity_link_type:
            if len(self._edit_URL.text())>0:
                fields += ' URL=' + self._edit_URL.text( )
            else:
                raise Exception('Заполнить поле URL')
        fields = cleareExtraSpace(fields)
        print('fields',fields)
        if not fields=="":
            fields = cleareSpaceAboutOperator(fields,'=')
           
            fields=fields.split(' ')
            #создавания объектов Field
            for field in fields:
                field_name,field_value = field.split('=')
                list_fields.append(Field(field_name,self._user_name,field_value)) #тип поля по умолчанию стринг
        return list_fields
    
    
    def __getTags(self):
        '''
            возращает список обеъктов тегов
        '''
        tags = cleareExtraSpace(self._edit_tags.text())
        list_tags=[]
        if not tags=="":
            tags = tags.split(' ')
            for tag_name in tags:
                list_tags.append(Tag(tag_name,self._user_name))
        return list_tags
    
    def __create(self):
        '''
            создание нового объекта. Передает с сигналом только что созданный объект Entity
        '''
        #обработка полей
        list_fields = self.__getFields()
        #обработка тегов
        list_tags = self.__getTags()        
        if self._object_type == SystemInfo.entity_link_type:
            entity = EntityManager.createEntity(title=self._edit_title.text(),entity_type=self._object_type,user_name=self._user_name,
                                            list_tags=list_tags,list_fields=list_fields,
                                            notes=self._edit_description.text()) #добавить дату создания
        else:
            entity = EntityManager.createEntity(title=self._edit_title.text(),entity_type=self._object_type,user_name=self._user_name,
                                            list_tags=list_tags,list_fields=list_fields,
                                            notes=self._edit_description.text(),file_path=self._file_path)
        self.emit(QtCore.SIGNAL('createEntity(entity)'),entity)
        self.__canceled()
        
        
        
        
    def __update(self):
        '''
            модификация сущности.
        '''
        list_fields= self.__getFields()
        list_tags= self.__getTags()
        
        entity = EntityManager.createEntity(title=self._edit_title.text(),entity_type=self._object_type,
                                            user_name=self._user_name,file_path=self._file_path, 
                                            list_tags=list_tags,list_fields=list_fields,
                                            id=self._entity_id)

        self.emit(QtCore.SIGNAL('updateEntity(entity)'),entity)    
        self.__canceled()     
    

        
    
        
    
class EditUserWindow(QtGui.QWidget):
    def __init__(self,status='create',user_name='',parent=None):
        
        QtGui.QWidget.__init__(self,parent)
        self._status = status
        
        vbox_layout = QtGui.QVBoxLayout()
        
        
        label = QtGui.QLabel('Имя пользователя',self)
        self._edit_user_name = QtGui.QLineEdit(self)
        self._edit_user_name.setText(user_name)
        
        vbox_layout.addWidget(label)
        vbox_layout.addWidget(self._edit_user_name)
        
        label = QtGui.QLabel('Пароль',self)
        self._edit_password = QtGui.QLineEdit(self)
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
        user = User(self._edit_user_name.text(),self._edit_password.text(),description=self._edit_description.text())
        self.emit(QtCore.SIGNAL('createUser(user)'),user)
        self.__canceled()
    
    
    def __updateUser(self):
        user = User(user_name=self._edit_user_name.text(),password=self._edit_password.text(),description=self._edit_description.text())
        self.emit(QtCore.SIGNAL('updateUser(user)'),user)
        self.__canceled()
    
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
        
        
class EditMetadataWindow(QtGui.QWidget):
    #переделать окно поотдельности. одно для тегов, другое для полей. Сделать базовое окно редактирования и от 
    #него наследуясь переделать окна. (это если такого плана дизайн будет не временным, а постоянным).
    def __init__(self,user_name,type_metadata='tag',status='create',metadata_name='',
                 field_type=SystemInfo.field_type_str,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self._type_metadata=type_metadata
        self._user_name = user_name
        self._status = status
        
        vbox_layout = QtGui.QVBoxLayout()
        
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
            self._metadata_name.setText(metadata_name)
            
            
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
            #если создается новое поле, тогда вывод необходимых для создания поля атрибутов
            if status=="add_value":
                self._type_field.setDisabled(1)
                self._metadata_name.setDisabled(1)
                if field_type==SystemInfo.field_type_int:
                    self._type_field.setCurrentIndex(1)
                else:
                    self._type_field.setCurrentIndex(0)
                
                
             
        if status=="create":
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
        if self._type_metadata=='tag':
            new_tag = Tag(self._metadata_name.text(),self._user_name,description=self._description.text())
            self.emit(QtCore.SIGNAL('mark(metadata_obj)'),new_tag)
        elif self._type_metadata=='field':
            if self._status=='create':
                new_field = Field(self._metadata_name.text(),self._user_name,self._field_value.text(),
                             self._type_field.currentText(),self._description.text())
            else:
                new_field = Field(self._metadata_name.text(),self._user_name,self._field_value.text(),
                             self._type_field.currentText())
            self.emit(QtCore.SIGNAL('mark(metadata_obj)'),new_field)
        else:
            raise Exception('траблы при передачи сигнала из EditMetadataWindow')
        self.__canceled()
        
        
    def __canceled(self):
        '''
            закрытие окна редактировани метаданных
        '''
        self.close()
        del(self)
    
        
class BrowseMetadataWindow(QtGui.QWidget):
    def __init__ (self, entity_id, user_name,type_metadata='tag',status='mark', parent=None):
        
        QtGui.QWidget.__init__(self,parent)
        self._user_name = user_name
        self._entity_id = entity_id
        self._type_metadata = type_metadata
        self._status = status
        
        vbox_layout = QtGui.QVBoxLayout()
        if status=='mark':
            self._str_request_select = "SELECT " + type_metadata + ".* FROM " + type_metadata
            
        
            button_add = QtGui.QPushButton('Пометить',self)
            button_create = QtGui.QPushButton('Создать и пометить',self)
            button_delete = QtGui.QPushButton('Удалить',self)
           # button_cancel = QtGui.QPushButton('Отмена',self)
            
            
            vbox_layout.addWidget(button_add)
            vbox_layout.addWidget(button_create)
            vbox_layout.addWidget(button_delete)
            
            
            self.connect(button_add,QtCore.SIGNAL('clicked()'),self.__add)
            self.connect(button_create,QtCore.SIGNAL('clicked()'),self.__create)    
            self.connect(button_delete,QtCore.SIGNAL('clicked()'),self.__delete)
        else:                           # SELECT     tag.*            FROM    tag,                     entity_tags             WHERE  name =          tag_name        AND 
            self._str_request_select = "SELECT " + type_metadata +".* FROM " + type_metadata + ", entity_" + type_metadata + "s WHERE name = " + type_metadata + "_name AND entity_id = " + str(self._entity_id)
            print(self._str_request_select)
            button_delete = QtGui.QPushButton('Открепить от файла',self)
            vbox_layout.addWidget(button_delete)
            self.connect(button_delete,QtCore.SIGNAL('clicked()'),self.__release)
            
            
        button_cancel = QtGui.QPushButton('Завершить',self)
        vbox_layout.addWidget(button_cancel)
        
        hbox_layout = QtGui.QHBoxLayout()
        self._table = QtGui.QTableView(self)
        hbox_layout.addWidget(self._table)
        
        hbox_layout.addLayout(vbox_layout)
        
        vbox_layout = QtGui.QVBoxLayout()
        vbox_layout.addLayout(hbox_layout)
        self.setLayout(vbox_layout)
        self.connect(button_cancel,QtCore.SIGNAL('clicked()'),self.__cancel)

        self.refresh()
        
    def __cancel(self):
        self.close()
        del(self)
        
        
    def __create(self):
        
        self._edit_window = EditMetadataWindow(self._user_name,self._type_metadata)
        self._edit_window.show()
        self.connect(self._edit_window,QtCore.SIGNAL('mark(metadata_obj)'),self.__pushSignal)
        
        
    def __pushSignal(self,metadata_obj):

        if self._type_metadata=='tag':
            print('push markTag signal')
            self.emit(QtCore.SIGNAL('markTag(entity_id,tag)'),self._entity_id,metadata_obj)
        elif self._type_metadata=='field':
            print('push markField signal')    
            self.emit(QtCore.SIGNAL('markField(entity_id,field)'),self._entity_id,metadata_obj)
        else:
            raise Exception('траблы с типом создаваемого объекта (ни tag и ни field) не правильно указан параметр')
        
        #self.__cancel()
        

    def __getSelectingData(self,type_metadata='tag'):
        '''
            получить необходимые данные из выбранной записи
        '''
        row=self._table.currentIndex().row()
        index=self._table.model().index(row,0)
        metadata_name = self._table.model().data(index)
        if metadata_name==None:
            raise Exception('не выбрана запись для действия')
        if type_metadata=='field':
            index = self._table.model().index(row,3)
            field_type=self._table.model().data(index)
            return (metadata_name,field_type)
        return metadata_name
            
    def __add(self):
        '''
            добавление нового тега или поля
        '''
        print('addMetadata')
            

        if self._type_metadata=='tag':
            metadata_name=self.__getSelectingData()
            print('tag')
            adding_obj = Tag(metadata_name,self._user_name)
            self.__pushSignal(adding_obj)
        else:
            print('field')
            metadata_name, field_type = self.__getSelectingData('field')
            print(field_type)
            self._edit_window = EditMetadataWindow(self._user_name,self._type_metadata,
                                                       metadata_name = metadata_name,status='add_value',
                                                       field_type=field_type)
            self._edit_window.show()
            self.connect(self._edit_window,QtCore.SIGNAL('mark(metadata_obj)'),self.__pushSignal)
            
        
    def __delete(self):
        '''
            удаление тега или поля
        '''    
        print('deleteTag')
        metadata_name=self.__getSelectingData()
        if self._type_metadata=='tag':
            deleting_metadata_obj = Tag(metadata_name,self._user_name)
            self.emit(QtCore.SIGNAL('deleteTag(tag)'),deleting_metadata_obj)
        else:
            print('start deleting field')
            deleting_metadata_obj = Field(metadata_name,self._user_name)
            self.emit(QtCore.SIGNAL('deleteField(field)'),deleting_metadata_obj)
        self.refresh()
        
    def __release(self):
        '''
            освобождение entity от тега или поля
        '''
        print('releaseMetadata')
        
        if self._type_metadata=='tag':
            metadata_name=self.__getSelectingData()
            print('start releasing tag')
            deleting_metadata_obj = Tag(metadata_name,self._user_name)
            self.emit(QtCore.SIGNAL('releaseTag(entity_id,tag)'),self._entity_id,deleting_metadata_obj)
        else:
            print('start releasing field')
            metadata_name, field_type=self.__getSelectingData('field')
            deleting_metadata_obj = Field(metadata_name,self._user_name,field_type)
            self.emit(QtCore.SIGNAL('releaseField(entity_id,field)'),self._entity_id,deleting_metadata_obj)
        self.refresh()
        
    def refresh(self):
        '''
            настройка модели
        '''
        self._model = QtSql.QSqlQueryModel()
        #self._model.setTable(self._type_metadata)
        
        self._model.setQuery(self._str_request_select)
        #self._model.select()
        if (self._model.lastError().isValid()):
            print('eroro in model where connecting BD file')
        self._table.setModel(self._model)
        self._table.show()
        
    def __connnectBD(self):
        '''
               подключение к БД с метаинформацией хранилщиа
        '''
        try:
            self.refresh()
        except Exception as error:
            print('проблемы при подключении к БД или ее настройки')
            print(error)   
    
    
#        
        
class EditFilesWindow(QtGui.QWidget):
    def __init__(self, repo_path, parent=None):
        QtGui.QWidget.__init__(self,parent)
        self._path_to_repo = repo_path
        
        self._file_path_copy = QtGui.QLineEdit(self)
        self._dir_path_recive = QtGui.QLineEdit(self)
        vbox_layout = QtGui.QVBoxLayout()
        
        label = QtGui.QLabel('Копируемый файл')
        vbox_layout.addWidget(label)
        
        button_open = QtGui.QPushButton('...',self)
        self.connect(button_open,QtCore.SIGNAL('clicked()'),self.__selectFile)
        hbox_layout = QtGui.QHBoxLayout()
        hbox_layout.addWidget(self._file_path_copy)
        hbox_layout.addWidget(button_open)
        vbox_layout.addLayout(hbox_layout)
        
        label = QtGui.QLabel('Директория хранилища')
        vbox_layout.addWidget(label)
        
        button_open = QtGui.QPushButton('...',self)
        self.connect(button_open,QtCore.SIGNAL('clicked()'),self.__selectDir)
        hbox_layout = QtGui.QHBoxLayout()
        hbox_layout.addWidget(self._dir_path_recive)
        hbox_layout.addWidget(button_open)
        vbox_layout.addLayout(hbox_layout)
        
        button_ok = QtGui.QPushButton('Сохранить',self)
        button_cancel = QtGui.QPushButton('Отменить',self)
        hbox_layout = QtGui.QHBoxLayout()
        hbox_layout.addWidget(button_ok)
        hbox_layout.addWidget(button_cancel)
        vbox_layout.addLayout(hbox_layout)
        
        self.setLayout(vbox_layout)
        
        self.connect(button_ok,QtCore.SIGNAL('clicked()'),self.__saveFile)
        self.connect(button_cancel,QtCore.SIGNAL('clicked()'),self.__cancel)
        
    def __saveFile(self):
        '''
            сохранения инфомрации о копировании и передача ее в окно BrowseFilesWindow
        '''
        self.emit(QtCore.SIGNAL('copyFileInRepo(copy_info)'),(self._file_path_copy.text(),self._dir_path_recive.text()))
        self.close()
        
        
    def __cancel(self):
        '''
            отмена копирования и передача окну BrowseFilesWindow сигнала об отмене копирования  
        '''
        #self.emit(QtCore.SIGNAL('closeEditFilesWindow()'))
        self.close()
        del(self)
        
    def __selectFile(self):
        '''
            сбор информации о файле коипрования
        '''
        self._file_path_copy.setText(QtGui.QFileDialog.getOpenFileName(self,'Выберите файл для копирования', '/'))
        
        
    def __selectDir(self):
        '''
            сбор информации о директории копирования
        '''
        self._dir_path_recive.setText(QtGui.QFileDialog.getExistingDirectory(self,'Выберите директорию для сохранения',self._path_to_repo))
    
        
class BrowseFilesWindow(QtGui.QWidget):
    '''
        окно для работы с файлами хранилища (добавление новых файлов, удаление существующих, пометка метаинформацией)
    '''
    def __init__(self,user_name, path_to_repo, parent=None):
        QtGui.QWidget.__init__(self,parent)
        self._user_name = user_name
        self._path_to_repo = path_to_repo
        
        vbox_layout = QtGui.QVBoxLayout()
        button_indexing = QtGui.QPushButton('Проиндексировать',self)
        button_add = QtGui.QPushButton('Добавить в хранилище',self)
        button_delete = QtGui.QPushButton('Удалить',self)
        button_cancel = QtGui.QPushButton('Выход',self)
        
        vbox_layout.addWidget(button_indexing)
        vbox_layout.addWidget(button_add)
        vbox_layout.addWidget(button_delete)
        vbox_layout.addWidget(button_cancel)
        
        hbox_layout = QtGui.QHBoxLayout()
        self._table = QtGui.QTableView(self)
        hbox_layout.addWidget(self._table)
        hbox_layout.addLayout(vbox_layout)
        self.setLayout(hbox_layout)
        
        
        self.connect(button_indexing,QtCore.SIGNAL('clicked()'),self.__indexingFile)
        self.connect(button_add,QtCore.SIGNAL('clicked()'),self.__copyFile)
        self.connect(button_delete,QtCore.SIGNAL('clicked()'),self.__deleteFile)
        self.connect(button_cancel,QtCore.SIGNAL('clicked()'),self.__cancel)
        
        self.refresh()
        
    def __cancel(self):
        '''
            выход из окна добавления
        '''
        self.close()
        del(self)
    
        
    def __copyFile(self):
        '''
            вызывает вспомогательное окно для указания файла для копирования и директории хранилища, куда файл будет сохранен
        '''
        self._edit_window = EditFilesWindow(self._path_to_repo)
        self._edit_window.show()
        self.connect(self._edit_window,QtCore.SIGNAL('copyFileInRepo(copy_info)'),self.__saveFile)
    #    self.connect(self._edit_window,QtCore.SIGNAL('closeEditFilesWindow()'),self.__deleteEditFilesWindow)
    
    
  
    def __splitDirPath(self,file_path):
        '''
            получение относительного пути файла.
            путь относительно хранилища
        '''
        
        split_repodir_path = self._path_to_repo.split(os.sep)
        split_file_path = file_path.split(os.sep)
        len_repodir = len(split_repodir_path)
        result_file_path =''
        index = len_repodir
        while index < len(split_file_path):
            result_file_path += os.sep + split_file_path[index] 
            index+=1
        return result_file_path

            
    
    def __saveFile(self,copy_info):    
        '''
            сохранение файла в хранилщие  
        '''
        
        file_name = os.path.split(copy_info[0])[1] 
        file_path = os.path.join(copy_info[1],file_name)
        shutil.copyfile(copy_info[0], file_path)
        
        file_path_to_BD = self.__splitDirPath(file_path)
        self.emit(QtCore.SIGNAL('saveFileInfo(file_path)'),file_path_to_BD)
        self.refresh()
        
        
    def __indexingFile(self):
        '''
            пометка файла метоинформацией. создается запись о файле в БД
        '''
        print('addFile')
        row=self._table.currentIndex().row()
        index = self._table.model().index(row,0)
        file_path = self._table.model().data(index)
        if not file_path==None:
            self.emit(QtCore.SIGNAL('indexingFile(file_path)'),file_path)
        #self.__cancel()
            
        
    def __saveFileEntity(self):
            self.edit_window = EditEntityWindow(self._user_name,self._path_to_repo,SystemInfo.entity_file_type,file_path)
            self.edit_window.show()
            self.connect(self.edit_window,QtCore.SIGNAL('createEntity(entity)'),self.__pushSignal)
    def __pushSignal(self,entity):
        '''
            отправляет сигнал на создания объекта entity
        '''
        self.emit(QtCore.SIGNAL('createEntity(entity)'),entity)
        #RepoManager.deleteFilesInfo(self._path_to_repo,entity.file_path)
        #self.__cancel()
    
    def __deleteFile(self):
        '''
            удаления файла из хранилища
        '''    
        print('deleteFile')
        
        row=self._table.currentIndex().row()
        index=self._table.model().index(row,0)
        file_path=self._table.model().data(index)
        print('row',row)
        print('index',index)
        print('id',id)
        if not file_path==None:
            os.remove(self._path_to_repo + os.sep + file_path)
            self.emit(QtCore.SIGNAL('deleteFileInfo(file_path)'),file_path)
        self.refresh()
        
    def refresh(self):
        '''
            настройка модели
        '''
        print('refresh')
        self._model = QtSql.QSqlTableModel()
        self._model.setTable('files_info')
        #self._model.setQuery(self._string_request)
        self._model.select()
        if (self._model.lastError().isValid()):
            print('eroro in model where connecting BD file')
        self._table.setModel(self._model)
        self._table.show()
        
        
def splitDirPath(parent_dir,file_path):
    split_repodir_path = parent_dir.split(os.sep)
    split_file_path = file_path.split(os.sep)
    index = 0
    result_file_path =os.sep
    for dir_name in split_repodir_path:
        if not dir_name==split_file_path[index]:
            
            while index<len(split_file_path):
                print(index,'=',result_file_path)
                result_file_path += split_file_path[index] + os.sep
                index+=1
            
            return result_file_path
        index +=1
    
    
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window=[]
#    window.append(EditEntityWindow('valex','/tmp/',object_type=SystemInfo.entity_link_type))
#    window.append(EditUserWindow())
#    window.append(EditMetadataWindow('valexl','tag'))
#    window.append(EditMetadataWindow('valexl','field'))
#    window.append(EditFilesWindow('/tmp/tmp'))
#    window.append(BrowseFilesWindow('valex','/tmp/tmp'))
    window.append( BrowseMetadataWindow('valex','/tmp/tmp',type_metadata='tag'))
#    window = EditMetadataWindow('valexl','field',status='add_value',field_type=SystemInfo.field_type_int)
#    window = EditFilesWindow('/tmp/tmp/')
#    window.append(EditEntityWindow('/tmp/','valexl',object_type=SystemInfo.entity_link_type))
    for win in window:
        win.show()
    sys.exit(app.exec_())


    