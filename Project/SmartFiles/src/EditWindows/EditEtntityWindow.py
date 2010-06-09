'''
Created on 07.06.2010

@author: valexl
'''
import os
import shutil
from PyQt4 import QtGui, QtCore


from EntityManager.EntityManager import EntityManager
from RepoManager.SystemInfo import SystemInfo
from ProcessingRequest.ProcessingRequest import cleareExtraSpace,\
    cleareSpaceAboutOperator
from EntityManager.Field import Field
from EntityManager.Tag import Tag
import datetime

class EditEntityWindow(QtGui.QDialog):
    '''
        окно редактирования сущности
    '''
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
        #self._edit_tags = QtGui.QLineEdit(self)
        self._edit_tags = QtGui.QTextEdit(self)
        #self._edit_tags.setGeometry(100,100,1000,100)
        vbox_layout.addWidget(label)
        vbox_layout.addWidget(self._edit_tags)
        
        label = QtGui.QLabel('Поля',self)
        #self._edit_fields = QtGui.QLineEdit(self)
        self._edit_fields = QtGui.QTextEdit(self)
         
     
        line = self._edit_fields.toPlainText()
        print(line.split('\n'))
        print(line)
        
        
        
        #cursor.movePosition
        
       # print(self._edit_fields.copy())
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
            if self._object_type=='file':
                self.info_window.setText('''хм.. наглец однако... ну ни чего.. файл выберешь, исправишься
            ''')
            else:
                self.info_window.setText('''хм.. наглец однако... ну ни чего.. URL выберешь, исправишься
            ''')
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
            print('fields',fields)
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
        print('list_fields',list_fields)
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
        for tag in list_tags: 
            print(tag.name)
        return list_tags
    
    
    def __splitFileByRepo(self,file_path):        
        '''
            отделение от пути файла путь к хранилищу. Если файл не принадлежит хранилищу, то копируется в корень хранилища.
        '''
        print('splitFileByRepo')
        part_dirs, file_name = os.path.split(file_path)
        part_dirs = part_dirs.split(os.path.sep)
        print('путь к файлу который будет копирваться',part_dirs)
        repo_path_dirs = self._path_to_repo.split(os.path.sep)
        print('путь хранилищу',repo_path_dirs)
        index = 0
        for dir_name in repo_path_dirs:
            if index >= len(part_dirs): #если копируемый файл не в хранилище, но путь к нему принадлежит хранилищу
                                        # то есть на пример. /tmp/tmp/tmp - хранилище, /tmp/tmp/file - файл добаляемый.
                
                self._new_files.append(file_name)
                #self.emit(QtCore.SIGNAL("indexingFile(entity)"),entity)
                shutil.copyfile(file_path,self._path_to_repo+os.path.sep + file_name)
                return file_name
            print('dir_name=',dir_name)
            print('part_dirs[',index,']=',part_dirs[index])
            if not dir_name == part_dirs[index]:
                    self._new_files.append(file_name)
                    shutil.copyfile(file_path, self._path_to_repo + os.path.sep + file_name)
                    return file_name                
            index+=1 
        result_path = os.path.sep
     
        for pos in range(index,len(part_dirs)):
            result_path+= part_dirs[pos] + os.path.sep
        print('result_path',result_path)
        result_path = result_path +  file_name
        result_path = result_path[1:]
        print('aaaaaaaaaaaaaaaaaaaaa-',result_path)
        return result_path 
    
    
    
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
            progress_window.setMaximum(99)
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
            progress_window.close()
            del(progress_window)
        print('the lenght outputting signal is -',len(list_entityes))
        
        
        self.emit(QtCore.SIGNAL("indexingFile(list_new_files)"),self._new_files)
    
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
    

        
    
    
if __name__=='__main__':
    import sys
    from RepoManager.User import User
    app = QtGui.QApplication(sys.argv)
    user = User('valexl')
    window = EditEntityWindow('/tmp/tmp', user, SystemInfo.entity_file_type)
    window.show()
    app.exec_()
    
    