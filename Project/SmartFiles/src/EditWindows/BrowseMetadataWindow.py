'''
Created on 07.06.2010

@author: valexl
'''
from PyQt4 import QtGui, QtCore, QtSql
from EntityManager.Tag import Tag
from EntityManager.Field import Field

class BrowseMetadataWindow(QtGui.QMainWindow):
    def __init__ (self,user_repo,type_metadata='tag',parent=None):
        
        QtGui.QMainWindow.__init__(self,parent)
        self._user_repo = user_repo
        self._str_request_select = "SELECT " + type_metadata + ".* FROM " + type_metadata + " WHERE user_name = '" + user_repo.name + "'"
        if type_metadata=='field':
            self._str_request_select += " AND not name='url' "
        self._type_metadata = type_metadata
        
        self.info_window = QtGui.QMessageBox()
        
        
        
        awidget = QtGui.QWidget()
        
        vbox_layout = QtGui.QVBoxLayout()        
        
        button_delete = QtGui.QPushButton('Удалить',self)   
        vbox_layout.addWidget(button_delete)
        
        button_cancel = QtGui.QPushButton('Завершить',self)
        vbox_layout.addWidget(button_cancel)
        
        vbox_layout.addStretch()
        awidget.setLayout(vbox_layout)
        
        dw = QtGui.QDockWidget()
        dw.setWidget(awidget)
        
        
        
        
        
        self._table = QtGui.QTableView(self)
    
        self.setCentralWidget(self._table)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dw)
        self.refresh()
        
        self.connect(button_delete,QtCore.SIGNAL('clicked()'),self.__delete)
        self.connect(button_cancel,QtCore.SIGNAL('clicked()'),self.__cancel)
        
    
    def __cancel(self):
        '''
            завершение работы с окном 
        '''
        self.close()
        
        
        
        

    def __getSelectingData(self,type_metadata='tag'):
        '''
            получить необходимые данные из выбранной записи
        '''
        row=self._table.currentIndex().row()
        index=self._table.model().index(row,0)
        metadata_name = self._table.model().data(index)
        if metadata_name==None:
            self.info_window.setText('''не выбрана запись для действия
            ''')
            self.info_window.show()
            
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
            self.info_window.setText('''проблемы при подключения к БД или ее настройки
            ''')
            self.info_window.show()
            print('проблемы при подключении к БД или ее настройки')
            print(error)   
    
    
if __name__=='__main__':
    import sys
    from RepoManager.User import User
    user_repo = User('asdfs')
    app = QtGui.QApplication(sys.argv)
    window=BrowseMetadataWindow(user_repo=user_repo,type_metadata='tag')
    window.show()
        
        
    sys.exit(app.exec_())
#        