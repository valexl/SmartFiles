'''
Created on 20.04.2010

@author: valexl
'''

class Field(object):
    '''
    classdocs
    '''


    def __init__(self,field_name,user_name,field_value,value_type,field_date_create,field_description=''):
        '''
        Constructor
        '''
        
        self.name = field_name
        self.user_name = user_name
        self.description = field_description
        self.value_type = value_type
        self.date_create = field_date_create
        
        self.value = field_value
    
    def get_attributes (self):
        '''
            возращает поля объекта в виде двойного списка. где 1й список это атрибуты для таблицы field, а второй список для таблицы entity_fields
        '''
        list_attributes = [[self.name,self.user_name,self.value_type,self.description,self.date_create],[self.value]]
        
        return list_attributes
    
        
        
#    cursor.execute("CREATE TABLE field ("
#                       "name VARCHAR2(255),"
#                       "user_name VARCHAR2(255),"
#                       "description VARCHAR2(255),"
#                       "value_type VARCHAR2(10),"
#                       "date_create TIMESTAMP,"
#                       "PRIMARY KEY (name,user_name),"
#                       "FOREIGN KEY (user_name) REFERENCES users)"
#                       )    