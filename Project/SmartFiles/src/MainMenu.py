'''
Created on 03.06.2010

@author: valexl
'''
import sys
import os

from PyQt4 import QtGui,QtCore,QtSql

from Ui_MainWindow import Ui_MainWindow
from RepoManager.SystemInfo import SystemInfo
from RepoManager.User import User
from RepoManager.InstallUser import InstallUser
from EntityManager.Field import Field
from EntityManager.Tag import Tag
from EntityManager.Entity import Entity
from EntityManager.EntityManager import EntityManager
from RepoManager.RepoManager import RepoManager
from ProcessingRequest.ProcessingRequest import ProcessingRequest,\
    cleareExtraSpace

from EditWindow import EditEntityWindow,EditUserWindow,BrowseFilesWindow,BrowseMetadataWindow,EditMetadataWindow
from NeuralNet.NeuralNetwork import NeuralNetwork
import pickle
import subprocess
SQLRequest = "SELECT entity.* FROM entity"
class SmartFilesMainWindow(QtGui.QMainWindow,Ui_MainWindow):
    '''
    главное окно программы
    '''
    
    def __init__(self,user_connect,parent = None):
 
        super(SmartFilesMainWindow,self).__init__(parent)
        self.setupUi(self)
        
#        label = QtGui.
#        self._scaning_tables = QtGui.QLineEdit(self)
        
        
        self._user_repo=user_connect
        self._path_to_repo = None
        self._repo_manager = None
        self._db = None
        self._string_request = SQLRequest
        self._model = QtSql.QSqlQueryModel()
        self._is_open_repo = False
        
        self.browse_window =None
        self._select_list_tags=[]
        
        self.info_window = QtGui.QMessageBox()
        #для работы с хранилищем
        
        self.connect(self.action_open_repo,QtCore.SIGNAL("triggered()"),self.__openRepository)
        self.connect(self.action_delete_repo, QtCore.SIGNAL("triggered()"),self.__deleteRepository)
        self.connect(self.action_create_repo,QtCore.SIGNAL("triggered()"),self.__createRepository)
        
        #для работы с пользователями хранилища
        
        #self.connect(self._menu.add_user,QtCore.SIGNAL("triggered()"),self.__createUser)
        self.connect(self.action_switch_user,QtCore.SIGNAL("triggered()"),self.__switchUser)
        self.connect(self.action_delete_user_from_repo,QtCore.SIGNAL("triggered()"),self.__deleteUser)
        self.connect(self.action_update_user,QtCore.SIGNAL("triggered()"),self.__updateUser)
        self.connect(self.action_exit,QtCore.SIGNAL("triggered()"),self.__exitSmartFiles)
        
        #для работы с объектами хранилища
         
        self.connect(self.action_add_file,QtCore.SIGNAL("triggered()"),self.__addFile)
        self.connect(self.action_add_URL,QtCore.SIGNAL("triggered()"),self.__addURL)
        self.connect(self.action_mark_tag,QtCore.SIGNAL("triggered()"),self.__markTag)
        self.connect(self.action_mark_field,QtCore.SIGNAL("triggered()"),self.__markField)
        self.connect(self.action_change_entity,QtCore.SIGNAL("triggered()"),self.__updateEntity)
        self.connect(self.action_delete_entity,QtCore.SIGNAL("triggered()"),self.__deleteEntity)
        self.connect(self.tableView_entity,QtCore.SIGNAL('doubleClicked(QModelIndex)'),self.__selectEntity)
        self.connect(self.action_repo_files,QtCore.SIGNAL('triggered()'),self.__workingRepoFiles)
        #для работы с метаданными
        self.connect(self.action_setting_tags,QtCore.SIGNAL('triggered()'),self.__settingTag)
        self.connect(self.action_setting_fields,QtCore.SIGNAL('triggered()'),self.__settingField)
        #поиск
        self.connect(self.pushButton_search,QtCore.SIGNAL('clicked()'),self.__searchEntity)
        
        self.connect(self.radioButton_neural_net,QtCore.SIGNAL('clicked()'),self.__showInfo)
        #переключение таблиц                       
        self.connect(self.tabWidget,QtCore.SIGNAL('currentChanged (int)'),self.__switchTab)
       # self.tabWidget.setCurrentIndex(0)
        self._table = self.tableView_entity
        
        self._db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
    
    def __showInfo(self):
        if self.radioButton_neural_net.isChecked():
            self.info_window.setText('поиск по нейросети осуществляется простым набором тегов через пробел')
        else:
            self.info_window.setText('''поиск на языке запросов осуществляется через язык запросов.
Через теги и поля связываются логическими операциями (OR AND скобки "(...)" )
            ''')
        self.info_window.show()
    def __startFile(self,path):
        '''
           запуск объекта типа file
        '''
        if hasattr(os, 'startfile'): # Windows
            os.startfile(path)
        else:
            if sys.platform.startswith('darwin'): # Mac OS X
                command = 'open'
            else: # Linux
                command = 'xdg-open'
        #subprocess.call([command, path])
        subprocess.call([command, path])
    
    
    def __startURL(self,url):
        '''
            запуск объекта типа URL
        '''
        
        if hasattr(os, 'startfile'): # Windows
            #как то запустить url через exploer или другой експолоер
            pass
        else:
            if sys.platform.startswith('darwin'): # Mac OS X
                command = 'firefox' #какой то браузер Mac OS X
            else: # Linux
                command = 'konqueror'
        subprocess.call([command, url])
    
    def __selectEntity(self,index):
        print('попался')
        
        if self._is_open_repo:
            row=self._table.currentIndex().row()
            index = self._table.model().index(row,0)
            entity_id = self._table.model().data(index)
            index = self._table.model().index(row,4)
            file_path = self._table.model().data(index)
            if self.radioButton_neural_net.isChecked():        
                if len(self._select_list_tags)>0:
                    self._entity_manager.learningNeuralNet(entity_id, self._select_list_tags)
                else:
                    self._entity_manager.learningNeuralNet(entity_id)
            file_path = os.path.join(self._path_to_repo,file_path)
            print(file_path)
            
            self.__startFile(file_path)
            
        
        
    def closeEvent(self,event):
        '''
            переопределяем событие закрытия окна. сохранение нужной инфы.
        '''
        if self._is_open_repo:
            self._entity_manager.saveNeuralNet()
        
        
        
    
    def __switchTab(self,index):
        '''
            переключение вкладок для отображения сущностей
        '''
        
        if self._is_open_repo:
            if index==0:
                self._table = self.tableView_entity 
                self.__settingModel()
            elif index==1:
                self._table = self.treeView_entity_browse_tags
                self.__settingModel()
                pass
            else:
                pass
            
    def __connnectBD(self):
        '''
            подключение к БД с метаинформацией хранилщиа
        '''
        try:
            self._db.setDatabaseName(os.path.join(self._path_to_repo,SystemInfo.metadata_file_name))
            self._db.open()
            self.__settingModel()
        except Exception as error:
            print('проблемы при подключении к БД или ее настройки')
            print(error)
            
            
    def __settingModel(self):
        '''
            отображение состояние базы на таблице
        '''
        if self.tabWidget.currentIndex()==0:
            self._model.setQuery(self._string_request)
        elif self.tabWidget.currentIndex()==1:
            self._model.setQuery(self._string_request)
        elif self.tabWidget.currentIndex()==2:
            #self.treeView_entity_browse
            pass
        
        if (self._model.lastError().isValid()):
            print('eroro in model where connecting BD file')
        self._table.setModel(self._model)
        self._table.show()
        print('table is showing')
        
    
    def __openRepository(self):
        '''
            открывание хранилище
        '''
        try:
            print('__openRepository')
            self._path_to_repo = QtGui.QFileDialog.getExistingDirectory(self,'открыть хранилище','/')   
            print(self._path_to_repo)
            self._repo_manager = RepoManager.openRepository(self._path_to_repo)
            self._repo_manager.identificationUser(self._user_repo)
            self._entity_manager = self._repo_manager.getEntityManager() 
            
            
            self.__connnectBD()
            self._is_open_repo = True
        except RepoManager.ExceptionRepoIsNull as err:
            self.info_window.setText(''' не возможно открыть хранилище. оно еще не создано.
            ''')
            self.info_window.show()
            print('невозможно открыть хранилище')
            print(err)
        except RepoManager.ExceptionUserExist as err:
            self.info_window.setText('''Пользователь уже существует в данном хранилище
            ''')
            self.info_window.show()
            print(err)
        except RepoManager.ExceptionUserGuest as err:
            self.info_window.setText('''
            пользователь гость.
            происходит регестрация текущего пользователя в хранилище.
            ''')
            self.info_window.show()
#            print('пользователь гость')
            print(err)
#            print('автоматически регестрируется в хранилище')
            self._repo_manager.addUserRepo(self._user_repo)
            self._entity_manager = self._repo_manager.getEntityManager()
            self.__connnectBD()
        except Exception as err:
            self.info_window.setText(''' какие то не учтенные траблы    
            ''')
            self.info_window.show()
            print(err)
            
            
    def __deleteRepository(self):
        '''
            удаление хранилища (всех мета файлов и директорий)
        '''
        print('__deleteRepository')
        try:
            RepoManager.deleteRepository(self._path_to_repo)
            self._path_to_repo = None
            self.__disconnectBD()
            self._is_open_repo = False
        except RepoManager.ExceptionRepoIsNull as error:
            #print('не возможно удалить хранилище')
            self.info_window.show()
            self.info_window.setText('''Не возможно удалить хранилище
Нет открытых хранилищ.
            ''')
            
            #self.connect(self.info_window,QtCore.SIGNAL('closed()'))
            print(error)
        except Exception as error:
            print('удаление хранилища')
            print('какие то не учтеные траблы в RepoManager')
            self.info_window.show()
            self.info_window.setText('какие-то неучтенные траблы')
            print(error) 
        
    def __disconnectBD(self):
        '''
            отключение БД 
        '''
        print('deleting db')
        self._db.close()
        self._model.clear()
        self._model.reset()
    
   
    def __createRepository(self):
        '''
            создание нового хранилища
        '''
        print('__createRepository')
        try:
            self._path_to_repo = QtGui.QFileDialog.getExistingDirectory(self,'выбирете директорию хранилища', '/')
            self._user_repo.type = SystemInfo.user_type_admin
            self._repo_manager = RepoManager.initRepository(self._path_to_repo,self._user_repo)
            self._repo_manager.fillRepoFiles() # заполнение базы информацией о файлах хранилщиа.
            self._entity_manager = self._repo_manager.getEntityManager()
            
            #запись ифны о нейронной сети в директорию с метаданными хранилища
            
             
            
            
            self._is_open_repo = True
            self.__connnectBD()
            print(self._path_to_repo)
        except RepoManager.ExceptionRepoIsExist as error:
#            print('не удается создать хранилище.')
#            print(' Хранилище уже созданно')
            self.info_window.show()
            self.info_window.setText('''не удалось создать хранилщие.
Хранилище уже создано''')
            print(error)
        except Exception as error:
            print('создание хранилища')
#            print('какие то не учтеные траблы в RepoManager')
            self.info_window.setText('''какие то не учтенные траблы в RepoManager
            ''')
            self.info_window.show()
            print(error)

 
    def __switchUser(self):
        '''
            переключение пользователя. Посылается сигнал о переключение в окно StartingWindow
        '''
        self.emit(QtCore.SIGNAL('switchUser()'))
        
        
    def __deleteUser(self):
        '''
            подготовка к удалению пользователя
        '''
        try:
            self.edit_window = EditUserWindow('delete')
            self.edit_window.show()
            self.connect(self.edit_window,QtCore.SIGNAL("deleteUser(user_name)"),self.__deletingUser)
        except Exception as error:    
            print('__deleteUser')
            self.info_window.setText('''Проблемы при удалении пользователя
            ''')
            self.info_window.show()        
            print(error)
            
            
    def __deletingUser(self,user):
        '''
            удаление пользователя и всех связей с ним
        '''
        try:
            
            self._repo_manager.deleteUser(user)
            self.__settingModel()
        except RepoManager.ExceptionUserNotFound as error:    
            print('__deletingUser')
            self.info_window.setText('''Удаляемый пользователь не найден.
            ''')
            self.info_window.show()        
            print(error)        
        except Exception as error:    
            print('__deletingUser')
            self.info_window.setText('''неучтенные траблы в RepoManager
            ''')
            self.info_window.show()        
            print(error)
        
                    
    def __updateUser(self):
        '''
            подготовка к модификации пользователя
        '''
        try:
            
            self.edit_window = EditUserWindow('update',self._user_repo)
            self.edit_window.show()
            self.connect(self.edit_window,QtCore.SIGNAL("updateUser(user)"),self.__updatingUser)
        except RepoManager.ExceptionErrorPasswordUser as error:
            self.info_window.setText('''Не правильно введен пароль или пользователь
            ''')
            self.info_window.show()
            print(error)
        except Exception as error:
            self.info_window.setText('''Неучтенные траблы при обновлении пользователя в RepoManager
            ''')
            self.info_window.show()
            print('__updateUser')
            print(error)
        
        
    def __updatingUser(self,user):
        '''
            модификация пользователя
        '''
        try:
            self._repo_manager.updateUser(user)
            self.__settingModel()
            self.emit(QtCore.SIGNAL('updateUser(user)'),user)
        except RepoManager.ExceptionUserNotFound as error:    
            print('__updatingUser')
            self.info_window.setText('''Не найден пользователь
            ''')
            self.info_window.show()        
            print(error)
        except Exception as error:    
            print('__updatingUser')
            self.info_window.setText('''Не учтенные траблы в RepoManager
            ''')
            self.info_window.show()        
            print(error)    
        
        
    def __exitSmartFiles(self):
        '''
            завершение работы программы
        '''
        self.__disconnectBD()
        sys.exit()
    def __searchByNeuralNet(self):
        '''
            поиск с помощью нейросети
        '''
        if self.lineEdit_search.text()=="":
            self._string_request = SQLRequest # "SELECT * FROM entity"
            self._entity_manager.searchByNeuralNet()
        else:
            request = cleareExtraSpace(self.lineEdit_search.text())
            print('request after clearning extra spacing')
            self._select_list_tags = request.split(' ')  
            print('request afger spliting',self._select_list_tags)
            
            self._entity_manager.tmpPrintNeuralNet()
            self._entity_manager.searchByNeuralNet(self._select_list_tags)
            
            
            request = self._select_list_tags[0]
            index = 1
            while index < len(self._select_list_tags):
                request+= " OR " + self._select_list_tags[index] 
                index+=1
            self._string_request = ProcessingRequest.getSQLRequest(request,True)
        self.__settingModel()
        print(self._string_request)
        
        
    def __searchByQueryLanguage(self):
        '''
            поис с помощью языка запроса
        '''
        print('query languages finding')
        if self.lineEdit_search.text()=="":
            self._string_request = SQLRequest # "SELECT * FROM entity"
        else:
            self._string_request = ProcessingRequest.getSQLRequest(self.lineEdit_search.text())
        print('SQL SEARCH',self._string_request)
        self.__settingModel()
        
    def __searchEntity(self):
        '''
            начала поиск объекта
        '''
        if self.radioButton_neural_net.isChecked():
            self.__searchByNeuralNet()
        else:
            self.__searchByQueryLanguage()
    
    
    
    def __addFile(self):
        '''
            добавление файла в хранилщие
        '''
        try:
            if self._is_open_repo:
                #entity = EntityManager.createEntity()
                self.edit_window = EditEntityWindow(path_to_repo = self._path_to_repo,user_repo= self._user_repo,object_type = SystemInfo.entity_file_type)
                self.edit_window.show()
                self.connect(self.edit_window,QtCore.SIGNAL('createEntity(list_entityes)'),self.__addingEntity)
                #отлавливание сигнала на добавление нового файла       
            else:
                self.info_window.setText(''' Для начало откроем хранилище
            ''')
                self.info_window.show()
                     
        except Exception as error:
            self.info_window.setText(''' какието траблы с qt
            ''')
            self.info_window.show()
            print('__addURL')
            print(error)
    
    def __indexingFile(self,entity):
        '''
            индексирование файла(отправляется на запись в БД и удаляется из таблицы не проиндексированных файлов)
        '''
        #entity = EntityManager.createEntity(entity_type=SystemInfo.entity_file_type, user_name=self._user_repo.name, file_path=file_path)
#        self.emit('sendEntity(entity)',entity)
        self.edit_window = EditEntityWindow(path_to_repo=self._path_to_repo,user_repo=self._user_repo,
                                            object_type=SystemInfo.entity_file_type,entity=entity)
        self.edit_window.show()
        self.connect(self.edit_window,QtCore.SIGNAL('createEntity(list_entityes)'),self.__addingEntity)
        

    def __addURL(self):
        '''
            добавление URL ссылки в хранилище
        '''
        try:
            if self._is_open_repo:
                #entity = EntityManager.createEntity()
                self.edit_window = EditEntityWindow(path_to_repo=self._path_to_repo,user_repo=self._user_repo,object_type=SystemInfo.entity_link_type)
                self.edit_window.show()                      
                self.connect(self.edit_window,QtCore.SIGNAL("createEntity(list_entityes)"),self.__addingEntity)
                #отлавливание сигнала на добавление нового файла       
            else:
                self.info_window.setText('''Для начало нужно отрыть хранилище
            ''')
                self.info_window.show()     
        except Exception as error:
            self.info_window.setText('''Траблы с qt
            ''')
            self.info_window.show()
            print('__addURL')
            print(error)

    
    def __addingEntity(self,list_entity):
        '''
                добавление объекта Entity в базу данных
        '''
        try:
            for entity in list_entity:
                print('adding entity-',entity)
                entity.id = self._entity_manager.saveEntity(entity)
                
                if not entity.file_path == None:
                    print('file_info.file_path=',entity.file_path)
                    self._repo_manager.deleteFilesInfo(entity.file_path)
        
                self.__settingModel()
                if not self.browse_window ==None:
                    self.browse_window.refresh()
        except EntityManager.ExceptionNotFoundFileBD as error:
            self.info_window.setText('''Не найден файл с метаданными
            ''')
            self.info_window.show()
            print('__addingEntity проблемы:')
            print(error)
        except EntityManager.ExceptionEntityIsExist as error:
            self.info_window.setText('''добавляемая сущность уже существует
            ''')
            self.info_window.show()
            print(error)
        except Exception as error:
            self.info_window.setText('''Какие то не учтенные траблы в EntityManager
            ''')
            self.info_window.show()
            print('__addingEntity')
            print(error)
            
            
    def __workingRepoFiles(self):
        '''
            отображение не проиндексированных файлов (файлов, которые не присвоил себе ни один пользователь)
        '''
        try:
            if self._is_open_repo:
                self.browse_window = BrowseFilesWindow(path_to_repo=self._path_to_repo,user_repo=self._user_repo)
                self.browse_window.show()
                self.connect(self.browse_window,QtCore.SIGNAL("indexingFile(entity)"),self.__indexingFile)
                self.connect(self.browse_window,QtCore.SIGNAL('deleteFileInfo(file_path)'),self._repo_manager.deleteFilesInfo)
                self.connect(self.browse_window,QtCore.SIGNAL('saveFileInfo(file_path)'),self._repo_manager.addFileInfo)
            else:
                self.info_window.setText('''открой что ли хранилище
            ''')
                self.info_window.show()
                print('открой что ли хранилище')
                #raise Exception('открой что ли хранилище') 
        except Exception as error:
            print('__workingRepoFiles')
            self.info_window.setText('''какие то трабы в qt
            ''')
            self.info_window.show()
            print(error)


    def __markTag(self):
        '''
            подкотовка для работы с тегами 
        '''
        
        if not (self._table.model() == None):
            row=self._table.currentIndex().row()
            index = self._table.model().index(row,0)
            entity_id = self._table.model().data(index)
            if not entity_id == None:
                try:

                    self.edit_window = EditMetadataWindow(entity_id=entity_id,user_repo=self._user_repo, type_metadata='tag') 
                    self.edit_window.show()
                    self.connect(self.edit_window,QtCore.SIGNAL("mark(entity_id,metadata_obj)"),self.__markingTag)
                except Exception as error:
                    print('__markTag')
                    print(error)
    
            else:
                #print('А кто будет Entity выбирать для добавления тега?')
                self.info_window.setText('''А кто будет Entity выбирать?
            ''')
                self.info_window.show()
        else:
            self.info_window.setText('''может откроешь хранилище?
            ''')
            self.info_window.show()
            

   
        
    def __markingTag(self,entity_id,marking_tag):
        '''
            пометка сущности тегом
        '''
        print('marking tag')
        try:
            entity = self._entity_manager.loadEntityObj(entity_id)
            self._entity_manager.markTag(entity, marking_tag)  
#            self.browse_window.refresh()
        except EntityManager.ExceptionNotFoundFileBD as error:
            self.info_window.setText('''не найден файл с метаданными
            ''')
            self.info_window.show()
            print(error)
        except Exception as error:
            self.info_window.setText('''какие-то неучтенные траблы в EntityManager
            ''')
            self.info_window.show()
            print(error)


    def __markField(self):
        '''
            поготовка работы с полями
        '''
        if not (self._table.model()==None):
            row=self._table.currentIndex().row()
            index = self._table.model().index(row,0)
            entity_id = self._table.model().data(index)
            if not entity_id==None:
                try:
                    self.edit_window = EditMetadataWindow(entity_id=entity_id,user_repo=self._user_repo, type_metadata='field') 
                    self.edit_window.show()
                    self.connect(self.edit_window,QtCore.SIGNAL("mark(entity_id,metadata_obj)"),self.__markingField)
                except Exception as error:
                    print('__markTag')
            else:
                self.info_window.setText('''а кто будет entity выбирать?
            ''')
                self.info_window.show()
                #print('кто будет Entity выбирать для добавления поля')
        else:
            self.info_window.setText('''может хранилище откроем?
            ''')
            self.info_window.show()
            #print('может хранилище откроем?')
            
    def __markingField(self,entity_id,marking_field):
        '''
            пометка полем сущности
        '''     
        print('get signal')
        try:
            entity = self._entity_manager.loadEntityObj(entity_id)
            self._entity_manager.addField(entity,marking_field)
            #self.browse_window.refresh()
        except EntityManager.ExceptionNotFoundFileBD as error:
            self.info_window.setText('''не найден файл с метаданными
            ''')
            self.info_window.show()
            print(error)
        except Exception as error:
            self.info_window.setText('''какие-то неучтенные траблы с entity_manager
            ''')
            self.info_window.show()
            print(error)
    
    
    def __updateEntity(self):
        '''
            подготовка к модификации сущности
        '''
        
        try:
            if self._is_open_repo:
                row=self._table.currentIndex().row()
                index = self._table.model().index(row,0)
                entity_id = self._table.model().data(index)
                if not entity_id==None:
                    #index = self._table.model().index(row,3) # тип обеъкта
                    #замечание. еще необходима передавать дату создания, так как ее модификация не нужна.
                    #object_type=self._table.model().data(index)
                    
                    entity = self._entity_manager.loadEntityObj(entity_id)
                    self.edit_window = EditEntityWindow(path_to_repo = self._path_to_repo,user_repo=self._user_repo,object_type=entity.object_type,entity=entity)
                    self.edit_window.show()
                    self.connect(self.edit_window,QtCore.SIGNAL("updateEntity(list_entityes)"),self.__updatingEntity)
                else:
                    self.info_window.setText('''Товарищ, а какой собственно объект изменять?
            ''')
                    self.info_window.show()
                
            else:
                self.info_window.setText('''не забываем отрыть хранилище
            ''')
                self.info_window.show()
        except Exception as error:
            self.info_window.setText('''какие то неучтенные траблы в entity_manager 
            ''')
            self.info_window.show()
            print('__updateEntity')
            print(error)
    
    
    def __updatingEntity(self,list_entityes):
        '''
            модификация сущности
        '''
        #if self._is_open_repo:
        try:
            old_entity,new_entity = list_entityes
            #поиск удаленных тегов
            for old_tag in old_entity.list_tags:
                is_delete=True
                for new_tag in new_entity.list_tags:
                    if old_tag.name == new_tag.name:
                        is_delete=False
                        break
                if is_delete:
                    self._entity_manager.releaseEntityFromTag(new_entity, old_tag)
            #поиск удаленных полей
            for old_field in old_entity.list_fields:
                is_delete=True
                for new_field in new_entity.list_fields:
                    if old_field.name == new_field.name:
                        is_delete=False
                        break
                if is_delete:
                    self._entity_manager.releaseEntityFromTag(new_entity, old_tag)
                    
                    
            self._entity_manager.saveEntity(new_entity)
            self.__settingModel()
        except EntityManager.ExceptionNotFoundFileBD as error:
            self.info_window.setText('''не найден файл с метаданным
            ''')
            self.info_window.show()
            print('__updatingEntity проблемы:')
            print(error)
        except Exception as error:
            self.info_window.setText('''какие то неучтенные траблы с EntityManager
            ''')
            self.info_window.show()
            print('__updatingEntity')
            print(error)
            
        self.disconnect(self.edit_window,QtCore.SIGNAL('"updateEntity(entity)'),self.__updatingEntity)
        
   
    def __deleteEntity(self):
        '''
            подготовка к удалению объекта сущности
        '''
        if self._is_open_repo:
#            print('__deleteEntity')
            row=self._table.currentIndex().row()
            index = self._table.model().index(row,0)
            id = self._table.model().data(index)
            if not id == None: #если объект выбран
                #print(id)
                self.__deletingEntity(id)
            else:
                self.info_window.setText('''не забываем выбирать объект хранилища
            ''')
                self.info_window.show()
                print('не забываем выбирать объект удаления')
        else:
            self.info_window.setText('''а хо хо не ху ху? открывай давай хранилище!
            ''')
            self.info_window.show()
            print('а хо хо не ху ху? открывай давай хранилщие')
            
            
        
    def __deletingEntity(self,entity_id):
        '''
            удаление сущности
        '''
        try:
            entity = self._entity_manager.loadEntityObj(entity_id)
            if entity.object_type == SystemInfo.entity_file_type:
                #добавление только что удаленный обеъкт в таблицу непроиндексированных объектов
                self._repo_manager.addFileInfo(entity.file_path)
            self._entity_manager.deleteEntity(entity)
            self.__settingModel()
        except EntityManager.ExceptionNotFoundFileBD as error:
            self.info_window.setText('''не найден файл с метаданными
            ''')
            self.info_window.show()
            print('__deletingEntity')
            print(error)
        except RepoManager.ExceptionRepoIsNull as error:
            print('__deletingEntity')
            self.info_window.setText('''хранилище не существует
            ''')
            self.info_window.show()
            print(error) 
        except Exception as error:
            self.info_window.setText('''какие то неучтенные траблы в RepoManager или EntityManager
            ''')
            self.info_window.show()
            print('__deletingEntity')
#       

    def __complexSearch(self):
        '''
            какой нибудь крутой поиск. типа в конкретной директориии.
        '''
        pass
        
        
    def __settingTag(self):
        '''
            управление тегами
        '''
        if self._is_open_repo:
            self.browse_window = BrowseMetadataWindow(self._user_repo, 'tag')
            self.browse_window.show()
            self.connect(self.browse_window,QtCore.SIGNAL('deleteTag(tag)'),self._entity_manager.deleteTag)
        else:
            self.info_window.setText('''Хранилище открой..
            ''')
            self.info_window.show()
            
        
        
    def __settingField(self):
        '''
            управление полями
        '''
        if self._is_open_repo:
            self.browse_window = BrowseMetadataWindow(self._user_repo, 'field')
            self.browse_window.show()
            self.connect(self.browse_window,QtCore.SIGNAL('deleteField(field)'),self._entity_manager.deleteField)
        else:
            self.info_window.setText('''нужно открыть хранилище
            ''')
            self.info_window.show()
            
        
        
        
        
        
if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    user_repo = User('alexl', 1)
    myclass = SmartFilesMainWindow(user_repo)
#    myclass = QtGui.QMessageBox()
    

    myclass.show()
    app.exec_()
#    print(os.path.split('tmp/tmp/aastelper.completions'))