'''
Created on 22.04.2010

@author: valexl
'''
import sqlite3 as sqlite
import os

class Repository(object):
    '''
    Класс репозиторий
    '''


    def __init__(self,repo_path):
        '''
            конструктор класса. инициализирует значение полей path и list_user
        '''
        self.path = repo_path        
        self.list_users = self.__get_repo_users()
        
        
    def __get_repo_users(self):
        
        repoDB = sqlite.connect(self.path)
        cursor = repoDB.cursor()
            
        cursor.execute("SELECT name FROM users")
        users = cursor.fetchall()
            
        return users

