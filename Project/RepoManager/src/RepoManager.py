'''
Created on 20.04.2010

@author: valexl
'''
import sqlite3 as sqlite
import os
from Repository import Repository
import SystemRepoInfo
import Entity
#import EntityManager
#import EntityManager

class RepoManager(object):
    '''
    classdocs
    '''

    
    def __init__(self):
        '''
            конструктор.. 
        '''
        #if not os.path.exists(SystemRepoInfo.metadata_dir):
        #    os.mkdir(SystemRepoInfo.metadata_dir)
        self._name_dbfile = os.path.join(SystemRepoInfo.metadata_dir,SystemRepoInfo.metadata_file)
        
        #временно файл с базой будет хранится в корне хранилище, а не в директории .metadata
        self._name_dbfile = SystemRepoInfo.metadata_file
    
    
    
    def create_repository(self,repo_path,user_name):
        '''
            создание нового хранилища или возращает существующие.
        '''
        path_dbfile = os.path.join(repo_path,self._name_dbfile)
        if not os.path.exists(path_dbfile):
            # если файл с базой не существует, то создается новый файл и заново инициализируются таблицы]
            print('the table disabled')
            self.__init_repository(path_dbfile,user_name)
        repo = Repository(path_dbfile)
        return repo
    
    
    
    def __init_repository(self,repo_path,user_name):
        '''
            создание таблиц и их заполнения необходимой для работы хранилища информацией.
        '''
       # print(repo_path)
        repoDB = sqlite.connect(repo_path)
        cursor = repoDB.cursor()
        cursor.execute("CREATE TABLE users("
                "name VARCHAR2(255) NOT NULL PRIMARY KEY,"
                "password INTEGER,"
                "description VARCHAR2(255),"
                "date_create TIMESTAMP)")
        self.__init_users_table(cursor, user_name)
        
        
        
        cursor.execute("CREATE TABLE dir_usage("
                       "path VARCHAR2(255) NOT NULL,"
                       "user_name VARCHAR2(255) NOT NULL ,"
                       "usage_status VARCHAR2 (30),"
                       "PRIMARY KEY (path,user_name),"
                       "FOREIGN KEY (user_name) REFERENCES users(name))"
                       )
        list_dirs=[]
        self.__init_dir_usage_table(cursor, list_dirs, user_name)
        
        
        
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
        self.__init_entity_table(cursor,repo_path,user_name)
            
        
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
      
        
       
    # инициализация таблицы пользователей  
    def __init_users_table(self,cursor, user_name):
        '''
            инициализация таблицы users. ЗАпись в базу информации о пользователе хранилища. 
        '''
        cursor.execute("INSERT INTO users"
                "(name,description)"
                "VALUES (?,?)",
                (user_name,'discription'))
    
    # конец
    # инициализация таблицы пользователей
    
    
    
    # инициализация таблицы включенных\отключенных директорий
    def __init_dir_usage_table(self,cursor, list_dirs, user_name):
        '''
            инициализация таблицы dir_usage. Заполняется информация о использованных и не использвоанных директориях хранилища.
        '''
        #необходима передавать в качестве параметров список директорий пользователя.
        pass
    
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
    def __init_entity_table(self, cursor, fileBD_path,user_name):
        '''
            инициализация таблицы entity. заполняется информацией о файлах хранилища 
        '''
       
        subdir_path = os.path.dirname(fileBD_path)
        list_files = self.__get_subdir_files(subdir_path)
        # Необходимо для вычисления SHA продублировать записи во временном файле.
        # Дублирование необходимо, что бы во время вычисления хеша не занималась база данных
    
        for file_path in list_files:
            cursor.execute("INSERT INTO entity"
                   "(file_path,user_name)"
                   "VALUES(?,?)",
                   (file_path,user_name))
      
        
            
            
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
        repoDB = sqlite.connect(os.path.join(repo_path,self._name_dbfile))
        cursor = repoDB.cursor()
        cursor.execute("SELECT id,file_path,user_name FROM entity")
        
        list_file_path = cursor.fetchall()
        return list_file_path
        
        
        
    def add_user_in_repository(self,reposit,user_name):
        
        '''
            добавляет пользователя в хранилище
        '''
        #if not os.path.exists(reposit.path):
            # если файл с базой не существует, то создается новый файл и заново инициализируются таблицы
        #    self.__init_repository(reposit.path,user_name)
        #else:
            
        repoDB = sqlite.connect(reposit.path)
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
    
    repo_path = '/tmp/tmp/'
    
    os.remove(os.path.join(repo_path,SystemRepoInfo.metadata_file))
    user_name = 'valexl'
    Rep = RepoManager()
    rep_obj = Rep.create_repository(repo_path,user_name)
    print('adding new user "vitvlkv"')
    user_name = 'vitvlkv'
    rep_obj = Rep.add_user_in_repository(rep_obj, user_name)
    print(rep_obj.path)
    print(rep_obj.list_users)
    print('delete user - ', user_name)
    Rep.delete_user(rep_obj, user_name)
    print(Rep.get_repository(repo_path).list_users)
    
    print(Rep.tmp_show_entity(repo_path))

      
    
    
    
#    Rep = RepoManager()
#    print(Rep.tmp_show_entity(repo_path))
#      