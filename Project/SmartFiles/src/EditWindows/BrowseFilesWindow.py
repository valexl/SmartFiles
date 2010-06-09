'''
Created on 07.06.2010

@author: valexl
'''
import os
import shutil
from PyQt4 import QtGui, QtCore, QtSql


from EditWindows.EditFilesWindow import EditFilesWindow
from EntityManager.EntityManager import EntityManager
from RepoManager.SystemInfo import SystemInfo




class BrowseFilesWindow(QtGui.QWidget):
    '''
        окно для работы с файлами хранилища (добавление новых файлов, удаление существующих, пометка метаинформацией)
    '''
    def __init__(self, path_to_repo,user_repo, parent=None):
        QtGui.QWidget.__init__(self,parent)
        self._user_repo = user_repo
        self._path_to_repo = path_to_repo
        self.info_window = QtGui.QMessageBox()
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
            self.info_window.setText('''не забываем выбирать файл
            ''')
            self.info_window.show()
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

if __name__ == '__main__':
    import sys
    from RepoManager.User import User
    app = QtGui.QApplication(sys.argv)
    user_repo = User('alexl')
    window = BrowseFilesWindow('tmp/tmp', user_repo)
    window.show()
    app.exec_()
    
        