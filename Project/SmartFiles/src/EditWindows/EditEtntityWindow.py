'''
Created on 07.06.2010

@author: valexl
'''
import os
import shutil
from PyQt4 import QtGui, QtCore
import datetime

from EntityManager.EntityManager import EntityManager
from RepoManager.SystemInfo import SystemInfo
from ProcessingRequest.ProcessingRequest import cleareExtraSpace,\
    cleareSpaceAboutOperator
from EntityManager.Field import Field
from EntityManager.Tag import Tag

#from ProcessingRequest.ProcessingRequest.ProcessingRequest import ExceptionInvalidRequestSyntaxis

class EditEntityWindow(QtGui.QDialog):
    '''
        окно редактирования сущности
    '''
    class ExceptionFileIsExist(Exception):
        pass
    
    def __init__(self,path_to_repo, user_repo,object_type,entity=None,parent=None):
        QtGui.QDialog.__init__(self,parent)
        self._object_type = object_type
        self._user_repo = user_repo
        self._path_to_repo = path_to_repo
        self._entity = entity
        
        self.info_window = QtGui.QMessageBox()
        
        self._new_files=[]
        
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
            button_files_browse = QtGui.QPushButton('...',self)
            
           
            vbox_layout.addWidget(label)
            hbox_layout = QtGui.QHBoxLayout()
            hbox_layout.addWidget(self._edit_path)
            hbox_layout.addWidget(button_files_browse)
            vbox_layout.addLayout(hbox_layout)
            
            if not self._entity == None:
                self._edit_path.setText(self._entity.file_path)
                self._edit_path.setDisabled(1)
            else:
                label = QtGui.QLabel('Путь к директории хранилища',self)
                self._edit_path_into_repo = QtGui.QLineEdit(self)
                self._edit_path_into_repo.setText(path_to_repo)
                button_repo_dir_browse = QtGui.QPushButton('...',self)
                self.connect(button_repo_dir_browse,QtCore.SIGNAL('clicked()'),self.__browseDir)
                vbox_layout.addWidget(label)
                hbox_layout = QtGui.QHBoxLayout()
                hbox_layout.addWidget(self._edit_path_into_repo)
                hbox_layout.addWidget(button_repo_dir_browse)
                vbox_layout.addLayout(hbox_layout)
                
            
            self.connect(button_files_browse,QtCore.SIGNAL('clicked()'),self.__browseFile)
            
        label = QtGui.QLabel('Теги',self)
        self._edit_tags = QtGui.QTextEdit(self)
        vbox_layout.addWidget(label)
        vbox_layout.addWidget(self._edit_tags)
        label = QtGui.QLabel('Поля',self)
        self._edit_fields = QtGui.QTextEdit(self)
        line = self._edit_fields.toPlainText()

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
        hbox_layout.addStretch()
        hbox_layout.addWidget(button_ok)
        hbox_layout.addWidget(button_cancel)
        vbox_layout.addLayout(hbox_layout)
        #помещение layout на форму
        
       
        
        self.setLayout(vbox_layout)
        
        self.connect(button_cancel,QtCore.SIGNAL('clicked()'),self.__canceled)
        self.connect(button_ok,QtCore.SIGNAL('clicked()'),self.__pressButtonOk)
        
        self.setGeometry(500,500,250,125)
        
        
    def __browseDir(self):
        '''
            сбор информации о директории копирования
        '''
        dir_path = QtGui.QFileDialog.getExistingDirectory(self,'Выберите директорию для сохранения',self._path_to_repo)
        if dir_path:
            self._edit_path_into_repo.setText(dir_path)
    
    def __browseFile(self):
        '''
            выбор файла для сохранения в хранилище
        '''
        file_dialog = QtGui.QFileDialog(self)
        file_dialog.setFileMode(QtGui.QFileDialog.ExistingFiles)

        
        list_files_names = file_dialog.getOpenFileNames(self,'выберити файлы для добавления',self._path_to_repo)
        if list_files_names:
            files = ''  
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

        if not self._edit_path.text()=='':
            if self._entity == None:
                    self.__create()
            else:
                if self._entity.id ==None:
                    self.__create()
                else:
                    self.__update()
        else:
            if self._object_type=='file':
                self.info_window.setText('''Не выбран файл для добавления''')
            else:
                self.info_window.setText('''не выбран URL для добавления''')
            self.info_window.show()
            
            
            
    def __getFields(self):
        '''
            возращает список объектов полей
        '''
        
        field_URL=''
        if self._object_type == SystemInfo.entity_link_type:
            if len(self._edit_path.text())>0:
                field_URL += ' URL=' + self._edit_path.text( )
            else:
                self.info_window.setText('''Добавляемый обеъкт типа URL.
необходимо заполнить поле URL.''')
                self.info_window.show()
                #raise Exception('Заполнить поле URL')
        list_fields=[]
        lines_field=[field_URL]
        lines_field += self._edit_fields.toPlainText().split('\n')
        for fields in lines_field:
            fields = cleareExtraSpace(fields)
#            print('fields',fields)
            if not fields=="":
                try:
                    fields = cleareSpaceAboutOperator(fields,'=')
                except IndexError as error:
                    print(error)
                    raise Exception()
                fields=fields.split(' ')
                #создавания объектов Field
                for field in fields:
                    field_name,field_value = field.split('=')
                    list_fields.append(Field(field_name,self._user_repo.name,field_value)) #тип поля по умолчанию стринг
#        print('list_fields',list_fields)
        return list_fields
    
    
    def __getTags(self):
        '''
            возращает список обеъктов тегов
        '''
        line_text = self._edit_tags.toPlainText().split('\n')
        list_tags=[]
        for line in line_text: 
            tags = cleareExtraSpace(line)
            if not tags=="":
                tags = tags.split(' ')
                for tag_name in tags:
                    list_tags.append(Tag(tag_name,self._user_repo.name))
#        for tag in list_tags: 
#            print(tag.name)
        return list_tags
    


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
            result_file_path +=  split_file_path[index] + os.sep 
            index+=1
        print(result_file_path)
        result_file_path = result_file_path[0:-1]
        return result_file_path
    
    def __isRepo(self,dir_path):
        '''
            проверка принадлежит ли выбранная директория хранилищу 
        '''
        list_dir_path = dir_path.split(os.path.sep)
        list_repo_path = self._path_to_repo.split(os.path.sep)
        index=0
        #print(dir_path)
        if len(list_dir_path)<len(list_repo_path):
            return False
        for repo_dir in list_repo_path:
            if not repo_dir==list_dir_path[index]:
                return False
            index+=1                
        return True
    
    def __create(self):
        '''
            создание нового объекта. Передает с сигналом только что созданный объект Entity
        '''
        
        #обработка полей
        try:
            list_fields = self.__getFields()
        #обработка тегов
            list_tags = self.__getTags()
        except Exception as error:
            self.info_window.setText(str('''Ошибка синтаксиса. "имя = значение" дложно быть в одной строке.
Возможно перепутали поле "теги" с полем "поля".
            '''))
            self.info_window.show()
            return  
        list_entityes = []      
        if self._object_type == SystemInfo.entity_link_type:
            list_entityes.append(EntityManager.createEntity(title=self._edit_title.text(),entity_type=self._object_type,user_name=self._user_repo.name,
                                            list_tags=list_tags,list_fields=list_fields,
                                            notes=self._edit_description.text())) #добавить дату создания
        else:
            dir_path = self._edit_path_into_repo.text()
            if self.__isRepo(dir_path):
                if not self._edit_path.text()=='':
                    files_names= self._edit_path.text()
                    list_files = files_names.split(';')
                    progress_window = QtGui.QProgressDialog(self)
                     
                    progress_window.setMinimum(0)
                    progress_window.setMaximum(99)
                    progress_window.show()
                    count_files = len(list_files)
                    d_progress = 99/count_files
                    progress = 0    
                
                    for file_path in list_files: # убираются лишнии пробелы в начале и конце строки. Если пользователь вводил файлы вручную
                        print(file_path
                              )
                        if not self.__isRepo(os.path.split(file_path)[0]):
                            file_path_copy = os.path.join(dir_path,os.path.split(file_path)[1])
                            if not os.path.exists(file_path_copy):
                                shutil.copyfile(file_path, file_path_copy)
                        else:
                            file_path_copy = file_path
                        file_path = self.__splitDirPath(file_path_copy)
                        entity = EntityManager.createEntity(title=self._edit_title.text(),
                                                   entity_type=self._object_type,
                                                   user_name=self._user_repo.name,
                                                   file_path = file_path,
                                                   list_tags=list_tags,
                                                   list_fields=list_fields,
                                                   notes=self._edit_description.text()) #добавить дату создания
             
                        list_entityes.append(entity)
                        progress+=d_progress
                        print(progress)
                        progress_window.setValue(int(progress))
                        QtGui.QApplication.processEvents()
#                    progress+=d_progress
#                    print(progress)
#                    progress_window.setValue(int(progress))
                    self.emit(QtCore.SIGNAL('createEntity(list_entityes)'),list_entityes)
                    progress_window.close()
                    self.close()
                else:
                    self.info_window.setText('''Не выбрано ни одного файла для копирвоания''')
                    self.info_window.show()
                #    print('епт.. файл выбери!')
            else:
                self.info_window.setText('''Выбранная директория не является хранилищем''')
                self.info_window.show()
            
            
            
            
            
#            
#
        
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
    

        
    
    
if __name__=='__main__':
    import sys
    from RepoManager.User import User
    app = QtGui.QApplication(sys.argv)
    user = User('valexl')
    window = EditEntityWindow('/tmp/tmp', user, SystemInfo.entity_file_type)
    window.show()
    app.exec_()
    
    