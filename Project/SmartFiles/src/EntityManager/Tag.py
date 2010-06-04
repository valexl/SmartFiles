'''
Created on 20.04.2010

@author: valexl
'''

class Tag(object):
    '''
    classdocs
    '''


    def __init__(self, tag_name,user_name,date_create=None,description=""):
        '''
        Constructor
        '''
        self.name = tag_name
        self.user_name = user_name
        self.description = description
        self.date_create = date_create
    
    def getAttributes(self):
        '''
            возращает поля объекта в виде списка
        '''
        list_attributes = [self.name,self.user_name,self.description,self.date_create]    
        return list_attributes
        
        