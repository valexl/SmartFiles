'''
Created on 06.06.2010

@author: valexl
'''
import sys
from PyQt4 import QtGui,QtCore,QtSql
from ProcessingRequest import ProcessingRequest



class TagViewModel(QtCore.QAbstractListModel):
    '''
        модель для представление тегами
    '''
    PREV_LEVEL='..'
    
    def __init__(self, list_metadata, parent=None):
        '''
            конструктор модели
        '''
        
        #self.header_data=['id','entity_type','file_path','date_create']
        
        QtCore.QAbstractItemModel.__init__(self,parent)
      
        self._selected_metadata = list_metadata
        
    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._selected_metadata)
 
        
    def item_data(self,index,role=QtCore.Qt.DisplayRole):
        if not(index.isValid()):
            return QtCore.QVariant
        if not(role == QtCore.Qt.DisplayRole):
            return QtCore.QVariant
        
        return self._selected_metadata[index.row()]#[index.column()]
        
    
    def headerData(self,col,orientation,role=QtCore.Qt.DisplayRole):
        if (orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole):
            return QtCore.QVariant(self.header_data[col])
        elif (orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole):
            return QtCore.QVariant(col)
        else:
            return QtCore.QVariant


class FieldItem():
    def __init__(self,data,parent):
        self.child_items=[]
        self.parent_item = parent #сами поля (имя и тд)
        self.item_data = data #значение полей
        
    def appendChild(self,child):
        print('append_child')
        self.child_items.append(child)
        
        
    def child(self,row):
        return self.child_items[row]
    
    
    def childCount(self):
        return len(self.child_items)
        
    def columnCount(self):
        return len(self.item_data)
    
    def item_data(self,column):
        print('asdfasdfasddddddddddddddddfasdf')
        return self.item_data[column]
    
    def row(self):
        try:
            if self.parent_item:
                return self.parent_item.child_item.index(self)
        except ValueError as error:
            print('не найден элемент дерева')
            print(error)
        return 0
    
    
    def parent_item(self):
        return self.parent_item
            

class FieldViewModel(QtCore.QAbstractItemModel):
    '''
        модель для представление тегами
    '''
    
    def __init__(self, list_metadata, parent=None):
        '''
            конструктор модели
        '''
        QtCore.QAbstractItemModel.__init__(self,parent)
      
        
        self.root_data_title = 'Заголовок'
        list_metadata = ['value1','value2']
        list_fields = ('field','field2')
        list_fields='field'
        self.root_item = FieldItem(list_fields,parent)
        self.setupModelData(list_metadata,self.root_item)
        print('__init__',self.root_item.item_data)
        print('__init__',self.root_item.child(0).item_data)
        print('__init__',self.root_item.child(1).item_data)
        
    def setupModelData(self,list_data,root_item):
        '''
            возвращает сконструированное дерево
        '''
        
        parent = root_item
        items = [] 
        for data in list_data:
            newItem = FieldItem(data,parent)
            parent.appendChild(newItem)
            
    
    
    def data(self,index,role):
        print('121231a')
        if not index.isValid():
            return QtCore.QVariant()
        if not (role == QtCore.Qt.DisplayRole):
            return QtCore.QVariant()
        
        item = index.iternalPointer()
        
        return item.data(index.column)
    
#    def flags(self,index):
#        if not index.isValid():
#            return 0
#        #print('QtCore.Qt.ItemIsEnabled',QtCore.Qt.ItemIsEnabled)
#        #print(' QtCore.Qt.ItemIsSelectable',QtCore.Qt.ItemIsSelectable)
#        
#        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
    
    
    def headerData(self,col,orientation,role=QtCore.Qt.DisplayRole):
        
        if (orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole):
            return QtCore.QVariant(self.root_data_title)
#        elif (orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole):
#            return QtCore.QVariant(col)
        else:
            return QtCore.QVariant
       
    def index(self,row,column,parent):
        if self.hasIndex(row,column,parent):
            return QtCore.QModelIndex()
        parent_item = None
        
        if not (parent.isValid()):
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()
        
        child_item = parent_item.child(row)
        if child_item:
            return self.createIndex(row,column,child_item)
        else:
            return QtCore.QModelIndex()
            
            
    def parent(self, index):
        
        if not(index.isValid()):
            return QtCore.QModelIndex()
        child_item = index.internalPointer()
        parent_item = child_item.parent()
        
        if parent_item == self.root_item:
            return QtCore.QModelIndex
        
        return self.createIndex(parent_item.row(),0,parent_item)
    
        
    def rowCount(self, parent=QtCore.QModelIndex()): 
        if parent.column()>0:
            return 0 
        if not parent.isValid():
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()
       
    
       # return 3
        return parent_item.childCount() 
    
    
    def columnCount(self,parent=QtCore.QModelIndex()):
        if parent.isValid():
            return parent.iternalPointer().columnCount()
        else:
            return self.root_item.columnCount()
    
    
        
            
    
        
    
    
    
from EntityManager.EntityManager import EntityManager    
class MyTableView(QtGui.QTableView):
    def __init__(self,parent=None):
        QtGui.QTableView.__init__(self,parent)
        
    
class MyWidget(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        
        #self._table = QtGui.QTableView(self)
        self._table = QtGui.QTreeView(self)
        self.button = QtGui.QPushButton('нажми что ли',self)
        vbox_layout = QtGui.QVBoxLayout()
        vbox_layout.addWidget(self._table)
        vbox_layout.addWidget(self.button)
        self.setLayout(vbox_layout)
        #list_string= QtCore.QString()
        self._entity_manager = EntityManager('/tmp/tmp')

            
        
        self.list_tag = ['tag1','tag2','tag3']
#        for tag in self._entity_manager.getListTags():
#            self.list_tag.append(tag[0])
        
        self.list_entityes = [] 
        
        for file in self._entity_manager.searchEntityBySQL('SELECT file_path FROM entity'):
            self.list_entityes.append(file[0])
        
        
        
        
        
        self.model = TagViewModel(self.list_tag)
        self.model = FieldViewModel(self.list_tag)
        
        #self.model.rowCount()
        self._table.setModel(self.model)
        self.connect(self.button,QtCore.SIGNAL('clicked()'),self.tmp)
        self.connect(self._table,QtCore.SIGNAL('clicked(QModelIndex)'),self.tmp2)
        
        label = QtGui.QLabel()
        label.setText('asdfasdf')
        header = QtGui.QHeaderView(QtCore.Qt.Vertical,label)
        
        
        
        #self._table.setVerticalHeader(header)
        
        
    def tmp(self):
#        self.model.setRowCount(self.index)
#        self.index+=1
        pass
        
    def tagCount(self):
        return len(self.list_tag)
    def tmp2(self,index):
        row = index.row()
        if row<self.tagCount():
            print('tag')
            selected_tag = self.model.item_data(index)
            request = "SELECT * FROM tag WHERE name='"+selected_tag+"'" 
            
            print(request)
            self.list_tag = self._entity_manager.getListTags(request)
            #self.model.selectedItem(self.model.item_data(index))
        else:
            print('entitye')
#        #if row.data.
        pass
        
        
if __name__=='__main__':
     
    app = QtGui.QApplication(sys.argv)
    window = MyWidget()
   
    window.show()
    app.exec_()
    
    
    
    