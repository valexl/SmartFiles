'''
Created on 20.04.2010

@author: valexl
'''
import sqlite3 as sqlite
import os
from Repository import Repository
import SystemRepoInfo
import Entity
from EntityManager import EntityManager
#import EntityManager
#import EntityManager

class RepoManager(object):
    '''
    classdocs
    '''
    
    
    def __init__(self, path_to_repo):
        '''
            конструктор.. 
        '''
        
        #Открываем хранилище path_to_repo
        #Проверяем хранилище ли это? Есть ли .metadata
        #Если нет, то сразу же выкидываем исключение
        
        #if not os.path.exists(SystemRepoInfo.metadata_dir):
        #    os.mkdir(SystemRepoInfo.metadata_dir)
        self._name_dbfile = os.path.join(SystemRepoInfo.metadata_dir,SystemRepoInfo.metadata_file)
        self._path_to_repo = path_to_repo
        
        #временно файл с базой будет хранится в корне хранилище, а не в директории .metadata
        self._name_dbfile = SystemRepoInfo.metadata_file
        
    def getEntityManager(self):
        ''' Возвращает экземпляр EntityManager, уже привязанный к данному хранилищу. '''        
        return EntityManager(self._path_to_repo)    
    
    
    
    @staticmethod
    def init_repository(path_to_new_repo, user_admin_name):        
        '''Это СТАТИЧЕСКИЙ метод, который позволяет создать новое пустое хранилище.
        Если при создании хранилища какие-либо ошибки --- должно вылетать иключение.
        Возвращает экземпляр RepoManager-а, привязанный к созданному хранилищу. 
        '''
        
        print('init_repository()')
        
        RepoManager.__init_repository(path_to_new_repo, user_admin_name)
        return RepoManager(path_to_new_repo)
    
    
    
    
    
    #Этот метод тоже надо бы сделать СТАТИЧЕСКИМ
    @staticmethod
    def __init_repository(repo_path, user_name):
        '''
            создание таблиц и их заполнения необходимой для работы хранилища информацией.
        '''
       # print(repo_path)
        path_metadata_file = os.path.join(repo_path, SystemRepoInfo.metadata_file)
        if os.path.exists(repo_path):
            raise Exception('ыдлвоаолыдвоа')
        print('path_metadata_file=', path_metadata_file)
        repoDB = sqlite.connect(path_metadata_file)
        cursor = repoDB.cursor()
        cursor.execute("CREATE TABLE users ("
                "name VARCHAR2(255) NOT NULL PRIMARY KEY,"
                "password INTEGER,"
                "description VARCHAR2(255),"
                "date_create TIMESTAMP)")
        repoDB.commit()
        
        cursor.execute("INSERT INTO users "
                "(name, description)"
                "VALUES (?,?)",
                (user_name,'123123123'))
        
        
        
        
        cursor.execute("CREATE TABLE dir_usage("
                       "path VARCHAR2(255) NOT NULL,"
                       "user_name VARCHAR2(255) NOT NULL ,"
                       "usage_status VARCHAR2 (30),"
                       "PRIMARY KEY (path,user_name),"
                       "FOREIGN KEY (user_name) REFERENCES users(name))"
                       )
        
        cursor.execute("CREATE TABLE entity("
                       "id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"
                       "title VARCHAR2(255),"
                       "notes VARCHAR2(255),"
                       "object_type VARCHAR2(10),"
                       "file_path VARCHAR2(255),"
                       "file_size INTEGER,"
                       "file_date_modifired TIMESTAMP,"
                       "file_hash INTEGER,"
                       "user_name VARCHAR2(255) NOT NULL,"
                       "date_create TIMESTAMP,"
                       "FOREIGN KEY (user_name) REFERENCES users(name))"       
        )    
        
            
        
        #
        #Создание пустых таблиц с метаинформацией хранилища 
        #
        cursor.execute("CREATE TABLE tag ( "
                       "name VARCHAR2(255) NOT NULL,"
                       "user_name VARCHAR2(255) NOT NULL,"
                       "description VARCHAR2(255),"
                       "date_create TIMESTAMP,"
                       "PRIMARY KEY (name,user_name),"
                       "FOREIGN KEY (user_name) REFERENCES users(name))"
                      
                       )
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
        cursor.execute("CREATE TABLE field ("
                       "name VARCHAR2(255) NOT NULL,"
                       "user_name VARCHAR2(255) NOT NULL,"
                       "description VARCHAR2(255),"
                       "value_type VARCHAR2(10),"
                       "date_create TIMESTAMP,"
                       "PRIMARY KEY (name,user_name),"
                       "FOREIGN KEY (user_name) REFERENCES users(name))"
                       )
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
        cursor.execute("CREATE TABLE groups("
                       "name VARCHAR2(255) NOT NULL,"
                       "user_name VARCHAR2(255) NOT NULL,"
                       "description VARCHAR2(255),"
                       "date_created TIMESTAMP,"
                       "PRIMARY KEY (name,user_name),"
                       "FOREIGN KEY (user_name) REFERENCES users(name))"
                       )
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
        repoDB.commit()
      
        
       
   
    
    
    
    def __get_list_dirs(self):
        '''
            получить список использованных пользователем директорий.
        '''
        # возможно лучше сделать через дополнительный параметр при создании хранилища.
        list_dirs = []
        
        return list_dirs
    # конец
    # инициализация таблицы включенных\отключенных директорий
    
    
    
    
    # инициализация таблицы сущностей
#    def __init_entity_table(self, cursor, fileBD_path,user_name):
#        '''
#            инициализация таблицы entity. заполняется информацией о файлах хранилища 
#        '''
#       
#        subdir_path = os.path.dirname(fileBD_path)
#        list_files = []
#        # Необходимо для вычисления SHA продублировать записи во временном файле.
#        # Дублирование необходимо, что бы во время вычисления хеша не занималась база данных
#    
#        for file_path in list_files:
#            cursor.execute("INSERT INTO entity"
#                   "(file_path,user_name)"
#                   "VALUES(?,?)",
#                   (file_path,user_name))
      
        
            
            
        # нужна функция добавления сущности в базу... либо добавление через EntityManager либо здесь отдельной функцией...
        # так как лучше всего что бы RepoManager работал со всем хранилищем, а не  отдельными элементами, 
        # то добалвение одногой или небольшого количества объектов хранилщища будет делать EntityManager..
         
        
        
        

    def __get_subdir_files(self,repodir_path,subdir_path=''):
        '''
            возращает список файлов всего хранилища, с учетом поддиректорий
        '''
        list_result = []
        
        print('the path of subdir is',os.path.join(repodir_path,subdir_path))
        
        list_object = os.listdir(os.path.join(repodir_path,subdir_path))
        for obj_path in list_object:
            if obj_path[0]!= '.':
                obj_path=os.path.join(subdir_path,obj_path)
                
                if os.path.isfile(os.path.join(repodir_path,obj_path)):
                    list_result.append(obj_path)
                else:
                    list_result+=self.__get_subdir_files(repodir_path,obj_path)
        
        return list_result
    # конец    
    # инициализация таблицы сущностей

    
        
    def tmp_show_entity (self,repo_path):
        '''
            вспомогательная функция для проверки записывания таблицы entity
        '''
        repoDB = sqlite.connect(os.path.join(self._path_to_repo,self._name_dbfile))
        cursor = repoDB.cursor()
        #cursor.execute("SELECT id,file_path,user_admin_name FROM entity")
        cursor.execute("SELECT * FROM users")
        
        list_file_path = cursor.fetchall()
        return list_file_path
        
        
        
    def add_user_in_repository(self,user_name):
        
        '''
            добавляет пользователя в хранилище
        '''
        #if not os.path.exists(reposit.path):
            # если файл с базой не существует, то создается новый файл и заново инициализируются таблицы
        #    self.__init_repository(reposit.path,user_name)
        #else:
            
        repoDB = sqlite.connect(os.path.join(self._path_to_repo,self._name_dbfile))
        cursor = repoDB.cursor()
                
        self.__init_users_table(cursor, user_name)
        repoDB.commit() 
        reposit.list_users.append(user_name)
        
        return reposit
    
    
    
    def delete_user(self,reposit,user_name):
        '''
        '''
        repoDB = sqlite.connect(reposit.path)
        cursor = repoDB.cursor()
        
        cursor.execute("DELETE FROM users WHERE name=?",
                (user_name,))
#        cursor.execute('SELECT COUNT(name) FROM users')
#        count = cursor.fetchone()
        repoDB.commit()
        return 0
    
    def get_repository(self,repo_path):
        '''
        '''
        repo = Repository(os.path.join(repo_path,self._name_dbfile))
        return repo
        
    
    
if __name__ == '__main__':
    
    
    repo_path = '/tmp/tmp'
    
    if os.path.exists(os.path.join(repo_path, SystemRepoInfo.metadata_file)):
        os.remove(os.path.join(repo_path, SystemRepoInfo.metadata_file))
      
    if not os.path.exists(repo_path):        
        os.mkdir(repo_path)
    
    
    user_name = 'valexl'    
    rep_obj = RepoManager.init_repository(repo_path,user_name)
    
    
#    print('adding new user "vitvlkv"')
#    user_name = 'vitvlkv'
#    rep_obj = rep_obj.add_user_in_repository(user_name)
##    print(rep_obj.path)
##    print(rep_obj.list_users)
#    print('delete user - ', user_name)
##    Rep.delete_user(rep_obj, user_name)
##    print(Rep.get_repository(repo_path).list_users)
##    
    print(rep_obj.tmp_show_entity(repo_path))

      
    
    
    
#    Rep = RepoManager()
#    print(Rep.tmp_show_entity(repo_path))
#      