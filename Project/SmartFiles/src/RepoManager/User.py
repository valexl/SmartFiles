'''
Created on 22.04.2010

@author: valexl
'''
import sqlite3 as sqlite
import os
from RepoManager.SystemInfo import SystemInfo 




#Этот класс объединяем вместе с RepoManager!!!
class User(object):
    '''
    Класс репозиторий
    '''
    

    def __init__(self,user_name,password=None,type=SystemInfo.user_type_other,description=''):
        '''
            конструктор класса. инициализирует значение полей path и list_user
        '''
        self.name = user_name
        self.password = password
        self.type = type
        self.description = description        
        

