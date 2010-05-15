'''
Created on 20.04.2010

@author: valexl
'''

class Tag(object):
    '''
    classdocs
    '''


    def __init__(self, tag_name,user_name,tag_date_create=None,tag_description=""):
        '''
        Constructor
        '''
        self.name = tag_name
        self.user_name = user_name
        self.description = tag_description
        self.date_create = tag_date_create
    
    def get_attirbutes(self):
        '''
            возращает поля объекта в виде списка
        '''
        list_attributes = [self.name,self.user_name,self.description,self.date_create]    
        return list_attributes
    
#        cursor.execute("CREATE TABLE tag("
#                       "name VARCHAR2(255),"
#                       "user_name VARCHAR2(255),"
#                       "description VARCHAR2(255),"
#                       "date_create TIMESTAMP,"
#                       "PRIMARY KEY (name,user_name),"
#                       "FOREIGN KEY (user_name) REFERENCES users)"
#                       )

        
        