'''
Created on 06.06.2010

@author: valexl
'''
from PyQt4 import QtGui,QtCore
import sys
from lxml.html.defs import list_tags
#import PyQt4

class TreeItem(object):
    def __init__(self,list_data,parent=None):
        self.list_child=[]
        self.item_data=list_data
        self.parent_item = parent
        
    def appendChild(self,child):
        '''
            добавление наследника
        '''
        self.list_child.append(child)
        
    def child(self,row):
        '''
            возращает ребенка в позиции row
        '''
        return self.list_child[row]
    
        
    def childCount(self):
        '''
            количество наследников
        '''
        return len(self.list_child)
    
    
    def columnCount(self):
        '''
            количество данных
        ''' 
        return len(self.item_data)
    
    
    def data(self,column):
        '''
            данные в заданной колнке
        '''
        return self.item_data[column]
    
    
    def row(self):
        '''
            возвращает позицию в строке для текущего элемента
            (то есть он ребенок относительно предка. и какой он в списке детей у предка)
        '''
        if self.parent_item:
            return self.parent_item.list_childs.index(self)
        return 0
    
    def parent(self):
        '''
            вернуть предка
        '''
        return self.parent_item
    
     
    
    
class TagViewModelTree(QtCore.QAbstractItemModel):
    '''
        модель для представление тегами
    '''
    
    def __init__(self, list_data, parent=None):
        '''
            конструктор модели
        '''
        QtCore.QAbstractItemModel.__init__(self,parent)
        #self.root_item=None
        
        self.root_data = []
        self.root_item = TreeItem(self.root_data)
        self.setupModelData(list_data, self.root_item)
        
    
    
    def data(self,index,role):

        if not(index.isValid()):
            return QtCore.QVariant
    
        if not(role == QtCore.Qt.DisplayRole):
            return QtCore.QVariant
    
        item = TreeItem(index.internalPointer());
    
        return item.data(index.column())

    
    def flags(self,index):
        if not(index.isValid()):
            return 0
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    
    def headerData(self,section,orientation,role=QtCore.Qt.DisplayRole):
        if (orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole):
            return self.root_data.data(section)

        return QtCore.QVariant

    
    
    def index(self, row, column, parent = QtCore.QModelIndex()):
        if not (self.hasIndex(row,column,parent)):
            return QtCore.QModelIndex()
        if not(parent.isValid()):
            parent_item=self.root_item
        else:
            
            
            parent_item= TreeItem(parent.internalPointer())
            
            
        child_item = parent_item.child(row)
        if (child_item):
            return self.createIndex()
        else:
            return QtCore.QModelIndex()
        
    
    def parent(self,index):
        
        if not (index.isValid()):
            return QtCore.QModelIndex()
        #parent_item= TreeItem(parent.internalPointer())
        child_item = TreeItem(index.internalPointer())
        parent_item = child_item.parent()
        
        if (parent_item == self.root_item):
            return QtCore.QModelIndex()

        return self.createIndex(parent_item.row(), 0, parent_item)


    def rowCount(self, parent=QtCore.QModelIndex()):
        #TreeItem *parentItem;
        if (parent.column() > 0):
            return 0;

        if not(parent.isValid()):
            parentItem = self.root_item
        else:
            parentItem = TreeItem(parent.internalPointer());

        return parentItem.childCount()

    def columnCount(self,parent=QtCore.QModelIndex()):
        
        if (parent.isValid()):
            return TreeItem(parent.internalPointer()).columnCount()
        else:
            return self.root_item.columnCount()

    #защищенный НЕПОНЯТНо
    
    def setupModelData(self,list_tag_names,list_file_names,matrix_metadata,parent):

        parents=[parent]
        indentations=[0]
        
        tag_rows=list_tag_names
        entity_columns= list_file_names
        
        number=0
        while number < len(tag_rows):
            position=0
            column_data = []
            while position < len(tag_rows):
                if matrix_metadata[number,position]==1:
                    column_data.append(entity_columns[position])
                position+=1
            number+=2












class TagViewModel(QtCore.QAbstractListModel):
    '''
        модель для представление тегами
    '''
    PREV_LEVEL='..'
    
    def __init__(self, list_tags,list_entityes,matrix_relation, parent=None):
        '''
            конструктор модели
        '''
        QtCore.QAbstractItemModel.__init__(self,parent)
        
        self._tags = list_tags
        self._files = list_entityes 
        self._matrix_relation = matrix_relation
        
        
        self._selected_tags = self._tags
        self._selected_files = self._files
        self._selected_data = self._selected_tags + self._selected_files
        
        
        self._level_tags=[]
        
        print(self._selected_data)
        
        
    def data(self,index,role=QtCore.Qt.DisplayRole):
        if not(index.isValid()):
            return QtCore.QVariant
        if not(role == QtCore.Qt.DisplayRole):
            return QtCore.QVariant
    
        if role== QtCore.Qt.DisplayRole:
            return self._selected_data[index.row()]
        else:
            return QtCore.QVariant
        
    
    def headerData(self,section,orientation,role=QtCore.Qt.DisplayRole):
        if (orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole):
            return QtCore.QVariant('asdfa')
        else:
            return QtCore.QVariant
    

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._selected_data)

    
    def tagCount(self):
        return len(self._selected_tags)
    
    def level(self):
        return len(self._level_tags)
    
    
    def __cutMatrixRelation(self,matrix_relation,tag_name):
        '''
            обрезание матрицы по текущему тегу
        '''
        print('список тегов для выбора',self._selected_tags)
        print('выбираемый тег',tag_name)
        row = self._selected_tags.index(tag_name)
        
        
        selected_rows_index=[]
        selected_column_index=[]
        column=0
        
        for status in matrix_relation[row]:
            print(status)
            if status==1:
                tag_index=0
                for tag in self._selected_tags:
                    if not(tag==tag_name):
                        if matrix_relation[tag_index][column]==1:
                            selected_rows_index.append(tag_index)
                            #selected_tags.append(tag)
                    tag_index+=1
                selected_column_index.append(column)
            #    selected_files.append()
                
            column+=1
        print('selected rows index is=',selected_rows_index)
        print('selected_column_index is=',selected_column_index)
        
        
        
        
        
        
        selected_tags=[]
        selected_files=[]
        
        new_matrix_relation=[]
        row=0
        for row_index in selected_rows_index:
            new_matrix_relation.append([])
            selected_tags.append(self._tags[row_index])
            print('тег который будет в следующем запросе - ',self._tags[row_index])
            column=0
            for column_index in selected_column_index:
                new_matrix_relation[row].append(matrix_relation[row_index][column_index])
                column+=1
                try:
                    selected_files.index(self._files[column_index])
                except ValueError:
                    selected_files.append(self._files[column_index])
            row+=1
        #print(matrix_relation)
        self._selected_files = selected_files
        self._selected_tags = selected_tags
        print('и так.. в следующем запросе будут след теги',self._selected_tags)
        self._selected_data = self._selected_tags + self._selected_files
        
        return new_matrix_relation
        
    
    def __selectedTag(self,tag_name):
        
        self._level_tags.append(tag_name)     
        
        matrix_relation_by_selected_tags = self._matrix_relation
        print('матрица перед обработкой',self._matrix_relation)
        for tag in self._level_tags:
            matrix_relation_by_selected_tags = self.__cutMatrixRelation(
                                        matrix_relation_by_selected_tags, tag_name)
   
        self._selected_data = [self.PREV_LEVEL] + self._selected_data
        self.reset()
        print('the level tags is',self._level_tags)
        
        
        
    def __releaseTag(self):
        tag_name = self._level_tags.pop()
        
        print('вернул все назад',tag_name)
        
    
    def selectedItem(self,tag_name):
        print('tag_name is ',tag_name)
        
        if tag_name == self.PREV_LEVEL:
            self.__releaseTag()
        else:
            self.__selectedTag(tag_name)
        self.reset()    


class MyTableView(QtGui.QTableView):
    def __init__(self,parent=None):
        QtGui.QTableView.__init__(self,parent)
        
    
class MyWidget(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        
        self._table = QtGui.QTableView(self)
        self.button = QtGui.QPushButton('нажми что ли',self)
        vbox_layout = QtGui.QVBoxLayout()
        vbox_layout.addWidget(self._table)
        vbox_layout.addWidget(self.button)
        self.setLayout(vbox_layout)
        #list_string= QtCore.QString()
        self.list_tag = ['tag1','tag2','tag3'] 
        self.list_entityes = ['file1','file2','file3'] 
        self.matrix_relation = [[1,0,0],[1,1,0],[1,0,1]]
        
        
        self.model = TagViewModel(self.list_tag,self.list_entityes,self.matrix_relation)
        self.model.rowCount()
        self._table.setModel(self.model)
        self.connect(self.button,QtCore.SIGNAL('clicked()'),self.tmp)
        self.connect(self._table,QtCore.SIGNAL('clicked(QModelIndex)'),self.tmp2)
        self.index=1
    
        
    def tmp(self):
        self.model.setRowCount(self.index)
        self.index+=1
        
        
    def tmp2(self,index):
        row = index.row()
        if row<self.model.tagCount():
            print('tag')
            self.model.selectedItem(self.model.data(index))
        else:
            print('entitye')
        #if row.data.
        
        
if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    window = MyWidget()
   
    window.show()
    app.exec_()
    
    
    
    