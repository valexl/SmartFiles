'''
Created on 03.06.2010

@author: valexl
'''
import sys
import os
import pickle
import subprocess
import shutil

from PyQt4 import QtGui,QtCore,QtSql


from RepoManager.SystemInfo import SystemInfo
from RepoManager.User import User

from EntityManager.EntityManager import EntityManager
from RepoManager.RepoManager import RepoManager
from ProcessingRequest.ProcessingRequest import ProcessingRequest,\
    cleareExtraSpace, cleareSpaceAboutOperator


from Ui_MainWindow import Ui_MainWindow
from EditWindows.EditEtntityWindow import EditEntityWindow
from EditWindows.EditUserWindow import EditUserWindow
from EditWindows.BrowseMetadataWindow import  BrowseMetadataWindow
from EditWindows.EditMetadataWindow import EditMetadataWindow
from EditWindows.EditFilesWindow import EditFilesWindow





class SmartFilesMainWindow(QtGui.QMainWindow,Ui_MainWindow):
    '''
        главное окно программы
    '''
    SQLRequest = "SELECT id,title,neuralnet_raiting,object_type,file_path FROM entity"
    def __init__(self,user_connect,parent = None):
        super(SmartFilesMainWindow,self).__init__(parent)
        self.setupUi(self)
        
        self._user_repo=user_connect       
        self._repo_manager = None
        self._db = None
        self._string_request = SmartFilesMainWindow.SQLRequest
        self._model = QtSql.QSqlQueryModel()
#        self._model_files_info = QtSql.QSqlQueryModel()
        self._model_metadata = QtSql.QSqlQueryModel()
        #self._model_metadata = MyModel
        self._is_open_repo = False
        self.browse_window =None
        self._select_list_tags=[]
        
        #информационное окно
        self.info_window = QtGui.QMessageBox()
        
# TOOLBAR
        
        icon = QtGui.QIcon('../Design/switch_users.png')
        action_delete_repo = self.toolBar.addAction(icon,'переключить пользователя')
        self.connect(action_delete_repo,QtCore.SIGNAL('triggered()'),self.__switchUser)
    
        self.toolBar.addSeparator()
        
        icon = QtGui.QIcon('../Design/create_repo.png')
        action_create_repo = self.toolBar.addAction(icon,'создать хранилище')
        self.connect(action_create_repo,QtCore.SIGNAL('triggered()'),self.__createRepository)
        
        icon = QtGui.QIcon('../Design/open_repo.png')
        action_open_repo = self.toolBar.addAction(icon,'октрыть хранилище ')
        self.connect(action_open_repo,QtCore.SIGNAL('triggered()'),self.__openRepository)
        
        icon = QtGui.QIcon('../Design/delete_repo.png')
        action_delete_repo = self.toolBar.addAction(icon,'удалить хранилище')
        self.connect(action_delete_repo,QtCore.SIGNAL('triggered()'),self.__deleteRepository)
        
        self.toolBar.addSeparator()
        
        icon = QtGui.QIcon('../Design/add_entity.png')
        action_delete_repo = self.toolBar.addAction(icon,'добавить Файл в хранилище')
        self.connect(action_delete_repo,QtCore.SIGNAL('triggered()'),self.__addFile)

        icon = QtGui.QIcon('../Design/update_entity.png')
        action_delete_repo = self.toolBar.addAction(icon,'изменить объект хранилища')
        self.connect(action_delete_repo,QtCore.SIGNAL('triggered()'),self.__updateEntity)
    
        icon = QtGui.QIcon('../Design/delete_entity.png')
        action_delete_repo = self.toolBar.addAction(icon,'удалить объект хранилища')
        self.connect(action_delete_repo,QtCore.SIGNAL('triggered()'),self.__deleteEntity)
          
#TOOLBAR
#STATUSBAR
        label = QtGui.QLabel('Текущий пользователь --- ' + self._user_repo.name+';',self)
        self.statusbar.addWidget(label)
        self.label_opening_repo = QtGui.QLabel(' Текущее хранилище --- ',self)
        self.statusbar.addWidget(self.label_opening_repo)
#STATUSBAR


#SLOTS AND SINGALS
        #для работы с хранилищем
        self.connect(self.action_open_repo,QtCore.SIGNAL("triggered()"),self.__openRepository)
        self.connect(self.action_delete_repo, QtCore.SIGNAL("triggered()"),self.__deleteRepository)
        self.connect(self.action_create_repo,QtCore.SIGNAL("triggered()"),self.__createRepository)
        
        #для работы с пользователями хранилища
        
        #self.connect(self._menu.add_user,QtCore.SIGNAL("triggered()"),self.__createUser)
        self.connect(self.action_switch_user,QtCore.SIGNAL("triggered()"),self.__switchUser)
        self.connect(self.action_delete_user_from_repo,QtCore.SIGNAL("triggered()"),self.__deleteUserFromRepo)
        
       
        self.connect(self.action_exit,QtCore.SIGNAL("triggered()"),self.__exitSmartFiles)
        
        #для работы с объектами хранилища
         
        self.connect(self.action_add_file,QtCore.SIGNAL("triggered()"),self.__addFile)
        self.connect(self.action_add_URL,QtCore.SIGNAL("triggered()"),self.__addURL)
        self.connect(self.action_mark_tag,QtCore.SIGNAL("triggered()"),self.__markTag)
        self.connect(self.action_mark_field,QtCore.SIGNAL("triggered()"),self.__markField)
        self.connect(self.action_change_entity,QtCore.SIGNAL("triggered()"),self.__updateEntity)
        self.connect(self.action_delete_entity,QtCore.SIGNAL("triggered()"),self.__deleteEntity)
        self.connect(self.tableView_entity,QtCore.SIGNAL('doubleClicked(QModelIndex)'),self.__selectEntity)
       
        #self.connect(self.action_view_repo_files,QtCore.SIGNAL('triggered()'),self.__workingRepoFiles)
        #для работы с метаданными
        self.connect(self.action_setting_tags,QtCore.SIGNAL('triggered()'),self.__settingTag)
        self.connect(self.action_setting_fields,QtCore.SIGNAL('triggered()'),self.__settingField)
        self.connect(self.treeView_metadata,QtCore.SIGNAL('clicked(QModelIndex)'),self.__selecteTags)
        #поиск
        self.connect(self.pushButton_search,QtCore.SIGNAL('clicked()'),self.__searchEntity)
        
        #переключение режима поиска (нейросеть/языкзапросов)
        self.connect(self.radioButton_neural_net,QtCore.SIGNAL('clicked()'),self.__clickNeuralnetRaioButton)
        self.connect(self.radioButton_request_language,QtCore.SIGNAL('clicked()'),self.__clickRequestLanguageRaioButton)
        #выбор пользователя для отображения его тегов 
        self.connect(self.comboBox_repo_users_metadata,QtCore.SIGNAL('currentIndexChanged(int)'),self.__selectedUserForView)

#SLOTS AND SINGALS
   
#SETTING WIDGETS PARAMETRES

        self.radioButton_request_language.setChecked(1)
        self.radioButton_neural_net.setChecked(0)
        
        
        self._table = self.tableView_entity
        self._db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        
        home_dir = os.path.join(SystemInfo.home_dir,self._user_repo.name)
        file_last_repo = os.path.join(home_dir,SystemInfo.last_repo_info)
        
        if os.path.exists(file_last_repo):
            #если существует то загружать путь к хранилищу и открывать его
            file_last_repo_info = open(file_last_repo,'rb')
            file_last_repo_info.seek(0)            
            self._path_to_repo = pickle.load(file_last_repo_info)
            
        else:
            #если не существует то создать пустое и ни чего не делать
            self._path_to_repo = None
            file_last_repo_info = open(file_last_repo,'wb')
            pickle.dump(self._path_to_repo, file_last_repo_info, pickle.HIGHEST_PROTOCOL)
        if self._path_to_repo:
            self.__openingRrepository()
#SETTING WIDGETS PARAMETRES        

#SETTING DOCKWIDGET_FILES

        
        
        # настройка отображение и скрывание dockwidget-ов
        self.connect(self.action_view_metadata,QtCore.SIGNAL('triggered()'),self.__dockWidget_metadataView)
        
        
       
        
        #TODO 
#            #в дальнейшем, когда будут сохраняться внешний вид окна, нужно будет каждый раз перед открытием окна 
#            #вызывать эти функции
#            self.__dockWidget_metadataView()
#            self.__dockWidget_repo_filesView()


#SETTING DOCKWIDGET_FILES

#HELPING
        self.pushButton_search.setToolTip('Найти в хранилище')
        self.dockWidget_tag.setToolTip('Теги хранилища')
        self.treeView_metadata.setToolTip('Используйте ctrl+щелчек левой кнопки мыши, для выбора тегов поискового запроса')
        self.comboBox_repo_users_metadata.setToolTip('Выберите пользователя, теги которого вы хотите увидеть')
        self.radioButton_neural_net.setToolTip('Поиск с сортеровокой результата нейросесть. Поиск осуществляется только по тегам.')
        self.radioButton_request_language.setToolTip('Поиск объектов хранилища по тегам, поля используя логические операции OR AND "()"')
#HELPING
        
    def __selectedUserForView(self,index):
        '''
            выбирает пользователя, для отображения его метаданных
        '''
        if index == 0:
            self.__settingModel('%')
        else:
            self.__settingModel(self.comboBox_repo_users_metadata.itemText(index))
        
    def __selecteTags(self,index):
        string_search=''
        for index in self.treeView_metadata.selectedIndexes():
            string_search+= ' ' + self.treeView_metadata.model().data(index)
        self.lineEdit_search.setText(string_search)
        
        
    def __clickNeuralnetRaioButton(self):
        '''
            переключение на нейросеть
        '''
        self.radioButton_request_language.setChecked(0)
        self.lineEdit_search.setText('')
        
        
    def __clickRequestLanguageRaioButton(self):
        '''
            переключение на языка запроса 
        '''
        self.radioButton_neural_net.setChecked(0)
        self.lineEdit_search.setText('')
        
    def __dockWidget_metadataView(self):
        '''
            скрывает октрывает окно с метаданными
        '''
        if self.action_view_metadata.isChecked():
            self.dockWidget_tag.show()
        else:
            self.dockWidget_tag.close()
        

#    
#    def __indexFile(self):
#        '''
#            пометка файла метоинформацией. создается запись о файле в БД
#        '''
#        
#        #TODO в дальнейшем можно будет выбирать по несколько элементов из дерева.
#        list_indexing = self.treeView_files_info.selectedIndexes()
#        if len(list_indexing)>0:
#            list_entityes=[]
#            for index in list_indexing:
#                file_path = self.treeView_files_info.model().data(index)
#                file_path = self._path_to_repo + os.path.sep + file_path 
#                entity = EntityManager.createEntity(entity_type=SystemInfo.entity_file_type, user_name=self._user_repo, file_path=file_path)
#                list_entityes.append(entity)
#            self.__indexingFile(list_entityes[0])
#        else:
#                self.info_window.setText('''не забываем выбирать файл
#                ''')
#                self.info_window.show()
#               # print('не забываем выбирать файл')
        
#    def __copyFile(self):
#        '''
#            вызывает вспомогательное окно для указания файла для копирования и директории хранилища, куда файл будет сохранен
#        '''
#        self._edit_window = EditFilesWindow(self._path_to_repo)
#        
#        self._edit_window.show()
#        self.connect(self._edit_window,QtCore.SIGNAL('copyFileInRepo(copy_info)'),self.__saveFile)
#        
#        
#    def __saveFile(self,copy_info):
#        '''
#            сохранение файла в хранилщие  
#        '''
#        try:
#            list_file_name = copy_info[0] 
#            progress_dialog = QtGui.QProgressDialog(self)
#            progress_dialog.setWindowModality(1)
#            d_progress = 100/len(list_file_name)
#            progress = 0
#            list_file_infs = []
#            list_error=[]
#            for copy_file_path in list_file_name:
#
#                QtGui.QApplication.processEvents()               
#                file_name = os.path.split(copy_file_path)[1]
#                file_path = os.path.join(copy_info[1],file_name)
#                if os.path.exists(file_path):
#                    list_error.append(file_path)
#                    continue
#                shutil.copyfile(copy_file_path, file_path)
#                new_file_info = self.__splitDirPath(file_path)
#                list_file_infs.append(new_file_info)
#                
#                
#                progress+=d_progress
#                progress_dialog.setValue(int(progress))
#                QtGui.QApplication.processEvents()
#            self._repo_manager.addFileInfo(list_file_infs)
#            if len(list_error)>0:
#                string_error = ''
#                for err in list_error:
#                    string_error+=err + '\n'
#                self.info_window.setText('файлы:' + string_error + '''  
#уже существует в хранилище. выбирите другую директорию для них или откажитись от добавления.''')
#                self.info_window.show()
#            self.__settingModel('%')
#        except RepoManager.ExceptionFileInfoIsExist as error:
#            print(error)
#            self.info_window.setText('Добавляемый файл уже существует в хранилище')
#            self.info_window.show()
#    
#    def __splitDirPath(self,file_path):
#        '''
#            получение относительного пути файла.
#            путь относительно хранилища
#        '''
#        
#        split_repodir_path = self._path_to_repo.split(os.sep)
#        split_file_path = file_path.split(os.sep)
#        len_repodir = len(split_repodir_path)
#        result_file_path =''
#        index = len_repodir
#        while index < len(split_file_path):
#            result_file_path += split_file_path[index] + os.path.sep 
#            index+=1
#        return result_file_path
#
#               
#        
#    def __deleteFile(self):
#        '''
#            удаления файла из хранилища
#        ''' 
#        list_files=[]   
#        list_indexes =self.treeView_files_info.selectedIndexes()
#        if len(list_indexes)>0:
#            for index in list_indexes:
#                file_path=self.treeView_files_info.model().data(index)
#                list_files.append(file_path)
#                os.remove(self._path_to_repo + os.sep + file_path)
#            self._repo_manager.deleteFilesInfo(list_files)
#            self.__settingModel('%')
#        else:        
#            self.info_window.setText('''не забываем выбирать файл
#            ''')
#            self.info_window.show()
    
    def saveNeuralNet(self):
        
        file_neurla_net = open(os.path.join(self._path_to_repo,SystemInfo.neural_net_file_path),'wb')
        pickle.dump(self._neural_net, file_neurla_net, pickle.HIGHEST_PROTOCOL)
        
    
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
                command = 'firefox'
                #command = 'xdg-open'
        subprocess.call([command, url])
    
    def __selectEntity(self,index):
#        print('попался')
        
        if self._is_open_repo:
            row=self._table.currentIndex().row()
            index = self._table.model().index(row,0)
            entity_id = self._table.model().data(index)
            index = self._table.model().index(row,3)
            type_entity = self._table.model().data(index)
            if type_entity==SystemInfo.entity_file_type:
                index = self._table.model().index(row,4)
                file_path = self._table.model().data(index)
                print('path to repo',self._path_to_repo)
                print('file_name',os.path.join(self._path_to_repo,file_path[1:]))
                file_path = os.path.join(self._path_to_repo,file_path)
                print('file',file_path)
                
    
                self.__startFile(file_path)
            elif type_entity==SystemInfo.entity_link_type:
                entity = self._entity_manager.createEntity(entity_type=type_entity, user_name=self._user_repo.name,id = entity_id)
                url = self._entity_manager.getURL(entity)
                self.__startURL(url)
            
            if self.radioButton_neural_net.isChecked():        
                    if len(self._select_list_tags)>0:
                        self._entity_manager.learningNeuralNet(entity_id, self._select_list_tags)
                    else:
                        self._entity_manager.learningNeuralNet(entity_id)
        
    def closeEvent(self,event):
        '''
            переопределяем событие закрытия окна. сохранение нужной инфы.
        '''
        self.__closeRepository()
#        self.emit(QtCore.SIGNAL('exitSmartFile()'))
        
        
        

            
    def __connnectBD(self):
        '''
            подключение к БД с метаинформацией хранилщиа
        '''
        try:
            self._db.setDatabaseName(os.path.join(self._path_to_repo,SystemInfo.metadata_file_name))
            self._db.open()
            self.__settingModel('%')
        except Exception as error:
            print('проблемы при подключении к БД или ее настройки')
            print(error)
            
            
    def __settingModel(self,user):
        '''
            отображение состояние базы на таблице
        '''
        if user==None:
            user='%'
        self._model.setQuery(self._string_request)# + " entity.user_name LIKE '" + user + "'" )
        self._model_metadata.setQuery("SELECT DISTINCT name FROM tag WHERE user_name LIKE '" + user + "'")

        if (self._model.lastError().isValid()):
            self.info_window.setText('Какие то проблемы при подключения модели')
            self.info_window.show()
            print('eroro in model where connecting BD file')
        if (self._model_metadata.lastError().isValid()):
            self.info_window.setText('Какие то проблемы при подключения модели')
            self.info_window.show()
            print('eroro in model where connecting BD file')
        self._table.setModel(self._model)
        self._table.show()
        
#        self.treeView_files_info.setModel(self._model_files_info)
#        self.treeView_files_info.show()
        
        self.treeView_metadata.setModel(self._model_metadata)
        self.treeView_metadata.show()
        #self.treeView_metadata.selectAll()
#        print('table is showing')
    def __settingComboBoxUsers(self):
        self.comboBox_repo_users_metadata.clear()
        self.comboBox_repo_users_metadata.insertItem(0,'все пользователи')
        self.comboBox_repo_users_metadata.insertItem(1,self._user_repo.name)
        for user in self._repo_manager.getUsersList():
            if user == self._user_repo.name:
                continue
            self.comboBox_repo_users_metadata.insertItem(2,user)
            
    def __openingRrepository(self):
        '''
            октрывает хранилище. парметр self._path_to_repo должен указывать на открываемое хранилище.
        '''
        try:
            self._repo_manager = RepoManager.openRepository(self._path_to_repo)
            self._repo_manager.identificationUser(self._user_repo)
            
            self.__settingComboBoxUsers()
            self.label_opening_repo.setText(' Текущее хранилище --- '+self._path_to_repo)
            self._entity_manager = self._repo_manager.getEntityManager() 
            
            self.__connnectBD()
            self._is_open_repo = True
        except RepoManager.ExceptionRepoIsNull as err:
            self.info_window.setText(''' Выбранная директория не является хранилищем.
            ''')
            self._path_to_repo = None
            self.info_window.show()
#            print('невозможно открыть хранилище')
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
            self.__openingRrepository()
        except Exception as error:
            self.info_window.setText('''
            какие то не учтенные траблы
            ''')
            self.info_window.show()
            print(error)
        
    
    def __openRepository(self):
        '''
            открывание хранилище
        '''
        try:
#            print('__openRepository')
            path_to_repo = QtGui.QFileDialog.getExistingDirectory(self,'открыть хранилище','/') 
            if path_to_repo:
                self._path_to_repo = path_to_repo
                self.__openingRrepository()
        except Exception as err:
            self.info_window.setText(''' какие то не учтенные траблы    
            ''')
            self.info_window.show()
            print(err)
            
            
    def __deleteRepository(self):
        '''
            удаление хранилища (всех мета файлов и директорий)
        '''
#        print('__deleteRepository')
        try:
            path_deleting_repo = self._path_to_repo
            self.__closeRepository()
            RepoManager.deleteRepository(path_deleting_repo)
#            self._path_to_repo = None
#            self.__disconnectBD()
#            self.label_opening_repo.setText('')
#            self._is_open_repo = False
            self.__settingModel('%')
        except RepoManager.ExceptionRepoIsNull as error:
            #print('не возможно удалить хранилище')
            self.info_window.show()
            self.info_window.setText('''Не возможно удалить хранилище
Нет открытых хранилищ.
            ''')
            
            #self.connect(self.info_window,QtCore.SIGNAL('closed()'))
            print(error)
        except Exception as error:
#            print('удаление хранилища')
#            print('какие то не учтеные траблы в RepoManager')
            self.info_window.show()
            self.info_window.setText('какие-то неучтенные траблы')
            print(error) 
        
    def __disconnectBD(self):
        '''
            отключение БД 
        '''
#        print('deleting db')
        self._db.close()
        self._model.clear()
        self._model.reset()
        self._model_metadata.clear()
        self._model_metadata.reset()
    
   
    def __createRepository(self):
        '''
            создание нового хранилища
        '''

        try:
            path_to_repo = QtGui.QFileDialog.getExistingDirectory(self,'выбирете директорию хранилища', '/')
            if path_to_repo:
                self._path_to_repo = path_to_repo
                self._user_repo.type = SystemInfo.user_type_admin
                self._repo_manager = RepoManager.initRepository(self._path_to_repo)
                self._repo_manager.addUserRepo(self._user_repo)
#                self._repo_manager.fillRepoFiles() # заполнение базы информацией о файлах хранилщиа.
                self._entity_manager = self._repo_manager.getEntityManager()     

                self._is_open_repo = True
                self.label_opening_repo.setText('Текущее хранилище ---')
                self.__connnectBD()
                self.__settingComboBoxUsers()
#               
        except RepoManager.ExceptionRepoIsExist as error:
            self.info_window.show()
            self.info_window.setText('''Не удалось создать хранилщие.
выбранная директория уже является хранилищем''')
            print(error)
        except Exception as error:
            
            self.info_window.setText('''какие то не учтенные траблы
            ''')
            self.info_window.show()
            print(error)

    def __closeRepository(self):
        if self._is_open_repo:
            self.__disconnectBD()
            home_dir = os.path.join(SystemInfo.home_dir,self._user_repo.name)
            file_last_repo = os.path.join(home_dir,SystemInfo.last_repo_info)
            file_last_repo_info = open(file_last_repo,'wb')
            pickle.dump(self._path_to_repo, file_last_repo_info, pickle.HIGHEST_PROTOCOL)
            self._path_to_repo = None
            self._entity_manager.saveNeuralNet()
            self._entity_manager = None
            self._repo_manager = None
            self.label_opening_repo.setText(' Текущее хранилище ---')
            self._is_open_repo = False
    
    def __switchUser(self):
        '''
            переключение пользователя. Посылается сигнал о переключение в окно StartingWindow
        '''
        #self.__closeRepository()
        self.emit(QtCore.SIGNAL('switchUser()'))
        self.close()
        
        
    def __deleteUserFromRepo(self):
        '''
            подготовка к удалению пользователя
        '''
        try:
            if self._is_open_repo:
                self.__deletingUser(self._user_repo)
                #self.__disconnectBD()
                self.__closeRepository()
            else:
                self.info_window.setText('''Необходимо открыть хранилище
            ''')
                self.info_window.show()
        except Exception as error:    
#            print('__deleteUserFromRepo')
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
            self.__settingModel('%')
        except RepoManager.ExceptionUserNotFound as error:    
#            print('__deletingUser')
            self.info_window.setText('''Удаляемый пользователь не найден.
            ''')
            self.info_window.show()        
            print(error)        
        except Exception as error:    
#            print('__deletingUser')
            self.info_window.setText('''неучтенные траблы в RepoManager
            ''')
            self.info_window.show()        
            print(error)
        
                    
    def __updateUser(self):
        '''
            подготовка к модификации пользователя
        '''
        if self._is_open_repo:
            try:
                
                self.edit_window = EditUserWindow(self._user_repo)
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
    #            print('__updateUser')
                print(error)
        else:
            self.info_window.setText('Не забываем открывать хранилище')
            self.info_window.show()
        
    def __updatingUser(self,user):
        '''
            модификация пользователя
        '''
        try:
            self._repo_manager.updateUser(user)
            #self.__settingModel('%')
            self.emit(QtCore.SIGNAL('updateUser(user)'),user)
        except RepoManager.ExceptionUserNotFound as error:    
            self.info_window.setText('''Не найден пользователь
            ''')
            self.info_window.show()        
            print(error)
        except Exception as error:    
            self.info_window.setText('''Не учтенные траблы в RepoManager
            ''')
            self.info_window.show()        
            print(error)    
        
        
    def __exitSmartFiles(self):
        '''
            завершение работы программы
        '''
        self.__disconnectBD()
        self.close()
    def __searchByNeuralNet(self):
        '''
            поиск с помощью нейросети
        '''
        if self.lineEdit_search.text()=="":
            self._string_request = SmartFilesMainWindow.SQLRequest + ' ORDER BY entity.neuralnet_raiting DESC'# "SELECT * FROM entity"
            self._entity_manager.searchByNeuralNet()
        else:
            request = cleareExtraSpace(self.lineEdit_search.text())
            self._select_list_tags = request.split(' ')  
            
            self._entity_manager.tmpPrintNeuralNet()
            self._entity_manager.searchByNeuralNet(self._select_list_tags)
            
            
            request = self._select_list_tags[0]
            index = 1
            while index < len(self._select_list_tags):
                request+= " OR " + self._select_list_tags[index] 
                index+=1
            self._string_request = ProcessingRequest.getSQLRequest(request,True)
        self.__settingModel('%')
#        print(self._string_request)
        
        
    def __searchByQueryLanguage(self):
        '''
            поис с помощью языка запроса
        '''

        if self.lineEdit_search.text()=="":
            self._string_request = SmartFilesMainWindow.SQLRequest 
        else: 
            self._string_request = ProcessingRequest.getSQLRequest(self.lineEdit_search.text())
            print(self._string_request)
            
        self.__settingModel('%')
        
    def __searchEntity(self):
        '''
            начала поиск объекта
        '''
        try:
            list_tags = []
            for index in self.treeView_metadata.selectedIndexes(): 
                    list_tags.append(self.treeView_metadata.model().data(index))
            if len(list_tags)>0: 
                if self.radioButton_neural_net.isChecked():
                    request = " ".join(list_tags)
                    self.lineEdit_search.setText(request)
                    self.__searchByNeuralNet()
                else:
                    request = ' AND '.join(list_tags)
                    self.lineEdit_search.setText(request)
                    self.__searchByQueryLanguage()
                
            else:
                
                if self.radioButton_neural_net.isChecked():
                    self.__searchByNeuralNet()
                else:
                    self.__searchByQueryLanguage()
        except ProcessingRequest.ExceptionInvalidRequestSyntaxis as error:
            print(error)
            self.info_window.setText('Ошибка синтаксиса языка запроса')
            self.info_window.show()
        
        
    
    
    def __addFile(self):
        '''
            добавление файла в хранилщие
        '''
        try:
            if self._is_open_repo:
                #entity = EntityManager.createEntity()
                self.edit_window = EditEntityWindow(path_to_repo = self._path_to_repo,user_repo= self._user_repo,object_type = SystemInfo.entity_file_type)
                
                self.edit_window.setWindowTitle('Окно редактирования файлов')
                self.edit_window.show()
                self.connect(self.edit_window,QtCore.SIGNAL('createEntity(list_entityes)'),self.__addingEntity)
                                                            #indexingFile(list_new_files)
              

                #отлавливание сигнала на добавление нового файла       
            else:
                self.info_window.setText(''' Для начало нужно открыть хранилище
            ''')
                self.info_window.show()
                     
        except Exception as error:
            self.info_window.setText(''' какието траблы с qt
            ''')
            self.info_window.show()
#            print('__addURL')
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
                self.edit_window.setWindowTitle('Окно редактирования URL ссылок')
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
            
            self._entity_manager.saveEntityes(list_entity)
#            print('длина списка добавляемых объектов - ',len(list_entity))
            
            self.__settingModel('%')
        except EntityManager.ExceptionNotFoundFileBD as error:
            self.info_window.setText('''Не найден файл с метаданными
            ''')
            self.info_window.show()
            print('__addingEntity проблемы:')
            print(error)
        except EntityManager.ExceptionEntityIsExist as error:
            self.info_window.setText('''Среди добавляемых файлов есть файлы уже присвоиные какому-то пользовтелю ''')
            self.info_window.show()
            self.__settingModel('%')
            print(error)
            
        except Exception as error:
            self.info_window.setText('''Какие то не учтенные траблы в EntityManager
            ''')
            self.info_window.show()
            print('__addingEntity')
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
#                    print('__markTag')
                    print(error)
    
            else:
                #print('А кто будет Entity выбирать для добавления тега?')
                self.info_window.setText('''Не выбран объект для пометки тегом.
            ''')
                self.info_window.show()
        else:
            self.info_window.setText('''Необходимо открыть хранилище.
            ''')
            self.info_window.show()
            

   
        
    def __markingTag(self,entity_id,marking_tag):
        '''
            пометка сущности тегом
        '''
#        print('marking tag')
        try:
            entity = self._entity_manager.loadEntityObj(entity_id)
            self._entity_manager.markTag(entity, marking_tag)  
            self.__settingModel('%')
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
                self.info_window.setText('''Не выбран объект для пометки полем.
            ''')
                self.info_window.show()
                #print('кто будет Entity выбирать для добавления поля')
        else:
            self.info_window.setText('''Необходимо открыть хранилище.
            ''')
            self.info_window.show()
            #print('может хранилище откроем?')
            
    def __markingField(self,entity_id,marking_field):
        '''
            пометка полем сущности
        '''     
#        print('get signal')
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
                    
                    entity = self._entity_manager.loadEntityObj(entity_id)
                    self.edit_window = EditEntityWindow(path_to_repo = self._path_to_repo,user_repo=self._user_repo,object_type=entity.object_type,entity=entity)
                    self.edit_window.show()
                    self.connect(self.edit_window,QtCore.SIGNAL("updateEntity(list_entityes)"),self.__updatingEntity)
                else:
                    self.info_window.setText('''Необходимо выбрать изменяемый объект.
            ''')
                    self.info_window.show()
                
                

                
            else:
                self.info_window.setText('''Необходимо открыть хранилище
            ''')
                self.info_window.show()
        except Exception as error:
            self.info_window.setText('''какие то неучтенные траблы в entity_manager 
            ''')
            self.info_window.show()
#            print('__updateEntity')
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
                    
                    
            self._entity_manager.saveEntityes((new_entity,))
            self.__settingModel('%')
        except EntityManager.ExceptionNotFoundFileBD as error:
            self.info_window.setText('''не найден файл с метаданным
            ''')
            self.info_window.show()
#            print('__updatingEntity проблемы:')
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
            
            selected_rows = []
            for selected_index in self._table.selectedIndexes():
                try:
                    selected_rows.index(selected_index.row())
                except ValueError:
                    selected_rows.append(selected_index.row()) 
            if len(selected_rows) >0:
              
                list_entity_id=[]
                for row in selected_rows:
                    index = self._table.model().index(row,0)
                    id = self._table.model().data(index)
                    list_entity_id.append(id)
                   
#                print(list_entity_id)   
                self.__deletingEntity(list_entity_id)
            else:
                self.info_window.setText('''Необходимо выбрать объект хранилщища
                ''')
                self.info_window.show()
                
        else:
            self.info_window.setText('''Необходимо открыть хранилище.
            ''')
            self.info_window.show()
            print('а хо хо не ху ху? открывай давай хранилщие')
            
            
        
    def __deletingEntity(self,list_entity_id):
        '''
            удаление сущности
        '''
        try:
            list_entity=[]
            
            progress_dialog = QtGui.QProgressDialog(self)
            progress_dialog.setWindowModality(1)
            d_progress = 100/len(list_entity_id)
            progress = 0
            for entity_id in list_entity_id:
                entity = self._entity_manager.loadEntityObj(entity_id)
                list_entity.append(entity)
                progress+=d_progress
                progress_dialog.setValue(int(progress))
                QtGui.QApplication.processEvents()
            progress_dialog.close()
            self._entity_manager.deleteEntity(list_entity)
            self.__settingModel('%')
        except EntityManager.ExceptionNotFoundFileBD as error:
            self.info_window.setText('''не найден файл с метаданными
            ''')
            self.info_window.show()
#            print('__deletingEntity')
            print(error)
        except RepoManager.ExceptionRepoIsNull as error:
            print('__deletingEntity')
            self.info_window.setText('''хранилище не существует
            ''')
            self.info_window.show()
            print(error) 
#        except Exception as error:
#            self.info_window.setText('''какие то неучтенные траблы в RepoManager или EntityManager
#            ''')
#            self.info_window.show()
#            print(error)#       


    def __deletingTag(self,tag):
        '''
            удаление тега
        '''
        self._entity_manager.deleteTag(tag)
        self.__settingModel('%')
        
        
    def __settingTag(self):
        '''
            управление тегами
        '''
        try:
            if self._is_open_repo:
                self.browse_window = BrowseMetadataWindow(self._user_repo, 'tag')
                self.browse_window.show()
                self.connect(self.browse_window,QtCore.SIGNAL('deleteTag(tag)'),self.__deletingTag)
    
                self.browse_window.close
            else:
                self.info_window.setText(''' Необходимо сначало открыть хранилище.
                ''')
                self.info_window.show()
        except Exception as err:
            self.info_window.setText('''Какие то не понятные траблы
                ''')
            self.info_window.show()
            print(err)
            
                
        
    def __deletingField(self,field):
        '''
            удаление поля и обновление таблцы тегов
        '''
        self._entity_manager.deleteField(field)
        self.__settingModel('%')
            
    def __settingField(self):
        '''
            управление полями
        '''
        try:
            if self._is_open_repo:
                self.browse_window = BrowseMetadataWindow(self._user_repo, 'field')
                self.browse_window.show()
                self.connect(self.browse_window,QtCore.SIGNAL('deleteField(field)'),self.__deletingField)
            else:
                self.info_window.setText('''Необходимо сначало открыть хранилище.
                ''')
                self.info_window.show()
        except Exception as error:
            self.info_window.setText('''Какие то не понятные траблы
                ''')
            self.info_window.show()
            print(error)
        
        
        
        
        
if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    user_repo = User('valexl', hash(-1874663864))
    myclass = SmartFilesMainWindow(user_repo)
    
    

    myclass.show()
    app.exec_()
#    print(os.path.split('__clickNeuralnetRaioButton/__clickNeuralnetRaioButton/aastelper.completions'))