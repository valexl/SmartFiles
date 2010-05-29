'''
Created on 27.05.2010

@author: valexl
'''
import os

import SystemInfo
import sqlite3 as sqlite
from User import User

class InstallUser(object):
    '''
    Добавляет пользователей в домашнюю директорию
    '''
    _home_dir= SystemInfo.home_dir
    class ExceptionUser(Exception):
        pass
    class ExceptionRepoIsNull(ExceptionUser):
        pass
    class ExceptionUserExist(ExceptionUser):
        pass
    class ExceptionUserNotFound(ExceptionUser):
        pass
    class ExceptionNoUsers(ExceptionUser):
        pass
    
    
    @staticmethod
    def initHomeDir():
        '''
            инициализация домашней директории
        '''
        dir_userinfo_path = os.path.join( SystemInfo.home_dir,SystemInfo.metadata_dir_name)
        file_userinfo_path = os.path.join(SystemInfo.home_dir,SystemInfo.file_user_info)
        
        if  not os.path.exists(dir_userinfo_path):
            os.mkdir(dir_userinfo_path) 
            if not os.path.exists(file_userinfo_path):
                connect = sqlite.connect(file_userinfo_path)
                cursor = connect.cursor()
                InstallUser.__initTables(cursor)
                connect.commit()
                
                
        connect = sqlite.connect(file_userinfo_path)
        cursor = connect.cursor()        
        cursor.execute( "SELECT COUNT (*) FROM users ")
        if cursor.fetchone()[0]==0:
            raise InstallUser.ExceptionNoUsers('не зарегестрировано ни одного пользователя')
        
        
    @staticmethod
    def __initTables(cursor):
        '''
            создание пустых таблиц
        '''
        cursor.execute("CREATE TABLE users ("
                " name VARCHAR2(255) NOT NULL PRIMARY KEY,"
                " password INTEGER,"
                #" user_type VARCHAR2(10) NOT NULL, "
                " description VARCHAR2(255))")
        
        
#        cursor.execute("CREATE TABLE reposits ("
#                " id INTEGER NOT NULL PRIMARY KEY,"
#                " user_admin"
#                "PATH VARCHAR2(255))")
#                #" user_type VARCHAR2(10) NOT NULL, "
#        
#        cursor.execute("CREATE TABLE repo_users ("
#                " user_name VARCHAR2(255) NOT NULL,"
#                " repo_id INTEGER NOT NULL, "
#                " PRIMARY KEY (user_name,repo_id), "
#                " FOREIGN KEY (user_name) REFERENCES users(name), "
#                " FOREIGN KEY (repo_id) REFERENCES reposits(id)) ")
                
        
        
         
        
        
    @staticmethod
    def addUser(user_system):
        '''
            добавление пользователя в домашнюю директорию
        '''
        file_userinfo_path = os.path.join(SystemInfo.home_dir,SystemInfo.file_user_info)
        if os.path.exists(file_userinfo_path):
            connect = sqlite.connect(file_userinfo_path)
            cursor=connect.cursor()
            
            InstallUser.__saveUser(cursor, user_system)
            connect.commit()
    
    @staticmethod
    def identificationUser(user_name,password):
        '''
            Идентификация пользователя
        '''
        passw = password #преобразования с str в int (пароль должен быть зашифрованный)
        return InstallUser.__scaningUserRepo(user_name,passw)
    
    @staticmethod
    def __scaningUserRepo(user_name,password):
        '''
            поиск пользователя по логингу и паролю
        '''
        
        file_userinfo_path = os.path.join(SystemInfo.home_dir,SystemInfo.file_user_info)
        if not os.path.exists(file_userinfo_path):
            raise InstallUser.ExceptionRepoIsNull('__scaningUserRepo. файл с метаданными' + 
                                                   file_userinfo_path + 'не найден')
        connect = sqlite.connect(file_userinfo_path)
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM users "
                       " WHERE name = ? AND password = ?",
                       (user_name, password)
                        )
        user_attributes = cursor.fetchone()
        if  not user_attributes == None:
            user_name, password, description = user_attributes
            return User(user_name = user_name, password = password,description = description)
        else:
            raise InstallUser.ExceptionUserNotFound('error in login or password')    
        
    @staticmethod
    def __saveUser(cursor,user_system):
        '''
             сохранение пользователя в домашнюю директорию
        '''
#        try:
        cursor.execute(' SELECT count (*) FROM users '
                              " WHERE name = ? ",
                              (user_system.name,)
                              )
        if cursor.fetchone()[0] > 0:
            raise InstallUser.ExceptionUserExist('пользователь с таким логином существует')
        cursor.execute("INSERT INTO users "
                    " (name, password, description) "
                    " VALUES (?,?,?) ",
                    (user_system.name,user_system.password, user_system.description))
#        except sqlite.IntegrityError as error:
#            raise InstallUser.ExceptionUserExist('пользователь с таким логином существует')
#            print(error)

    @staticmethod
    def updateUser(user_repo):
        path_metadata_file = os.path.join(SystemInfo.home_dir, SystemInfo.file_user_info)
        if os.path.exists(path_metadata_file):
            connect = sqlite.connect(path_metadata_file)
            cursor = connect.cursor()
                
            cursor.execute(" UPDATE  users "
                    " SET password=?, description=? "
                    " WHERE name=? ",
                    (user_repo.password,user_repo.description,user_repo.name))
            connect.commit() 
            
        else:
            raise InstallUser.ExceptionRepoIsNull('udateUser. не найден файл ' + 
                                                  path_metadata_file +
                                                   ' с метаданными' )
    @staticmethod
    def pritnUsers():
        '''
            временная функция. (вывод всех пользователей системы (показывает таблицу users находящейся в домашней директории))
        '''
        file_userinfo_path = os.path.join(SystemInfo.home_dir,SystemInfo.file_user_info)
        
        connect = sqlite.connect(file_userinfo_path)
        cursor=connect.cursor()
        cursor.execute("SELECT * FROM users"
                           )
        print(cursor.fetchall())
        
if __name__ == '__main__':
    
    
    repo_path = '/tmp/tmp'
    user_system = User('valexl')
#    InstallUser.initHomeDir()
#    InstallUser.addUser(user_system)
    InstallUser.pritnUsers()
        