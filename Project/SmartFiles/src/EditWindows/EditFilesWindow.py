'''
Created on 07.06.2010

@author: valexl
'''
from PyQt4 import QtGui, QtCore
import os

        
class EditFilesWindow(QtGui.QWidget):
    def __init__(self, repo_path, parent=None):
        QtGui.QWidget.__init__(self,parent)
        self._path_to_repo = repo_path
        self.info_window = QtGui.QMessageBox()
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
       # self.connect(self,QtCore.SIGNAL('closeEvent(QCloseEvent*))'),self.tmp)
    def closeEvent(self,event):
#        print('asdfa')
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
                self.info_window.setText('''епт... файл выбери!
            ''')
                self.info_window.show()
            #    print('епт.. файл выбери!')
        else:
            self.info_window.setText('''Выбранная директория не является хранилищем''')
            self.info_window.show()
            
        
        
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
        if list_files_names:
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
    
        