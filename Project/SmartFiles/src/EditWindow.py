'''
Created on 20.05.2010

@author: valexl
'''
import sys
import os
import shutil
from PyQt4 import QtGui,QtCore,QtSql


from ProcessingRequest.ProcessingRequest import cleareExtraSpace, cleareSpaceAboutOperator 
from RepoManager.SystemInfo import SystemInfo
from EntityManager.EntityManager import EntityManager
from RepoManager.User import User
from EntityManager.Field import Field
from EntityManager.Tag import Tag
from RepoManager.RepoManager import RepoManager



        
class EditEntityWindow(QtGui.QDialog):
    def __init__(self,path_to_repo, user_repo,object_type,entity=None,parent=None):
        QtGui.QDialog.__init__(self,parent)
        self._object_type = object_type
        self._user_repo = user_repo
        self._path_to_repo = path_to_repo
        self._entity = entity
        
        
        
        vbox_layout = QtGui.QVBoxLayout()
        
        #создание виджетов и их расположение на layout
        label = QtGui.QLabel('Заголовок',self)
        self._edit_title = QtGui.QLineEdit(self)
        vbox_layout.addWidget(label)
        vbox_layout.addWidget(self._edit_title)
        
        if self._object_type == SystemInfo.entity_link_type:
            label = QtGui.QLabel('URL',self)
            self._edit_path = QtGui.QLineEdit(self)
            if not self._entity == None:
                URL_data=''
                for field in self._entity.getFieldAttributes():
                    if field[0][0]=='url':
                        URL_data=field[1][0] #запись данных из поля URL
                        break
                if URL_data=='':
                    raise EntityManager.ExceptionNotFoundEntityData('не найден URL ссылка для объекта ' + entity.title)
                self._edit_path.setText(URL_data)
            vbox_layout.addWidget(label)
            vbox_layout.addWidget(self._edit_path)
        else:
            label = QtGui.QLabel('Путь к файлу',self)
            self._edit_path = QtGui.QLineEdit(self)
            button_browse = QtGui.QPushButton('...',self)
            
            if not self._entity == None:
                self._edit_path.setText(self._entity.file_path)
                self._edit_path.setDisabled(1)
                button_browse.setDisabled(1)
            vbox_layout.addWidget(label)
            hbox_layout = QtGui.QHBoxLayout()
            hbox_layout.addWidget(self._edit_path)
            hbox_layout.addWidget(button_browse)
            vbox_layout.addLayout(hbox_layout)
            
            self.connect(button_browse,QtCore.SIGNAL('clicked()'),self.__browseFile)
            
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
                    
                    
        if not self._entity == None:
            self._edit_title.setText(self._entity.title)
            self._edit_description.setText(self._entity.notes)
            tag_names=''
            for tag in self._entity.list_tags:
                tag_names += tag.name + ' '
            self._edit_tags.setText(tag_names)
            fields=''
            for field in self._entity.list_fields:
                if field.name =='url':
                    continue
                fields+= ' ' + field.name+'='+field.value
            self._edit_fields.setText(fields)
                    
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
        
        

    def __browseFile(self):
        '''
            выбор файла для сохранения в хранилище
        '''
        file_dialog = QtGui.QFileDialog(self)
        file_dialog.setFileMode(QtGui.QFileDialog.ExistingFiles)
        
        
        list_files_names = file_dialog.getOpenFileNames(self,'выберити файлы для добавления',self._path_to_repo)
        files=self._edit_path.text()
        files=files.strip()
        
        if not files=='':
            if not files[-1]==';':
                files+=';'
                
        for file_name in list_files_names:
            files= files +  file_name + ';'
        files=files[0:-1]
        self._edit_path.setText(str(files))
        
        
    def __canceled(self):
        '''
            завершение работы
        '''
        self.close()
        del(self)
        

    def __pressButtonOk(self):
        '''
            выполнить действие (создание/модификация)
        '''
        #if self._object_type =='
        if not self._edit_path.text()=='':
            if self._entity == None:
                    print('create Entity')
                    self.__create()
            else:
                if self._entity.id ==None:
                    print('create Entity')
                    self.__create()
                else:
                    self.__update()
        else:
            print('хм.. наглец однако.. ну ни чего.. файл выберишь, исправишься:)')
            
            
    def __getFields(self):
        '''
            возращает список объектов полей
        '''
        list_fields=[]
        fields = self._edit_fields.text()
        if self._object_type == SystemInfo.entity_link_type:
            if len(self._edit_path.text())>0:
                fields += ' URL=' + self._edit_path.text( )
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
                list_fields.append(Field(field_name,self._user_repo.name,field_value)) #тип поля по умолчанию стринг
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
                list_tags.append(Tag(tag_name,self._user_repo.name))
        return list_tags
    
    
    def __splitFileByRepo(self,file_path):        
        '''
            отделение от пути файла путь к хранилищу. Если файл не принадлежит хранилищу, то копируется в корень хранилища.
        '''
        print('splitFileByRepo')
        part_dirs, file_name = os.path.split(file_path)
        part_dirs = part_dirs.split(os.path.sep)
        print(part_dirs)
        repo_path_dirs = self._path_to_repo.split(os.path.sep)
        print(repo_path_dirs)
        index = 0
        for dir_name in repo_path_dirs:
            print('dir_name=',dir_name)
            print('part_dirs[',index,']=',part_dirs[index])
            if not dir_name == part_dirs[index]:
                    shutil.copyfile(file_path, self._path_to_repo + os.path.sep + file_name)
                    return file_name                
            index+=1 
        result_path = ''
     
        for pos in range(index,len(part_dirs)):
            result_path+= os.path.sep + part_dirs[pos]
            
        result_path = result_path + os.path.sep + file_name
        result_path = result_path[1:]
        print('aaaaaaaaaaaaaaaaaaaaa-',result_path)
        return result_path 
    
    
    
    def __create(self):
        '''
            создание нового объекта. Передает с сигналом только что созданный объект Entity
        '''
        
        #обработка полей
        list_fields = self.__getFields()
        #обработка тегов
        list_tags = self.__getTags()  
        list_entityes = []      
        if self._object_type == SystemInfo.entity_link_type:
            list_entityes.append(EntityManager.createEntity(title=self._edit_title.text(),entity_type=self._object_type,user_name=self._user_repo.name,
                                            list_tags=list_tags,list_fields=list_fields,
                                            notes=self._edit_description.text())) #добавить дату создания
        else:
            files_names = self._edit_path.text()
            print(files_names)
            #files_names = cleareExtraSpace(files_names)
            list_files = files_names.split(';')
            list_files_names=[]
            for file_name in list_files: # убираются лишнии пробелы в начале и конце строки. Если пользователь вводил файлы вручную
                list_files_names.append(file_name.strip())

            count_files = len(list_files_names)
            
            
#            self.setDisabled(1)
            progress_window = QtGui.QProgressDialog(self)
#            progress_window.setWindowModality(1)
            progress_window.setMinimum(0)
            progress_window.setMaximum(100)
            progress_window.show()
            self.connect(progress_window,QtCore.SIGNAL('canceled()'),self.__stoped)
            d_progress = 100/count_files
            progress = 0
            for file_path in list_files_names:
                progress_window.setValue(progress)
                QtGui.QApplication.processEvents()
                file_repo_path = self.__splitFileByRepo(file_path)
                print(self._path_to_repo)
                print('file_repo_path',file_repo_path)
                list_entityes.append(EntityManager.createEntity(title=self._edit_title.text(),entity_type=self._object_type,user_name=self._user_repo.name,
                                            list_tags=list_tags,list_fields=list_fields,
                                            notes=self._edit_description.text(),file_path=file_repo_path))
                print('progress---',progress)
                print('dprogress---',d_progress)
                
                progress+=d_progress
                progress_window.setValue(progress)
                QtGui.QApplication.processEvents()
#            progress_window.setWindowModality(0)    
            print('deleting progress window')
            del(progress_window)
        print('the lenght outputting signal is -',len(list_entityes))
        self.emit(QtCore.SIGNAL('createEntity(list_entityes)'),list_entityes)
        self.__canceled()
    def __stoped(self):
        pass
        print('процесс копирования не выполнен до конца')
    def __update(self):
        '''
            модификация сущности.
        '''
        list_fields= self.__getFields()
        list_tags= self.__getTags()
        
        entity = EntityManager.createEntity(title=self._edit_title.text(),entity_type=self._entity.object_type,
                                            user_name=self._user_repo.name,file_path=self._entity.file_path, 
                                            list_tags=list_tags,list_fields=list_fields,
                                            id=self._entity.id)

        self.emit(QtCore.SIGNAL('updateEntity(list_entityes)'),(self._entity,entity))    
        self.__canceled()     
    

        
    
        
    
class EditUserWindow(QtGui.QWidget):
    def __init__(self,status='create',user=None,parent=None):
        
        QtGui.QWidget.__init__(self,parent)
        self._status = status
        self._user = user
        vbox_layout = QtGui.QVBoxLayout()
        
        
        label = QtGui.QLabel('Имя пользователя',self)
        self._edit_user_name = QtGui.QLineEdit(self)
        if self._status == 'create':
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
        user = User(self._edit_user_name.text(),self._edit_password.text(),description=self._edit_description.text())
        self.emit(QtCore.SIGNAL('createUser(user)'),user)
        self.__canceled()
    
    
    def __updateUser(self):
        if self._edit_password.text()==str(self._user.password):
            user = User(user_name=self._edit_user_name.text(),password=self._edit_password.text(),description=self._edit_description.text())
            self.emit(QtCore.SIGNAL('updateUser(user)'),user)
            self.__canceled()
        else:
            print(self._edit_password.text())
            print(self._user.password)
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
                    print('введите значение для поля')
            
        else:
            print('поле с именем ' + self._type_metadata + ' пустое')
        
        
        
    def __canceled(self):
        '''
            закрытие окна редактировани метаданных
        '''
        self.close()
        del(self)
    
        
class BrowseMetadataWindow(QtGui.QWidget):
    def __init__ (self,user_repo,type_metadata='tag',parent=None):
        
        QtGui.QWidget.__init__(self,parent)
        self._user_repo = user_repo
        self._str_request_select = "SELECT " + type_metadata + ".* FROM " + type_metadata
        self._type_metadata = type_metadata
        
        
        vbox_layout = QtGui.QVBoxLayout()
        
        button_delete = QtGui.QPushButton('Удалить',self)   
        vbox_layout.addWidget(button_delete)
        
        button_cancel = QtGui.QPushButton('Завершить',self)
        vbox_layout.addWidget(button_cancel)
        
        
        hbox_layout = QtGui.QHBoxLayout()
        
        self._table = QtGui.QTableView(self)
        hbox_layout.addWidget(self._table)
        hbox_layout.addLayout(vbox_layout)
        vbox_layout = QtGui.QVBoxLayout()
        vbox_layout.addLayout(hbox_layout)
        self.setLayout(vbox_layout)
        self.refresh()
        
        self.connect(button_delete,QtCore.SIGNAL('clicked()'),self.__delete)
        self.connect(button_cancel,QtCore.SIGNAL('clicked()'),self.__cancel)
        
        
    def __cancel(self):
        '''
            завершение работы с окном 
        '''
        self.close()
        del(self)
        
        
        

    def __getSelectingData(self,type_metadata='tag'):
        '''
            получить необходимые данные из выбранной записи
        '''
        row=self._table.currentIndex().row()
        index=self._table.model().index(row,0)
        metadata_name = self._table.model().data(index)
        if metadata_name==None:
            print('не выбрана запись для действия')
        if type_metadata=='field':
            index = self._table.model().index(row,3)
            field_type=self._table.model().data(index)
            return (metadata_name,field_type)
        return metadata_name
            
            
        
    def __delete(self):
        '''
            удаление тега или поля
        '''    
        print('deleteTag')
        metadata_name=self.__getSelectingData(self._type_metadata)
        if self._type_metadata=='tag':
            deleting_metadata_obj = Tag(metadata_name,self._user_repo.name)
            self.emit(QtCore.SIGNAL('deleteTag(tag)'),deleting_metadata_obj)
        else:
            print('start deleting field')
            field_name, field_type = metadata_name
            deleting_metadata_obj = Field(field_name=field_name,user_name=self._user_repo.name,value_type=field_type)
            self.emit(QtCore.SIGNAL('deleteField(field)'),deleting_metadata_obj)
        self.refresh()
        
#    def __release(self):
#        '''
#            освобождение entity от тега или поля
#        '''
#        print('releaseMetadata')
#        
#        if self._type_metadata=='tag':
#            metadata_name=self.__getSelectingData()
#            print('start releasing tag')
#            deleting_metadata_obj = Tag(metadata_name,self._user_repo)
#            self.emit(QtCore.SIGNAL('releaseTag(entity_id,tag)'),self._entity_id,deleting_metadata_obj)
#        else:
#            print('start releasing field')
#            metadata_name, field_type=self.__getSelectingData('field')
#            deleting_metadata_obj = Field(metadata_name,self._user_repo,field_type)
#            self.emit(QtCore.SIGNAL('releaseField(entity_id,field)'),self._entity_id,deleting_metadata_obj)
#        self.refresh()
        
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
        self._dir_path_recive.setText(repo_path)
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
        #self.closeEvent()
        self.connect(self,QtCore.SIGNAL('closeEvent(QCloseEvent*))'),self.tmp)
    def closeEvent(self,event):
        print('asdfa')
        pass
        
    
    def __isRepo(self,dir_path):
        list_dir_path = dir_path.split(os.path.sep)
        index=0
        for repo_dir in self._path_to_repo.split(os.path.sep):
            if not repo_dir==list_dir_path[index]:
                return False
            index+=1                
        return True
    def __saveFile(self):
        '''
            сохранения инфомрации о копировании и передача ее в окно BrowseFilesWindow
        '''
        dir_path = self._dir_path_recive.text()
        if self.__isRepo(dir_path):
            if not self._file_path_copy.text()=='':
                files_names= self._file_path_copy.text()
                list_files = files_names.split(';')
                list_files_names=[]
                for file_name in list_files: # убираются лишнии пробелы в начале и конце строки. Если пользователь вводил файлы вручную
                    list_files_names.append(file_name.strip())
                 
                print('list_files_names-',list_files_names)
                print('dir_path',dir_path)
                self.emit(QtCore.SIGNAL('copyFileInRepo(copy_info)'),(list_files_names,dir_path))
                self.close()
            else:
                print('епт.. файл выбери!')
        else:
            print('косарезик... директория куда собираешься сохранять - не хранилище то')
        
        
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
        
        file_dialog = QtGui.QFileDialog(self)
        file_dialog.setFileMode(QtGui.QFileDialog.ExistingFiles)
        
        
        list_files_names = file_dialog.getOpenFileNames(self,'выберити файлы для добавления',self._path_to_repo)
        files=self._file_path_copy.text()
        files=files.strip()
        
        if not files=='':
            if not files[-1]==';':
                files+=';'
                
        for file_name in list_files_names:
            files= files +  file_name + ';'
        files=files[0:-1]
        self._file_path_copy.setText(str(files))
        
        
        
    def __selectDir(self):
        '''
            сбор информации о директории копирования
        '''
        self._dir_path_recive.setText(QtGui.QFileDialog.getExistingDirectory(self,'Выберите директорию для сохранения',self._path_to_repo))
    
        
class BrowseFilesWindow(QtGui.QWidget):
    '''
        окно для работы с файлами хранилища (добавление новых файлов, удаление существующих, пометка метаинформацией)
    '''
    def __init__(self, path_to_repo,user_repo, parent=None):
        QtGui.QWidget.__init__(self,parent)
        self._user_repo = user_repo
        self._path_to_repo = path_to_repo
        
        vbox_layout = QtGui.QVBoxLayout()
        button_indexing = QtGui.QPushButton('Присвоить себе',self)
        button_add = QtGui.QPushButton('Скопировать в хранилище',self)
        button_delete = QtGui.QPushButton('Удалить из хранилища',self)
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
        
        list_file_name = copy_info[0] 
        progress_dialog = QtGui.QProgressDialog(self)
        progress_dialog.setWindowModality(1)
        d_progress = 100/len(list_file_name)
        progress = 0
        for copy_file_path in list_file_name:
            #file_name = os.path.split(file_name[0])[1]
            QtGui.QApplication.processEvents()
            print('copy_file_path',copy_file_path)
            file_name = os.path.split(copy_file_path)[1]
            print('file_name-',file_name)
            print('dir_name',copy_info[1]) 
            file_path = os.path.join(copy_info[1],file_name)
            print('file_path-',file_path)
            shutil.copyfile(copy_file_path, file_path)
            file_path_to_BD = self.__splitDirPath(file_path)
            self.emit(QtCore.SIGNAL('saveFileInfo(file_path)'),file_path_to_BD)
            progress+=d_progress
            progress_dialog.setValue(int(progress))
            QtGui.QApplication.processEvents()
        #self.refresh()
        
        
    def __indexingFile(self):
        '''
            пометка файла метоинформацией. создается запись о файле в БД
        '''
        print('addFile')
        row=self._table.currentIndex().row()
        index = self._table.model().index(row,0)
        file_path = self._table.model().data(index)
        if not file_path==None:
            file_path = self._path_to_repo + os.path.sep + file_path 
            entity = EntityManager.createEntity(entity_type=SystemInfo.entity_file_type, user_name=self._user_repo, file_path=file_path)
            self.emit(QtCore.SIGNAL('indexingFile(entity)'),entity)
        else:
            print('не забываем выбирать файл')
        #self.__cancel()
            
        
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
    user_repo = User('valex', 123)
#    window.append(EditEntityWindow('valex','/tmp/',object_type=SystemInfo.entity_link_type))
#    window.append(EditUserWindow())
#    window.append(EditMetadataWindow('valexl','tag'))
#    window.append(EditMetadataWindow('valexl','field'))
#    window.append(EditMetadataWindow('valexl','tag'))
#    window.append(EditFilesWindow('/tmp/tmp'))
#    window.append(BrowseFilesWindow(path_to_repo='/tmp/tmp',user_repo='valex'))
#    window.append( BrowseMetadataWindow(user_name='valex',type_metadata='tag'))

    window .append(EditFilesWindow('/tmp/tmp'))
#    window.append(EditEntityWindow('/tmp/tmp',user_repo,SystemInfo.entity_file_type))
    
    

    for win in window:
        win.show()
        #print(win.__splitFileByRepo('/tmp/tmp2/tmpfile'))
        
    sys.exit(app.exec_())


    