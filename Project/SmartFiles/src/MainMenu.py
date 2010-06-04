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
from ProcessingRequest.ProcessingRequest import ProcessingRequest

from EditWindow import EditEntityWindow,EditUserWindow,BrowseFilesWindow,BrowseMetadataWindow
SQLRequest = "SELECT entity.* FROM entity "
class SmartFilesMainWindow(QtGui.QMainWindow,Ui_MainWindow):
    '''
    главное окно программы
    '''
    
    def __init__(self,user_connect,parent = None):
 
        super(SmartFilesMainWindow,self).__init__(parent)
        self.setupUi(self)
        
        self._user_repo=user_connect
        self._path_to_repo = None
        self._repo_manager = None
        self._db = None
        self._string_request = SQLRequest
        self._model = QtSql.QSqlQueryModel()
        self._is_open_repo = False
        
        self.browse_window =None
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
        self.connect(self.action_mark_tag,QtCore.SIGNAL("triggered()"),self.__workWithTag)
        self.connect(self.action_mark_field,QtCore.SIGNAL("triggered()"),self.__workWithField)
        self.connect(self.action_change_entity,QtCore.SIGNAL("triggered()"),self.__updateEntity)
        self.connect(self.action_delete_entity,QtCore.SIGNAL("triggered()"),self.__deleteEntity)
        self.connect(self.action_search,QtCore.SIGNAL('triggered()'),self.__complexSearch)
        self.connect(self.action_repo_files,QtCore.SIGNAL('triggered()'),self.__workingRepoFiles)
        #для работы с метаданными
        self.connect(self.action_metadata_setting,QtCore.SIGNAL('triggered()'),self.__settingMetadata)

        #переключение таблиц                       currentChanged 
        self.connect(self.tabWidget,QtCore.SIGNAL('currentChanged (int)'),self.__switchTab)
       # self.tabWidget.setCurrentIndex(0)
        self._table = self.tableView_entity
        
        self._db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        
    def __switchTab(self,index):
        print(index)
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
            print('невозможно открыть хранилище')
            print(err)
        except RepoManager.ExceptionUserExist as err:
            print(err)
        except RepoManager.ExceptionUserGuest as err:
            print('пользователь гость')
            print(err)
            print('автоматически регестрируется в хранилище')
            self._repo_manager.addUserRepo(self._user_repo)
            self._entity_manager = self._repo_manager.getEntityManager()
            self.__connnectBD()
            
            
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
            print('не возможно удалить хранилище')
            print(error)
        except Exception as error:
            print('удаление хранилища')
            print('какие то не учтеные траблы в RepoManager')
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
            self._path_to_repo = QtGui.QFileDialog.getExistingDirectory(self,'Откройте хранилище', '/')
            self._user_repo.type = SystemInfo.user_type_admin
            self._repo_manager = RepoManager.initRepository(self._path_to_repo,self._user_repo)
            self._repo_manager.fillRepoFiles() # заполнение базы информацией о файлах хранилщиа.
            self._entity_manager = self._repo_manager.getEntityManager()
            self._is_open_repo = True
            self.__connnectBD()
            print(self._path_to_repo)
        except RepoManager.ExceptionRepoIsExist as error:
            print('не удается создать хранилище.')
            print(' Хранилище уже созданно')
            print(error)
#        except Exception as error:
#            print('создание хранилища')
#            print('какие то не учтеные траблы в RepoManager')
#            print(error)

 
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
            print(error)        
#        except Exception as error:    
#            print('__deletingUser')        
#            print(error)
        
                    
    def __updateUser(self):
        '''
            подготовка к модификации пользователя
        '''
        try:
            
            self.edit_window = EditUserWindow('update',self._user_repo)
            self.edit_window.show()
            self.connect(self.edit_window,QtCore.SIGNAL("updateUser(user)"),self.__updatingUser)
        except RepoManager.ExceptionErrorPasswordUser as error:
            print('косарез')
            print(error)
        except Exception as error:
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
            print(error)
        except Exception as error:    
            print('__updatingUser')        
            print(error)    
        
        
    def __exitSmartFiles(self):
        '''
            завершение работы программы
        '''
        self.__disconnectBD()
        sys.exit()
        
        
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
                print('для начало откроем хранилщие')     
        except Exception as error:
            print('__addURL')
            print(error)
    
    def __indexingFile(self,file_path):
        '''
            индексирование файла(отправляется на запись в БД и удаляется из таблицы не проиндексированных файлов)
        '''
        #entity = EntityManager.createEntity(entity_type=SystemInfo.entity_file_type, user_name=self._user_repo.name, file_path=file_path)
#        self.emit('sendEntity(entity)',entity)
        self.edit_window = EditEntityWindow(self._path_to_repo,self._user_repo.name,SystemInfo.entity_file_type,file_path=file_path,status='create')
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
                print('для начало откроем хранилщие')     
        except Exception as error:
            print('__addURL')
            print(error)

    
    def __addingEntity(self,list_entity):
        '''
                добавление объекта Entity в базу данных
        '''
       
        print('что то начал делать')
        try:
            for entity in list_entity:
                print('adding entity-',entity)
                self._entity_manager.saveEntity(entity)
                if not entity.file_path == None:
                    self._repo_manager.deleteFilesInfo(entity.file_path)
        
                self.__settingModel()
                if not self.browse_window ==None:
                    self.browse_window.refresh()
        except EntityManager.ExceptionNotFoundFileBD as error:
            print('__addingEntity проблемы:')
            print(error)
        except EntityManager.ExceptionEntityIsExist as error:
            print(error)
#        except Exception as error:
#            print('__addingEntity')
#            print(error)
    def __workingRepoFiles(self):
        '''
            отображение не проиндексированных файлов (файлов, которые не присвоил себе ни один пользователь)
        '''
        try:
            if self._is_open_repo:
                self.browse_window = BrowseFilesWindow(path_to_repo=self._path_to_repo,user_name=self._user_repo)
                self.browse_window.show()
                self.connect(self.browse_window,QtCore.SIGNAL("indexingFile(file_path)"),self.__indexingFile)
                self.connect(self.browse_window,QtCore.SIGNAL('deleteFileInfo(file_path)'),self._repo_manager.deleteFilesInfo)
                self.connect(self.browse_window,QtCore.SIGNAL('saveFileInfo(file_path)'),self._repo_manager.addFileInfo)
            else:
                print('открой что ли хранилище')
                #raise Exception('открой что ли хранилище') 
        except Exception as error:
            print('__workingRepoFiles')
            print(error)



    def __workWithTag(self):
        '''
            подкотовка для работы с тегами 
        '''
        
        if not (self._table.model() == None):
            row=self._table.currentIndex().row()
            index = self._table.model().index(row,0)
            entity_id = self._table.model().data(index)
            if not entity_id == None:
                try:
                    
                    self.browse_window = BrowseMetadataWindow(entity_id = entity_id, user_name= self._user_repo.name)
                    self.browse_window.show()
                    self.connect(self.browse_window,QtCore.SIGNAL("markTag(entity_id,tag)"),self.__markingTag)
                    self.connect(self.browse_window,QtCore.SIGNAL('deleteTag(tag)'),self.__deletingTag)
                except Exception as error:
                    print('__workWithTag')
                    print(error)
    
            else:
                print('А кто будет Entity выбирать для добавления тега?')
        else:
            print('может откроешь хранилище?')

   
        
    def __markingTag(self,entity_id,marking_tag):
        '''
            пометка сущности тегом
        '''
        print('marking tag')
        try:
            entity = self._entity_manager.loadEntityObj(entity_id)
            self._entity_manager.markTag(entity, marking_tag)
            self.browse_window.refresh()
        except EntityManager.ExceptionNotFoundFileBD as error:
            print(error)
#        except Exception as error:
#            print(error)


    def __workWithField(self):
        '''
            поготовка работы с полями
        '''
        if not (self._table.model()==None):
            row=self._table.currentIndex().row()
            index = self._table.model().index(row,0)
            entity_id = self._table.model().data(index)
            if not entity_id==None:
                try:
                    self.browse_window = BrowseMetadataWindow(entity_id=entity_id,user_name=self._user_repo.name,type_metadata='field')
                    self.browse_window.show()
                    self.connect(self.browse_window,QtCore.SIGNAL('markField(entity_id,field)'),self.__markingField)
                    self.connect(self.browse_window,QtCore.SIGNAL('deleteField(field)'),self.__deletingField)
                except Exception as error:
                    print('__workWithTag')
            else:
                print('кто будет Entity выбирать для добавления поля')
        else:
            print('может хранилище откроем?')
            
    def __markingField(self,entity_id,marking_field):
        '''
            пометка полем сущности
        '''     
        print('get signal')
        try:
            entity = self._entity_manager.loadEntityObj(entity_id)
            self._entity_manager.addField(entity,marking_field)
            self.browse_window.refresh()
        except EntityManager.ExceptionNotFoundFileBD as error:
            print(error)
#        except Exception as error:
#            print(error)
    
    
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
                    index = self._table.model().index(row,3) # тип обеъкта
                    #замечание. еще необходима передавать дату создания, так как ее модификация не нужна.
                    object_type=self._table.model().data(index)
                    self.edit_window = EditEntityWindow(user_name=self._user_repo.name,path_repo=self._path_to_repo,object_type=object_type,id=entity_id,status='update')
                    self.edit_window.show()
                    self.connect(self.edit_window,QtCore.SIGNAL("updateEntity(entity)"),self.__updatingEntity)
            else:
                print('не забываем открывать хранилище!')
        except Exception as error:
            print('__updateEntity')
            print(error)
    
    
    def __updatingEntity(self,entity):
        '''
            модификация сущности
        '''
        if self._is_open_repo:
            try:
                self._entity_manager.saveEntity(entity)
                self.__settingModel()
            except EntityManager.ExceptionNotFoundFileBD as error:
                print('__updatingEntity проблемы:')
                print(error)
            except Exception as error:
                print('__updatingEntity')
                print(error)
            self.disconnect(self.edit_window,QtCore.SIGNAL('"updateEntity(entity)'),self.__updatingEntity)
        else:
            print('ёпт.. открой хранилище')
   
    def __deleteEntity(self):
        '''
            подготовка к удалению объекта сущности
        '''
        if self._is_open_repo:
            print('__deleteEntity')
            row=self._table.currentIndex().row()
            index = self._table.model().index(row,0)
            id = self._table.model().data(index)
            if not id == None: #если объект выбран
                #print(id)
                self.__deletingEntity(id)
        else:
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
            print('__deletingEntity')
            print(error)
        except RepoManager.ExceptionRepoIsNull as error:
            print('__deletingEntity')
            print(error) 
#        except Exception as error:
#            print('__deletingEntity')
#       

    def __complexSearch(self):
        pass
        print('поиск на языке запросов')
    def __settingMetadata(self):
        pass
        print('управление метаданными')
        
        
        
        
        
        
        
        
        
if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    user_repo = User('alexl', 1)
    myclass = SmartFilesMainWindow(user_repo)
#    myclass.mylabel.setText("Hello World!")
    myclass.show()
    app.exec_()