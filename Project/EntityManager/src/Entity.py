'''
Created on 20.04.2010

@author: valexl
'''
from Tag import Tag
from Field import Field
class Entity(object):
    '''
    Класс "Сущность". 
    '''    

    def __init__(self, title, entity_type, user_name, file_path=None, list_tags=[], list_fields=[], 
                file_size=0, file_date_modifired=None, file_hash=None, 
                 notes='', date_created=None, id=None):
        '''
        Constructor
        '''
        
        self.id = id
        
        self.title = title
        self.object_type = entity_type
        self.user_name = user_name
        
        self.file_path = file_path
        self.file_size = file_size
        self.file_hash = file_hash
        self.file_date_modifired = file_date_modifired
        
        self.date_create = date_created
        self.notes = notes
     
        self.list_tags = list_tags
        self.list_fields = list_fields
        
           
    def addTag (self,tag):
        '''
            пометка сущности тегом
        '''
        self.list_tags.append(tag)


    def deleteTag(self,tag_name):
        '''
            тег отделяется от объекта entity
        '''
        index = 0
        for tag in self.list_tags:
            if tag.name == tag_name:
                break
            index+=1
        if index <= len(self.list_tags):
            self.list_tags.pop(index)

                  
    def isTagExist(self,tag_name):
        '''
            помечен ли данным тегом объект entity
        '''
        for tag in self.list_tags:
            if tag.name == tag_name:
                return 1
        return 0 

    
    def addField(self,field):
        '''
            пометка полем сущности
        '''
        self.list_fields.append(field)

        
    def deleteField(self,field_name):
        '''
            особождает объект entity от данного поля
        '''
        index = 0
        for field in self.list_fields:
            if field.name == field_name:
                break
            index+=1
        if index <= len(self.list_fields):
            self.list_fields.pop(index)

        
    def isFieldExist(self,field_name):
        '''
            помечен ли данным полем объект entity
        '''
        for field in self.list_fields:
            if field.name == field_name:
                return 1
        return 0

    
    def getTagAttributes(self):
        '''
            возращает список списков атрибутов тегов, помечающих данный объект entity
        '''
        result_list = []
        for tag in self.list_tags:
            print(tag)
            result_list.append(tag.getAttributes())
        return result_list
        
        
    def getFieldAttributes(self):
        '''
            возращает список списоков атрибутов полей, помечающих данный объект entity
        '''
        result_list = []
        for field in self.list_fields:
            result_list.append(field.getAttributes())
        return result_list
        