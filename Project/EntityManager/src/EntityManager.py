'''
Created on 20.04.2010

@author: valexl
'''
import sqlite3 as sqlite
import os
import SystemRepoInfo
from Entity import Entity,Tag,Field
#from Tag import Tag

class EntityManager:
    '''
        Класс управление сущностью.
    '''
    
    
    def __init__(self,repo_path):
        '''
           конструктор класса. Регестрирует EntityManager в конкретном хранилище
        '''
        self._name_dbfile = os.path.join(SystemRepoInfo.metadata_dir,SystemRepoInfo.metadata_file)
        print(self._name_dbfile)
        self._name_dbfile = SystemRepoINfo.metadata_file
    
        self._repo_path = os.path.join(repo_path,self._name_dbfile)
          
    def create_entity(self,file_path,user_name,tags=[],fields=[]):
        '''
            создание нового объекта класса Entity
        '''
        obj_entity = Entity(file_path,user_name,tags,fields)
        return obj_entity
        
    def tmp_insert_func(self,file_path):
        '''
        временная функция добавление файла в entity
        '''
        connect=sqlite.connect(self._repo_path)
        cursor=connect.cursor()
        #нужен id кортэжа таблицы entity
        
        cursor.execute("INSERT INTO entity"
                       "(file_path)"
                       "VALUES(?)",
                      (file_path,))
        connect.commit()
           
    def tmp_select_entity(self,user_name):
        '''
            временная функция выборки одного id из entity
        '''
        connect=sqlite.connect(self._repo_path)
        cursor=connect.cursor()
        
        cursor.execute("SELECT * FROM entity "
                       "WHERE user_name=?",
                       (user_name,)
                       )
        
        res = cursor.fetchall()
        print(res)
        
    def tmp_select_all_entity(self,file_path):
        '''
            временная функция выборки id всех элементов из entity
        '''
        connect=sqlite.connect(self._repo_path)
        cursor=connect.cursor()
        
        cursor.execute("SELECT * from entity")
        
        res = cursor.fetchall()
        print(res)
                
    def tmp_select_all_tag(self):
        '''
            временная функция выборки всех name из tag
        '''
        connect=sqlite.connect(self._repo_path)
        cursor=connect.cursor()
        
        cursor.execute("SELECT name from tag")
        
        res = cursor.fetchall()
        print(res)
      
      
    def tmp_select_all_entitytag(self):
        '''
            временная функция выборки всех элементов из entity_tags
        '''
        connect=sqlite.connect(self._repo_path)
        cursor=connect.cursor()
        cursor.execute(#"SELECT tag.* FROM (tag "
                       #"INNER JOIN entity_tags ON entity_tags.tag_name = tag.name)"
                       #" INNER JOIN "                
                       #"(entity_tags INNER JOIN entity ON entity.id = entity_tags.entity_id) AS t ON t.user_name = tag.user_name)"
                       
                       
                       "SELECT tag.* FROM tag "
                       "INNER JOIN (entity_tags INNER JOIN " 
                       " entity ON entity.id = entity_tags.entity_id "
                       " AND entity.user_name = entity_tags.user_name) AS t1"
                       " ON t1.user_name = tag.user_name AND t1.tag_name = tag.name "
                       )
        res = cursor.fetchall()
        print(res)
         
    def tmp_select_all_fields(self):
        '''
            временная функция выборки всех name из field
        '''
        connect=sqlite.connect(self._repo_path)
        cursor=connect.cursor()
        cursor.execute("SELECT name from field")
        res = cursor.fetchall()
        print(res)
            
    def tmp_select_all_entityfield(self):
        '''
            временная функция выборки всех элементов из entity_tags
        '''
        connect=sqlite.connect(self._repo_path)
        cursor=connect.cursor()
        cursor.execute("SELECT * from entity_fields")
        res = cursor.fetchall()
        print(res)
     
    def __get_entity_id(self,cursor,file_path):
        '''
            возращает id таблицы entity или None если записи с заданным file_path нет
        '''
        cursor.execute("SELECT id FROM entity "
                       "WHERE file_path=?",
                       (file_path,)
                       )
        
        return cursor.fetchone()
    
    
    def __save_entity_and_get_id(self,connect,file_path,user_name,file_size):
        '''
            сохранить объект в entity если такго в базе нет и получить его id
        '''
        cursor=connect.cursor()
        id_file = self.__get_entity_id(cursor, file_path)
        if id_file==None:
          #  print('id is not finding')
            cursor.execute("INSERT INTO entity"
                           "(file_path,user_name,file_size)"
                           "VALUES(?,?,?)",
                          (file_path,user_name,file_size))
            connect.commit()
            return cursor.lastrowid
        else:
           # print('id is finding')
            return id_file[0]      
      
    def __save_tag(self,cursor,id_file,tag_attributes):
        '''
            сохранить тег в таблице tag и в таблицы связи entity_tags если тег еще не сохранен 
        '''
          
        #сохранение в таблице tag
            
        cursor.execute("SELECT COUNT(*) FROM tag "
                           "WHERE name = ? AND user_name = ?",
                           (tag_attributes[0],tag_attributes[1])
                           )
        if cursor.fetchone()[0] == 0:
            #    print('creating new tag')
            cursor.execute("INSERT INTO tag "
                       "(name,user_name,description,date_create)"
                       "VALUES (?,?,?,?)",
                        tag_attributes  
                      )
            # сохранение в таблице entity_tags
        cursor.execute("SELECT COUNT(*) FROM entity_tags "
                           "WHERE entity_id = ? AND tag_name = ? AND user_name = ?",
                           (id_file,tag_attributes[0],tag_attributes[1])
                           )
        if cursor.fetchone()[0]==0:    
            cursor.execute("INSERT INTO entity_tags "
                               "(entity_id,tag_name,user_name)"
                               "VALUES(?,?,?)",
                               (id_file,tag_attributes[0],tag_attributes[1])
                               )
            
    def __save_field(self,cursor,id_file,field_attributes):
            # запись в field
        cursor.execute("SELECT COUNT (*) FROM field "
                           "WHERE name = ? AND user_name = ? ",
                           (field_attributes[0][0],field_attributes[0][1]) 
                           )
        if cursor.fetchone()[0]==0:
            cursor.execute("INSERT INTO field"
                            "(name,user_name,value_type,description,date_create)"
                            "VALUES(?,?,?,?,?)",
                            field_attributes[0]
            )
               
            # запись в entity_fields
        cursor.execute("SELECT COUNT (*) FROM entity_fields "
                        "WHERE entity_id=? AND field_name = ? AND user_name = ? ",
                        (id_file, field_attributes[0][0],field_attributes[0][1]) 
        )
        if cursor.fetchone()[0]==0:
            # print('creating new entity_fields')
            cursor.execute("INSERT INTO entity_fields"
                            "(entity_id,field_name,user_name,value)"
                            "VALUES(?,?,?,?)",
                            (id_file,field_attributes[0][0],field_attributes[0][1],field_attributes[1][0])
            )
        

             
    def save_entity_obj(self,entity):
        '''
            запись entity в базу данных
        '''
        connect=sqlite.connect(self._repo_path)
        # запись entity
        id_file = self.__save_entity_and_get_id(connect, entity.file_path, entity.user_name,entity.file_size)
        # запись tag 
        cursor = connect.cursor()
        for tag_attributes in entity.get_tag_attributes():    
            self.__save_tag(cursor, id_file,tag_attributes )
        # запись field
        for field_attributes in entity.get_field_attributes():
            #print(field_attributes)
            self.__save_field(cursor, id_file, field_attributes)
        connect.commit()
            
           
    def __get_list_tags(self,connect,file_path,user_name):
        list_tags = []
        cursor = connect.cursor()
        
       # print(file_path)
        
        cursor.execute("SELECT tag.* FROM tag "
                       "INNER JOIN (entity_tags INNER JOIN " 
                       " entity ON entity.id = entity_tags.entity_id AND entity.file_path = ? "
                       " AND entity.user_name = entity_tags.user_name) AS t1"
                       " ON t1.user_name = tag.user_name AND t1.tag_name = tag.name ",
                       (file_path,)
                       )
        
        
        for tag_attributes in cursor.fetchall():
            list_tags.append(Tag(tag_attributes[0],tag_attributes[1],tag_attributes[2],tag_attributes[3]))
        return list_tags
        
    def __get_list_fields(self,connect,file_path,user_name):
        list_tags = []
        cursor = connect.cursor()
        
       # print(file_path)
        
        cursor.execute("SELECT field.name, field.user_name, t1.value, field.value_type, field.date_create,field.description FROM field "
                       "INNER JOIN (entity_fields INNER JOIN " 
                       " entity ON entity.id = entity_fields.entity_id AND entity.file_path = ? "
                       " AND entity.user_name = entity_fields.user_name) AS t1"
                       " ON t1.user_name = field.user_name AND t1.field_name = field.name ",
                       (file_path,)
                       )
        
        
        for field_attributes in cursor.fetchall():
            list_tags.append(Field(field_attributes[0],field_attributes[1],field_attributes[2],field_attributes[3],field_attributes[4],field_attributes[5]))
#        print(cursor.fetchall())
        return list_tags
        
    def load_entity_obj(self,file_path,user_name):
        connect = sqlite.connect(self._repo_path)
        cursor = connect.cursor()
        
        tags = self.__get_list_tags(connect,file_path,user_name)
        fields = self.__get_list_fields(connect, file_path, user_name)
        #print(fields)
        entity = Entity(file_path,user_name,tags,fields)
        
        return entity
        
        
    def __delete_entity(self,connect,file_path):
        '''
            удаляет запись из enity и возращает id
        '''
        cursor = connect.cursor()
        id_entity = self.__get_entity_id(cursor, file_path)[0]
    
        cursor.execute("DELETE FROM entity "
                       "WHERE file_path=?",
                       (file_path,)
                       )
       # connect.commit()
        return id_entity
    
    def __delete_entity_tags(self,connect,id_entity,list_tag_attributes):
        '''
            удаляютСя заиписи из entity_tags. если в этих записей больше нет ни одной записи с данными тегами, 
            то удаляются и эти теги из tag
        '''
        
        cursor = connect.cursor()
        cursor.execute("DELETE FROM entity_tags "
                       "WHERE entity_id = ?",
                       (id_entity,)
                       )
        #connect.commit()
        list_deleting_tag_name = []
        for tag_attributes in list_tag_attributes:
            cursor.execute("SELECT COUNT(*) FROM entity_tags "
                           "WHERE tag_name = ? AND user_name = ?",
                           (tag_attributes[0],tag_attributes[1])
                           )
            if cursor.fetchone()[0]==0:
                self.__delete_tag(cursor,tag_attributes[0],tag_attributes[1])
                list_deleting_tag_name.append(tag_attributes[0])
        #return list_deleting_tag_name
       # connect.commit()
    def __delete_tag(self,cursor,tag_name,user_name):
        '''
            удаление тега из базы
        '''
        cursor.execute("DELETE FROM tag "
                       "WHERE name=? AND user_name = ?",
                       (tag_name, user_name)
                       )
        
    def __delete_entity_fields(self,connect,id_entity,list_field_attributes):
        '''
            удаляютСя заиписи из entity_fields. если в этих записей больше нет ни где связей с данным полем, 
            то удаляются и запись и из field
        '''
        cursor = connect.cursor()
        cursor.execute("DELETE FROM entity_fields "
                       "WHERE entity_id = ?",
                       (id_entity,)
                       )
       # connect.commit()
        list_deleting_field_name = []
        for field_attributes in list_field_attributes:
           
            cursor.execute("SELECT COUNT(*) FROM entity_fields "
                           "WHERE field_name = ? AND user_name = ?",
                           (field_attributes[0][0],field_attributes[0][1])
                           )
            if cursor.fetchone()[0]==0:
                self.__delete_field(cursor,field_attributes[0][0],field_attributes[0][1])
                list_deleting_field_name.append(field_attributes[0][0])
        #return list_deleting_field_name
        #connect.commit()
    def __delete_field(self,cursor,field_name,user_name):
        '''
            удалание поля из базы
        '''
        cursor.execute("DELETE FROM field "
                       "WHERE name=? AND user_name = ?",
                       (field_name, user_name)
                       )
        
    def delete_entity_obj(self,entity):
        '''
            удаление объекта Entity из базы
        '''
        
        connect=sqlite.connect(self._repo_path)
        
        id_entity = self.__delete_entity(connect, entity.file_path)
        #list_tag_name = 
        self.__delete_entity_tags(connect, id_entity, entity.get_tag_attributes())
#        if not list_tag_name == []:
#            for tag_name in list_tag_name:
#                entity.delete_tag(tag_name)
        #list_field_name = 
        self.__delete_entity_fields(connect, id_entity, entity.get_field_attributes())
#        if not list_field_name == []:
#            for field_name in list_field_name:
#                entity.delete_field(field_name)
#            
        connect.commit()
        
        
    def add_tags(self,entity,list_tag_attributes):
        '''
            добавление несколько тегов
        '''
        for tag_attributes in list_tag_attributes:
            self.add_tag(entity,tag_attributes[0],tag_attributes[1],tag_attributes[2],tag_attributes[3])
            
    def add_tag(self, entity,tag_name,date_create=None,description=''):
        '''
            добавление одного тега
        '''
        connect = sqlite.connect(self._repo_path)
        cursor = connect.cursor()
        
        id_file = self.__get_entity_id(cursor, entity.file_path)[0]
        print(id_file)
        self.__save_tag(cursor, id_file, [tag_name,entity.user_name,date_create,description])
        if not entity.is_tag_exist(tag_name):
            new_tag = Tag(tag_name,entity.user_name,date_create,description)
            entity.add_tag(new_tag)
            
    def add_fields(self, entity, list_field_attributes):
        '''
            добавление нескольких полей
        '''
        for field_attributes in list_field_attributes:
            self.add_field(entity, field_attributes[0][0], field_attributes[0][1], field_attributes[1][0], field_attributes[0][2], field_attributes[0][3])

    def add_field(self,entity, field_name,field_value,field_value_type,date_create=None,description=''):
        '''
            добавление поля
        '''
        connect = sqlite.connect(self._repo_path)
        cursor = connect.cursor()
        
        id_file = self.__get_entity_id(cursor, entity.file_path)[0]
        self.__save_field(cursor, id_file, [[field_name,entity.user_name,field_value_type,date_create,description],[field_value]])
        if not entity.is_field_exist(field_name):
            new_field = Field(field_name,entity.user_name,field_value,field_value_type,date_create,description)
            entity.add_field(new_field)
            
        
    def find_entityes(self, request):
        '''
            поиск обеъктов Entity в хранилище
        '''
        
        connect = sqlite.connect(self._repo_path)
        cursor = connect.cursor()
        cursor.execute(request)
        
        result = cursor.fetchall()
        print(result)
        return result
    
    def modifired_entity(self,old_entity,new_entity):
        '''
            модификация объекта Entity
        '''
        pass
    
    
    
if __name__ == '__main__':
    
    repo_path = '/tmp/tmp/'


    tags = ['tag1','tag2']
    fields = ['field1']
    user_name = 'user1'
    file_path = 'path_file777'
    
    
    Ent = Entity(file_path,user_name)
    #Ent.add_field('field1', 'value1','type1')
    #Ent.add_tag('tag1')
    
    #Ent.add_field('field2', 'value2','type2')
    #Ent.add_tag('tag2')
    #Ent.add_field('field3', 'value3','type3')
    #Ent.add_tag('tag3')    
    
    
    EntMan = EntityManager(repo_path)
    EntMan.save_entity_obj(Ent)
    
    EntMan.add_tag(Ent, 'tag111')
    EntMan.add_tag(Ent,'tag222')
    EntMan.add_tag(Ent,'tag333')
    
    EntMan.add_field(Ent,'field1','value1','string')
    EntMan.add_field(Ent,'field2','value2','string')
    EntMan.add_field(Ent,'field3','value3','numeric')
#    EntMan.tmp_insert_func('file_path1')
#    EntMan.tmp_insert_func('file_path2')
#    EntMan.tmp_insert_func('file_path3')
#    
    EntMan.save_entity_obj(Ent)
    #users='valexl'
#    print('the  all entity ')
#    EntMan.tmp_select_entity(users)   
#    print('the all tag')
#    EntMan.tmp_select_all_tag()
#    print('the all entity_tags')
#    EntMan.tmp_select_all_entitytag()
#    print('the all fields')
#    EntMan.tmp_select_all_fields()
#    print('the all entity_fields')
#    EntMan.tmp_select_all_entityfield()  
    Ent = EntMan.load_entity_obj(file_path, user_name)
    for tags in Ent.get_tag_attributes():
        print(tags)
    for fields in Ent.get_field_attributes():
        print(fields)
    EntMan.delete_entity_obj(Ent)
#    
#    print('the  entity after deleting')
#    EntMan.tmp_select_entity(users)
##    print('the all entity_tags after deleting')
##    EntMan.tmp_select_all_entitytag()
##    print('the all tag after deleting')
##    EntMan.tmp_select_all_tag()
#    print('the all fields after deleting')
#    EntMan.tmp_select_all_fields()
#    print('the all entity_fields after deleting')
#    EntMan.tmp_select_all_entityfield()  
