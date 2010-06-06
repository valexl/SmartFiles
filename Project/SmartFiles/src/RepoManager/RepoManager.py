'''
Created on 20.04.2010

@author: valexl
'''
import sqlite3 as sqlite
import os
#import User.User
from  RepoManager.SystemInfo import SystemInfo
#import Entity
from EntityManager.EntityManager import EntityManager 
#from EntityManager import EntityManager
#import EntityManager
#import EntityManager
 
class RepoManager(object):
    '''
    classdocs
    '''
    class RepoException(Exception):
        pass
    class ExceptionErrorPasswordUser(RepoException):
        pass
    class ExceptionUserExist(RepoException):
        pass
    class ExceptionUserNotFound(RepoException):
        pass
    class ExceptionUserGuest(ExceptionUserNotFound):
        pass
    class ExceptionRepoIsExist(RepoException):
        pass
    class ExceptionRepoIsNull(RepoException):
        pass
    
     
    
    def __init__(self, path_to_repo):
        '''
            конструктор.. 
        '''
        
        self._path_to_repo = path_to_repo
        
        
        self._list_users=[]
        
        #временно файл с базой будет хранится в корне хранилище, а не в директории .metadata
        #self._name_dbfile = SystemInfo.metadata_file
        
    
        
    
        
        
    def getEntityManager(self):
        ''' Возвращает экземпляр EntityManager, уже привязанный к данному хранилищу. '''        
        return EntityManager(self._path_to_repo)
        
    
    @staticmethod
    def initRepository(path_to_new_repo, user_admin):        
        '''Это СТАТИЧЕСКИЙ метод, который позволяет создать новое пустое хранилище.
        Если при создании хранилища какие-либо ошибки --- должно вылетать иключение.
        Возвращает экземпляр RepoManager-а, привязанный к созданному хранилищу. 
        '''
        
       # print('initRepository()')
        path_metadata_dir = os.path.join(path_to_new_repo,SystemInfo.metadata_dir_name)
        if not os.path.exists(path_metadata_dir):#если директории нет, то создается новая
            os.mkdir(path_metadata_dir)
        else:
            raise RepoManager.ExceptionRepoIsExist('initRepository. директория ' + path_metadata_dir +' существует')
        
        path_metadata_file = os.path.join(path_to_new_repo, SystemInfo.metadata_file_name )
        if os.path.exists(path_metadata_file):
            raise RepoManager.ExceptionRepoIsExist('initRepository. файл с метаданными' + path_metadata_file + 'не найден')
        connect = sqlite.connect(path_metadata_file)
        cursor = connect.cursor()
        
        
        RepoManager.__initRepository(cursor,user_admin.name)
       
        
        connect.commit()
        repository = RepoManager(path_to_new_repo)
        print(os.path.join(repository._path_to_repo, SystemInfo.metadata_file_name))
        repository.addUserRepo(user_admin)
        return repository
    
    
    def deleteFilesInfo(self,file_path):
        '''
            удаление информации о файле
        '''
        repo_metadata_file = os.path.join(self._path_to_repo, SystemInfo.metadata_file_name)
        if os.path.exists(repo_metadata_file):
            connect = sqlite.connect(repo_metadata_file)
            cursor = connect.cursor()
            cursor.execute("DELETE FROM files_info "
                           " WHERE path = ? ",
                           (file_path,) 
                           )
            connect.commit()
        else:
            raise RepoManager.ExceptionRepoIsNull('deleteFileInfo. Не найден файл ' + 
                                                  repo_metadata_file + 
                                                  ' с метаданными' )
        
    @staticmethod
    def __insertFileInfoIntoBD(cursor,file_name):
        '''
            запись информации о файлах в базу данных
        '''
        cursor.execute( "INSERT INTO files_info "
                            " (path) "
                            " VALUES (?) ",
                            (file_name,)
                           )
        
        
            
    def addFileInfo(self,file_name):
        '''
            добавление инфомрации о файлах, которые находятся в хранилище 
            и еще не проиндексированы
        '''
        
        repo_metadata_file = os.path.join(self._path_to_repo, SystemInfo.metadata_file_name)
        if os.path.exists(repo_metadata_file):
            connect = sqlite.connect(repo_metadata_file)
            cursor = connect.cursor()
            RepoManager.__insertFileInfoIntoBD(cursor, file_name)
            connect.commit()
        else:
            raise RepoManager.ExceptionRepoIsNull('addFileInfo. Не найден файл ' + 
                                                  repo_metadata_file + 
                                                  ' с метаданными' )

         
    
    def fillRepoFiles(self):
        '''
            заполнение базы информацией о файлах хранилища
        '''
        path_metadata_file = os.path.join(self._path_to_repo, SystemInfo.metadata_file_name )
        if not os.path.exists(path_metadata_file):
            raise RepoManager.ExceptionRepoIsExist('fillRepoFiles. файл с метаданными' + path_metadata_file + 'не найден')
        connect = sqlite.connect(path_metadata_file)
        cursor = connect.cursor()
        
        list_files = RepoManager.__get_subdir_files(self._path_to_repo)
        for file_name in list_files:
            RepoManager.__insertFileInfoIntoBD(cursor, file_name)
        connect.commit()
        #RepoManager.addFileInfo(repo_file_info, list_files)
        
        
    @staticmethod
    def __get_subdir_files(repodir_path,subdir_path=''):
        '''
            возращает список файлов всего хранилища, с учетом поддиректорий
        '''
        list_result = []
        
#        print('the path of subdir is',os.path.join(repodir_path,subdir_path))
        
        list_object = os.listdir(os.path.join(repodir_path,subdir_path))
        for obj_path in list_object:
            if obj_path[0]!= '.':
                obj_path=os.path.join(subdir_path,obj_path)
                
                if os.path.isfile(os.path.join(repodir_path,obj_path)):
                    list_result.append(obj_path)
                else:
                    list_result+=RepoManager.__get_subdir_files(repodir_path,obj_path)
        
        return list_result        
        
        
    @staticmethod
    def __initRepository(cursor, user_name):
        '''
            создание таблиц и их заполнения необходимой для работы хранилища информацией.
        '''
        #
        #Создание пустых таблиц с метаинформацией хранилища 
        #
        
        #таблица с файлами хранилища
        cursor.execute("CREATE TABLE files_info ("
                       " path VARCHAR2(255) PRIMARY KEY )"
                       )
        #таблица пользователей
        cursor.execute("CREATE TABLE users ("
                "name VARCHAR2(255) NOT NULL PRIMARY KEY,"
                "password INTEGER,"
                "user_type VARCHAR2(10) NOT NULL, "
                "description VARCHAR2(255),"
                "date_create TIMESTAMP)")
                
        #таблица подключенных/отключенных директорий
        cursor.execute("CREATE TABLE dir_usage("
                       "path VARCHAR2(255) NOT NULL,"
                       "user_name VARCHAR2(255) NOT NULL ,"
                       "usage_status VARCHAR2 (30),"
                       "PRIMARY KEY (path,user_name),"
                       "FOREIGN KEY (user_name) REFERENCES users(name))"
                       )
        #таблица сущности
        cursor.execute("CREATE TABLE entity("
                       "id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"
                       "title VARCHAR2(255),"
                       "notes VARCHAR2(255),"
                       "object_type VARCHAR2(10),"
                       "file_path VARCHAR2(255),"
                       "file_size INTEGER,"
                       "file_date_modifired TIMESTAMP,"
                       "file_hash INTEGER,"
                       "neuralnet_raiting INTEGER DEFAULT 0,"
                       "user_name VARCHAR2(255) NOT NULL,"
                       "date_create TIMESTAMP,"
                       "FOREIGN KEY (user_name) REFERENCES users(name))"       
        )    
        #таблица тегов
        cursor.execute("CREATE TABLE tag ( "
                       "name VARCHAR2(255) NOT NULL,"
                       "user_name VARCHAR2(255) NOT NULL,"
                       "description VARCHAR2(255),"
                       "date_create TIMESTAMP,"
                       "PRIMARY KEY (name,user_name),"
                       "FOREIGN KEY (user_name) REFERENCES users(name))"
                      
                       )
        #таблица связи тегов с сущностью
        cursor.execute("CREATE TABLE entity_tags ("
                       "entity_id INTEGER NOT NULL,"
                       "tag_name VARCHAR2(255) NOT NULL,"
                       "user_name VARCHAR2(255)NOT NULL,"
                       "PRIMARY KEY (entity_id,tag_name,user_name),"
                       "FOREIGN KEY (entity_id) REFERENCES entity(id)"
                       #"FOREIGN KEY (user_name) REFERENCES users(name),"
                       "FOREIGN KEY (user_name) REFERENCES tag(user_name),"
                       "FOREIGN KEY (user_name) REFERENCES entity(user_name),"
                       "FOREIGN KEY (tag_name) REFERENCES tag(name))"
                       )
        #таблица полей
        cursor.execute("CREATE TABLE field ("
                       "name VARCHAR2(255) NOT NULL,"
                       "user_name VARCHAR2(255) NOT NULL,"
                       "description VARCHAR2(255),"
                       "value_type VARCHAR2(10),"
                       "date_create TIMESTAMP,"
                       "PRIMARY KEY (name,user_name),"
                       "FOREIGN KEY (user_name) REFERENCES users(name))"
                       )
        #таблица связей сущностей с полями
        cursor.execute("CREATE TABLE entity_fields("
                       "entity_id INTEGER NOT NULL,"
                       "field_name VARCHAR2(255) NOT NULL,"
                       "user_name VARCHAR2(255) NOT NULL,"
                       "value VARCHAR2(255),"
                       "PRIMARY KEY (entity_id,field_name,user_name),"
                       "FOREIGN KEY (entity_id) REFERENCES entity(id),"
                       #"FOREIGN KEY (user_name) REFERENCES users(name),"
                       "FOREIGN KEY (user_name) REFERENCES entity(user_name),"
                       "FOREIGN KEY (user_name) REFERENCES field(user_name),"
                       "FOREIGN KEY (field_name) REFERENCES field(name))"
                       )
        #таблица группы
        cursor.execute("CREATE TABLE groups("
                       "name VARCHAR2(255) NOT NULL,"
                       "user_name VARCHAR2(255) NOT NULL,"
                       "description VARCHAR2(255),"
                       "date_created TIMESTAMP,"
                       "PRIMARY KEY (name,user_name),"
                       "FOREIGN KEY (user_name) REFERENCES users(name))"
                       )
        #таблица группировки тегов
        cursor.execute("CREATE TABLE groups_tags("
                       "group_name VARCHAR2(255) NOT NULL,"
                       "tag_name VARCHAR2(255) NOT NULL,"
                       "user_name VARCHAR2(255)NOT NULL,"
                       "PRIMARY KEY(group_name,tag_name,user_name),"
                       "FOREIGN KEY(group_name) REFERENCES groups(name),"
                       "FOREIGN KEY(tag_name) REFERENCES tag(name),"
                       "FOREIGN KEY (user_name) REFERENCES groups(user_name),"                       
                       "FOREIGN KEY(user_name) REFERENCES tag(name))"
                       
                       )
        #таблица группировки полей
        cursor.execute("CREATE TABLE groups_fields("
                       "group_name VARCHAR2(255) NOT NULL,"
                       "field_name VARCHAR2(255) NOT NULL,"
                       "user_name VARCHAR2(255) NOT NULL,"
                       "PRIMARY KEY(group_name,field_name,user_name),"
                       "FOREIGN KEY(group_name) REFERENCES groups(name),"
                       "FOREIGN KEY(field_name) REFERENCES field(name),"
                       "FOREIGN KEY (user_name) REFERENCES groups(user_name),"                       
                       "FOREIGN KEY(user_name) REFERENCES field(name))"
                       )
        #
        #Создание пустых таблиц с метаинформацией хранилища 
        #  
      
        
       
    
    @staticmethod
    def __addUser(cursor,user_repo):
        '''
            сохраняет инфу о  пользователе в указанную базу. 
            Необходим для добавление как в домашнюю директорию пользователя, 
            так и в директорию .metadata хранилища.
        '''
       
        cursor.execute("INSERT INTO users "
                    " (name, password, user_type, description) "
                    " VALUES (?,?,?,?) ",
                    (user_repo.name,user_repo.password, user_repo.type,user_repo.description))
#        except:
#            cursor.execute(" SELECT COUNT (*) FROM USERS WHERE name = ? ",
#                              (user_repo.name,)
#                              )
#            if cursor.fetchone()[0]>0:
#                raise RepoManager.ExceptionUserExist('не верный пароль')
#            else:
#                raise RepoManager.ExceptionUserGuest('текущий пользователь не зарегистрирован в хранилище')

    def addUserRepo(self,user_repo):
        '''
            добавляет пользователя в хранилище
        '''    
        path_metadata_file = os.path.join(self._path_to_repo,SystemInfo.metadata_file_name)
        if os.path.exists(path_metadata_file):
            connect = sqlite.connect(path_metadata_file)
            cursor = connect.cursor()
            RepoManager.__addUser(cursor, user_repo)
            connect.commit()
            self._list_users.append(user_repo)
        else:
            raise RepoManager.ExceptionRepoIsNull('__addUser. не найден файл ' + 
                                                  path_metadata_file +
                                                ' с метаданными' )
        
        
    def updateUser(self,user_repo):
        '''
            модификаия пользователя хранилщиа
        '''
        path_metadata_file = os.path.join(self._path_to_repo, SystemInfo.metadata_file_name )
        if os.path.exists(path_metadata_file):
            connect = sqlite.connect(path_metadata_file)
            cursor = connect.cursor()
                
            cursor.execute(" UPDATE  users "
                    " SET password=?, description=? "
                    " WHERE name=? ",
                    (user_repo.password, user_repo.description,user_repo.name))
            connect.commit() 
            self._list_users.append(user_repo)
        else:
            raise RepoManager.ExceptionRepoIsNull('udateUser. не найден файл ' + 
                                                  path_metadata_file +
                                                   ' с метаданными' )
    @staticmethod
    def __purgeUser(cursor,user_name):
        '''
            освобождение всех записией в БД от удаляемого пользователя
        '''
        cursor.execute("SELECT file_path FROM entity "
                       " WHERE entity.object_type = ? AND "
                       " entity.user_name = ?",
                       (SystemInfo.entity_file_type,user_name)
                       )
        files = cursor.fetchall()
        for file_path in files:
            RepoManager.__insertFileInfoIntoBD(cursor, file_path[0])
        
        cursor.execute(" DELETE FROM entity_fields WHERE user_name = ? ",
                           (user_name,)
                           )
        cursor.execute(" DELETE FROM entity_tags WHERE user_name = ? ",
                           (user_name,)
                           )
        cursor.execute(" DELETE FROM tag WHERE user_name = ? ",
                           (user_name,)
                           )
        cursor.execute(" DELETE FROM field WHERE user_name = ? ",
                           (user_name,)
                           )
        cursor.execute(" DELETE FROM entity WHERE user_name = ? ",
                           (user_name,)
                           )
       
           
    def deleteUser(self,user):
        '''
            удаление пользователя
        '''
#        connect = sqlite.connect(os.path.join(self._path_to_repo,os.path.join(SystemInfo.metadata_dir,SystemInfo.metadata_file)))
        path_metadata_file = os.path.join(self._path_to_repo, SystemInfo.metadata_file_name )
        
        if os.path.exists(path_metadata_file):

            connect = sqlite.connect(path_metadata_file)
            cursor = connect.cursor()
            RepoManager.__purgeUser(cursor,user.name)
#            cursor.execute("DELETE FROM users WHERE name=?",
#                    (user.name,))
            connect.commit()
        else:
            raise RepoManager.ExceptionRepoIsNull('delete_user. не найден файл ' + 
                                                  path_metadata_file +
                                                   ' с метаданными' )

    
    @staticmethod    
    def __getRepoUsers(repo_path):
        '''
            получение списка пользователей в данном хранилище
        '''
        #connect = sqlite.connect(os.path.join(repo_path,os.path.join(SystemInfo.metadata_dir,SystemInfo.metadata_file)))
        path_metadata_file = os.path.join(repo_path, SystemInfo.metadata_file_name )
        if os.path.exists(path_metadata_file):
        
            connect = sqlite.connect(path_metadata_file)
            cursor = connect.cursor()
                
            cursor.execute("SELECT name,password FROM users")
            users = cursor.fetchall()
            if len(users)>0:
                return users
            else:
                raise Exception('в хранилище нет пользователей')
        else:
            raise RepoManager.ExceptionRepoIsNull('_getRepoUsers. Не найден файл ' + 
                                                  path_metadata_file + 
                                                  ' с метаданными' )

    def identificationUser(self,user_repo):
        '''
            идентификация пользователя в хранилище. если успех то возращает 1.
            иначе вызывается исключение RepoManager.ExceptionUserGuest
        '''
        for user in self._list_users:
            if (user[0]==user_repo.name):
                flag = 0
                if (int(user_repo.password)==int(user[1])):
                    return 1
                else:
                    RepoManager.ExceptionUserExist('не верный пароль пользователя')            
        raise RepoManager.ExceptionUserGuest("Текущий пользователь не зарегестирован в хранилище")
    
    
    @staticmethod    
    def openRepository(repo_path):
        '''
            открывание пользователем хранилища
        '''
        list_users = RepoManager.__getRepoUsers(repo_path)
        repository = RepoManager(repo_path)
        repository._list_users=list_users
        return repository        
        
        
        
        
#    def save_repository(self):    
#        _save
    @staticmethod
    def deleteRepository(repo_path):
        if repo_path == None:
            raise RepoManager.ExceptionRepoIsNull('не найдено хранилщие')
        dir_name = os.path.join(repo_path,SystemInfo.metadata_dir_name)
        file_name = os.path.join(repo_path,SystemInfo.metadata_file_name)
        neural_net = os.path.join(repo_path,SystemInfo.neural_net_file_path)
        if os.path.exists(dir_name):
            os.remove(file_name)
            os.remove(neural_net)
            os.rmdir(dir_name)
        else:
            raise RepoManager.ExceptionRepoIsNull('deleteRepository. не найден каталог с метаданными ' + repo_path)
        
        


    
if __name__ == '__main__':
    
    
    repo_path = '/tmp/tmp'
    
    RepoManager.deleteRepository(repo_path)

      