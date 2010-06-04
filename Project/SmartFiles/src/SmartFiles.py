'''
Created on 17.05.2010

@author: valexl
'''
import sys
import os
from PyQt4 import QtGui,QtCore,QtSql

#import NeuralNetwork.NeuralNetwork


#from NeuralNetwork import NeuralNetwork
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

#import MainForm


height = 500
width = 1000
SQLRequest = "SELECT entity.* FROM entity "
#SQLRequest = "SELECT id,title,user_name,object_type,file_path FROM entity"
class MainMenu(QtGui.QMainWindow):
#class MainMenu(QtGui.QWidget):
    def __init__(self):
        '''
            создание меню и панели инструментов
        '''
        QtGui.QMainWindow.__init__(self)
       
       
        #работа с хранилщием
        self.open_repo = QtGui.QAction('Открыть',self)  
        self.create_repo = QtGui.QAction("Создать",self)
        self.delete_repo = QtGui.QAction("Удалить",self)
        #работа с пользователем
        self.add_user = QtGui.QAction("Добавить",self)
        self.delete_user = QtGui.QAction("Удалить",self)
        self.update_user = QtGui.QAction('Изменить',self)
        self.switch_user = QtGui.QAction('Переключить',self)
        #выход
        self.quit_programm = QtGui.QAction('Выход',self)
        
    
        #работа с сущностью
        self.createEntity = QtGui.QAction("Файл", self)
        self.create_URL = QtGui.QAction("URL ссылку",self)
        self.mark_tag = QtGui.QAction("Тегом",self)
        self.mark_field = QtGui.QAction("Полем",self)
        self.release_tag = QtGui.QAction("Тега",self)
        self.release_field = QtGui.QAction("Поля",self)
        
        self.save_entity = QtGui.QAction("Изменить", self)   
        #self.search_entity = QtGui.QAction('Поиск',self)
        self.delete_entity = QtGui.QAction("Удалить",self)
        
        #панель инструментов
        toolbar = self.addToolBar('Tools')
        toolbar.addAction(self.create_repo)
        toolbar.addAction(self.open_repo)
        toolbar.addAction(self.quit_programm)
        
        #toolbar.addAction(self.search_entity)
        
        
        #меню 
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu('&Файл')
        #создание/октрытие хранилщиа
        repo_menu = file_menu.addMenu("Хранилище")
        repo_menu.addAction(self.create_repo)
        repo_menu.addAction(self.open_repo)
        repo_menu.addAction(self.delete_repo)
        #работа с пользователями хранилища
        users_menu = file_menu.addMenu("Пользователь")
        users_menu.addAction(self.add_user)
        users_menu.addAction(self.switch_user)
        users_menu.addAction(self.update_user)
        users_menu.addAction(self.delete_user)
        #выход из программы
        file_menu.addAction(self.quit_programm)
        
        object_menu = menubar.addMenu('&Объект')
        create_menu = object_menu.addMenu("Добавить")
        create_menu.addAction(self.createEntity)
        create_menu.addAction(self.create_URL)
        
        mark_menu = object_menu.addMenu("Пометить")
        mark_menu.addAction(self.mark_tag)
        mark_menu.addAction(self.mark_field)
        
        release_metadata_menu = object_menu.addMenu("Освободить От ")
        release_metadata_menu.addAction(self.release_tag)
        release_metadata_menu.addAction(self.release_field)
        
        metadatat_menu = menubar.addMenu('Метаданные')
        
        object_menu.addAction(self.save_entity)
        object_menu.addAction(self.delete_entity)
      #  object_menu.addAction(self.search_entity)

        
class StartWindow(QtGui.QWidget):
    def __init__(self,parent=None):
        try:
            QtGui.QWidget.__init__(self,parent)
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
            
            self.setLayout(vbox_layout)
            InstallUser.initHomeDir()
        except InstallUser.ExceptionNoUsers as err:
            print(err)
            print('добавьте пользователя для работы в системе')
        
    def __startSF(self):
        '''
            Идентификация пользователя. В случае успеха запуск программы.
        '''        
        try:
            user_repo = InstallUser.identificationUser(self._edit_login.text(), self._edit_password.text())
            self.__starting(user_repo)
            
        except RepoManager.ExceptionUserNotFound as err:
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
        '''
            Сбор информации необходимой для создание нового пользователя.   
        '''
        try:
            self.edit_window = EditUserWindow('create')
            self.edit_window.show()
            self.connect(self.edit_window,QtCore.SIGNAL("createUser(user)"),self.__saveUser)
        except Exception as err:
            print(err)
        
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
        
 
class MainWindow(QtGui.QWidget):
    '''
        главное окно программы
    '''
    def __init__(self,user_connect,parent = None):
        
        
        QtGui.QWidget.__init__(self,parent)
         
        self._user_repo=user_connect
        self._path_to_repo = None
        self._repo_manager = None
        self._db = None
        self._string_request = SQLRequest
        
        self.setWindowTitle('SmartFiles')
                
        vbox_layout = QtGui.QVBoxLayout()
        
        
        self._menu = MainMenu()
        #для работы с хранилищем
        self.connect(self._menu.open_repo,QtCore.SIGNAL("triggered()"),self.__openRepository)
        self.connect(self._menu.delete_repo, QtCore.SIGNAL("triggered()"),self.__deleteRepository)
        self.connect(self._menu.create_repo,QtCore.SIGNAL("triggered()"),self.__createRepository)
        self.connect(self._menu.add_user,QtCore.SIGNAL("triggered()"),self.__createUser)
        self.connect(self._menu.switch_user,QtCore.SIGNAL("triggered()"),self.__switchUser)
        self.connect(self._menu.delete_user,QtCore.SIGNAL("triggered()"),self.__deleteUser)
        self.connect(self._menu.update_user,QtCore.SIGNAL("triggered()"),self.__updateUser)
        self.connect(self._menu.quit_programm,QtCore.SIGNAL("triggered()"),self.__exitSmartFiles)
        #для работы с объектами хранилища 
        self.connect(self._menu.createEntity,QtCore.SIGNAL("triggered()"),self.__addFile)
        self.connect(self._menu.create_URL,QtCore.SIGNAL("triggered()"),self.__addURL)
        
        self.connect(self._menu.mark_tag,QtCore.SIGNAL("triggered()"),self.__workWithTag)
        self.connect(self._menu.mark_field,QtCore.SIGNAL("triggered()"),self.__workWithField)
        self.connect(self._menu.release_tag,QtCore.SIGNAL('triggered()'),self.__releaseTag)
        self.connect(self._menu.release_field,QtCore.SIGNAL('triggered()'),self.__releaseField)
        
        self.connect(self._menu.save_entity,QtCore.SIGNAL("triggered()"),self.__updateEntity)
        self.connect(self._menu.delete_entity,QtCore.SIGNAL("triggered()"),self.__deleteEntity)
     #   self.connect(self._menu.search_entity,QtCore.SIGNAL("triggered()"),self.__complexSearchEntity)
        
        
        vbox_layout.addWidget(self._menu)
#Для проверки базы
        #добавление и настройка виджетов для строки поиска
        hbox_layout = QtGui.QHBoxLayout()
        label_search = QtGui.QLabel('SQL запрос     ',self)
        self._searchSQL_edit_text = QtGui.QLineEdit()
        self._button_searchSQL = QtGui.QPushButton('Проверить таблицы',self)
        self.connect(self._button_searchSQL,QtCore.SIGNAL('clicked()'),self.__searchEntityBySQL)
        
        hbox_layout.addWidget(label_search)
        hbox_layout.addWidget(self._searchSQL_edit_text)
        hbox_layout.addWidget(self._button_searchSQL)
        vbox_layout.addLayout(hbox_layout)
#Для проверки базы
        
        hbox_layout = QtGui.QHBoxLayout()
        label_search = QtGui.QLabel('Строка поиска',self)
        self._search_edit_text = QtGui.QLineEdit()
        self._button_search = QtGui.QPushButton('Найти',self)
        self.connect(self._button_search,QtCore.SIGNAL('clicked()'),self.__searchEntity)
        
        hbox_layout.addWidget(label_search)
        hbox_layout.addWidget(self._search_edit_text)
        hbox_layout.addWidget(self._button_search)
        vbox_layout.addLayout(hbox_layout)
                         
        #добавление таблицы для отображение состояние базы
        self._table = QtGui.QTableView(self)
      #  self._table = QtGui.QListView(self)
        self._model = QtSql.QSqlQueryModel()
       
   
        vbox_layout.addWidget(self._table)
        
        
        
        #строка состояние о текущем пользователе
        label_info = QtGui.QLabel('текущий пользователь --- ' + self._user_repo.name,self)
        vbox_layout.addWidget(label_info)
         
        #расположение всех виджетов на главном окне 
        self.setLayout(vbox_layout) 
        

        
    def __switchUser(self):
        self.emit(QtCore.SIGNAL('switchUser()'))
            
    def __searchEntity(self):
        try:
            if not self._search_edit_text.text() =='':
                self._string_request = ProcessingRequest.getSQLRequest(self._search_edit_text.text())
                print(self._string_request)
            else:
                self._string_request = SQLRequest    
            self.__settingModel()
        except Exception as error:
            print('__searchEntityBySQL')
            print(error)
    
    
    def __searchEntityBySQL(self):
        try:
            if self._searchSQL_edit_text.text() =="":
                self._string_request = SQLRequest # "SELECT * FROM entity"
            else:
                self._string_request = self._searchSQL_edit_text.text()
            print('SQL SEARCH',self._string_request)
            self.__settingModel()
        except Exception as error:
            print('__searchEntityBySQL')
            print(error)
    
        
    def __exitSmartFiles(self):
        '''
            завершение работы программы
        '''
        self.__disconnectBD()
        sys.exit()
        
            
    def __openRepository(self):
        '''
            открывание хранилище
        '''
        try:
            print('__openRepository')
            self._path_to_repo = QtGui.QFileDialog.getExistingDirectory(self,'OpenDir', '/tmp/tmp')   
            print(self._path_to_repo)
            self._repo_manager = RepoManager.openRepository(self._path_to_repo)
            self._repo_manager.identificationUser(self._user_repo)
            self._entity_manager = self._repo_manager.getEntityManager()
            self.__connnectBD()
        except RepoManager.ExceptionRepoIsNull as err:
            print('невозможно открыть хранилище')
            print(err)
        except RepoManager.ExceptionUserGuest as err:
            print('пользователь гость')
            #print(err)
            print('автоматически регестрируется в хранилище')
            self._repo_manager.addUserRepo(self._user_repo)
            self._entity_manager = self._repo_manager.getEntityManager()
            self.__connnectBD()
            
#        except Exception as error:
#            print('какие то не учтеные траблы в RepoManager')
#            print(error) 
        
        
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
        
        
    def __connnectBD(self):
        '''
            подключение к БД с метаинформацией хранилщиа
        '''
        try:
            self._db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
            self._db.setDatabaseName(os.path.join(self._path_to_repo,SystemInfo.metadata_file_name))
            self._db.open()
            self.__settingModel()
        except Exception as error:
            print('проблемы при подключении к БД или ее настройки')
            print(error)
        
    def __deleteRepository(self):
        '''
            удаление хранилища (всех мета файлов и директорий)
        '''
        print('__deleteRepository')
        try:
            RepoManager.deleteRepository(self._path_to_repo)
            self._path_to_repo = None
            self.__disconnectBD()
            
        except RepoManager.ExceptionRepoIsNull as error:
            print('не возможно удалить хранилище')
            print(error)
        except Exception as error:
            print('удаление хранилища')
            print('какие то не учтеные траблы в RepoManager')
            print(error) 
        
   
        
    def __settingModel(self):
        '''
            отображение состояние базы на таблице
        '''
        self._model.setQuery(self._string_request)
        if (self._model.lastError().isValid()):
            print('eroro in model where connecting BD file')
        self._table.setModel(self._model)
        self._table.show()
        print('table is showing')
        
    def __disconnectBD(self):
        '''
            отключение БД 
        '''
        if not self._db == None:
            del(self._db)
            self._model.clear()
            self._model.reset()
        
    def __addFile(self):
            '''
                добавление файла в хранилщие
            '''
        
#        try:
            self.browse_window = BrowseFilesWindow(path_to_repo=self._path_to_repo,user_name=self._user_repo)
            self.browse_window.show()
            self.connect(self.browse_window,QtCore.SIGNAL("indexingFile(file_path)"),self.__indexingFile)
            self.connect(self.browse_window,QtCore.SIGNAL('deleteFileInfo(file_path)'),self._repo_manager.deleteFilesInfo)
            self.connect(self.browse_window,QtCore.SIGNAL('saveFileInfo(file_path)'),self._repo_manager.addFileInfo)
#        except Exception as error:
#            print('__addFile')
#            print(error)
#        pass

    def __indexingFile(self,file_path):
        '''
            индексирование файла(отправляется на запись в БД и удаляется из таблицы не проиндексированных файлов)
        '''
        #entity = EntityManager.createEntity(entity_type=SystemInfo.entity_file_type, user_name=self._user_repo.name, file_path=file_path)
#        self.emit('sendEntity(entity)',entity)
        self.edit_window = EditEntityWindow(self._path_to_repo,self._user_repo.name,SystemInfo.entity_file_type,file_path=file_path,status='create')
        self.edit_window.show()
        self.connect(self.edit_window,QtCore.SIGNAL('createEntity(entity)'),self.__addingEntity)
        
#        self.connect(self.edit_window,QtCore.SIGNAL("createEntity(entity)"),self.__addingEntity)
#        self.connect(self.edit_window,QtCore.SIGNAL('saveFileInfo(file_path)'),self._repo_manager.addFileInfo)
#        self.connect(self.edit_window,QtCore.SIGNAL('deleteFileInfo(file_path)'),self._repo_manager.deleteFilesInfo)
    def __addURL(self):
        '''
            добавление URL ссылки в хранилище
        '''

        try:
            #entity = EntityManager.createEntity()
            self.edit_window = EditEntityWindow(self._path_to_repo,self._user_repo.name,SystemInfo.entity_link_type)
            self.edit_window.show()
            self.connect(self.edit_window,QtCore.SIGNAL("createEntity(entity)"),self.__addingEntity)
            #отлавливание сигнала на добавление нового файла
            
        except Exception as error:
            print('__addURL')
            print(error)

    
    def __addingEntity(self,entity):
        '''
                добавление объекта Entity в базу данных
        '''
       
        print('что то начал делать')
        try:
            print('_adding Entity')
            print('the fields attributes is - ', entity.getFieldAttributes())
            
            self._entity_manager.saveEntity(entity)
            if not entity.file_path == None:
                self._repo_manager.deleteFilesInfo(entity.file_path)
    #        self.__connnectBD()
            self.__settingModel()
            self.browse_window.refresh()
        except EntityManager.ExceptionNotFoundFileBD as error:
            print('__addingEntity проблемы:')
            print(error)
#        except Exception as error:
#            print('__addingEntity')
#            print(error)
    
     


    def __workWithTag(self):
        '''
            подкотовка для работы с тегами тегом
        '''
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
            print('не был выбран Entity для добавления')
        

   
        
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
        
        
    def __releaseTag(self):
        '''
            подготовка к особождению entity от тега
        '''
        row=self._table.currentIndex().row()
        index = self._table.model().index(row,0)
        entity_id = self._table.model().data(index)
        if not entity_id == None:
            try:
                self.browse_window = BrowseMetadataWindow(entity_id = entity_id, user_name= self._user_repo.name,type_metadata='tag',status='release')
                self.browse_window.show()
                self.connect(self.browse_window,QtCore.SIGNAL("releaseTag(entity_id,tag)"),self.__releasingTag)
            except Exception as error:
                print('__workWithTag')
                print(error)

        else:
            print('не был выбран Entity ')
        
        
    def __releasingTag(self,entity_id,releasing_tag):
        '''
            особождение entity от тега
        '''
        try:
            entity = self._entity_manager.loadEntityObj(entity_id)
            self._entity_manager.releaseEntityFromTag(entity,releasing_tag)
            self.browse_window.refresh()
        except EntityManager.ExceptionNotFoundFileBD as error:
            print('__releasingTag')
            print(error)
#        except Exception as error:
#            print(error)
        
        
    def __deletingTag(self,deleting_tag):
        '''
            удаление тега
        '''
        #print('__deletingTag')
        try:
            self._entity_manager.deleteTag(deleting_tag)
            self.browse_window.refresh()
        except EntityManager.ExceptionNotFoundFileBD as error:
            print('__deletingTag проблемы')
            print(error)
#        except Exception as error:
#            print(error)
   
            
    def __workWithField(self):
        '''
            поготовка работы с полями
        '''
        print('__workWithField')
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
            print('не был выбран Entity для добавления')
            
            
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
                
    def __releaseField(self):
        '''
            особождение entity от поля
        '''    
        row=self._table.currentIndex().row()
        index = self._table.model().index(row,0)
        entity_id = self._table.model().data(index)
        if not entity_id == None:
            try:
                self.browse_window = BrowseMetadataWindow(entity_id = entity_id, user_name= self._user_repo.name,type_metadata='field',status='release')
                self.browse_window.show()
                self.connect(self.browse_window,QtCore.SIGNAL("releaseField(entity_id,field)"),self.__releasingField)
            except Exception as error:
                print('__workWithTag')
                print(error)

        else:
            print('не был выбран Entity ')
        
        
    
    def __releasingField(self,entity_id,releasing_field):
        '''
            особождение entity от поля
        '''    
        entity = self._entity_manager.loadEntityObj(entity_id)
        self._entity_manager.releaseEntityFromField(entity, releasing_field)
        self.browse_window.refresh()    
        
    def __deletingField(self,deleting_field):
        '''
            удаление поля
        '''
        #print('__deletingField')
        try:
            self._entity_manager.deleteField(deleting_field)
            self.browse_window.refresh()
        except EntityManager.ExceptionNotFoundFileBD as error:
            print('__deletingTag проблемы')
            print(error)
        
    def __updateEntity(self):
        '''
            подготовка к модификации сущности
        '''
        try:
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
        except Exception as error:
            print('__updateEntity')
            print(error)
    
    
    def __updatingEntity(self,entity):
        '''
            модификация сущности
        '''
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
    
   
        
    def __deleteEntity(self):
        '''
            подготовка к удалению объекта сущности
        '''
        print('__deleteEntity')
        row=self._table.currentIndex().row()
        index = self._table.model().index(row,0)
        id = self._table.model().data(index)
        if not id == None: #если объект выбран
            #print(id)
            self.__deletingEntity(id)
        
            
        
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
#            print(error)
        
    def __createUser(self):
        '''
            создания нового пользователя
        '''
        try:
            self.edit_window = EditUserWindow('create')
            self.edit_window.show()
            self.connect(self.edit_window,QtCore.SIGNAL("createUser(user)"),self.__saveUser)
        except Exception as error:
            print('__createUser')
            print(' в базу системы добавлен не будет')                             
        
    def __saveUser(self,user):
        '''
            сохранение пользователя в хранилщие. 
            Если созданный пользователь не зарегестрирован в системе, то он автоматически регестрируется. 
        '''
        try:
            self.emit(QtCore.SIGNAL('createUser(user)'),user)
            self._repo_manager.addUserRepo(user)  #попытка добавить пользователя в текущее хранилище (если оно открыто)
            self.__settingModel()
        except RepoManager.ExceptionUserExist as error:
            print('__saveUser')
            print(error)
        except Exception as error:
            print('__saveUser')
            print(error)
            
        
    def __updateUser(self):
        '''
            подготовка к модификации пользователя
        '''
        try:
            
            self.edit_window = EditUserWindow('update',self._user_repo.name)
            self.edit_window.show()
            self.connect(self.edit_window,QtCore.SIGNAL("updateUser(user)"),self.__updatingUser)
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
        
        
if __name__ == '__main__':
    
    app = QtGui.QApplication(sys.argv)
    user = User('valexl',111,SystemInfo.user_type_admin)
    
    main = MainWindow(user)
    #main =  StartWindow()
    main.show()
    sys.exit(app.exec_())
    main._db.close()