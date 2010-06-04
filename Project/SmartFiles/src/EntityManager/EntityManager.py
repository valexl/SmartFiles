'''
Created on 20.04.2010

@author: valexl
'''
import sqlite3 as sqlite
import os
from RepoManager.SystemInfo import SystemInfo
from EntityManager.Entity import Entity
from EntityManager.Tag import Tag
from EntityManager.Field import Field


class EntityManager(object):
    '''
        Класс управление сущностью.
    '''
    class ExceptionEntityManager(Exception):
        pass
    class ExceptionNotFoundFileBD(ExceptionEntityManager):
        pass
    class ExceptionEntityIsExist(ExceptionEntityManager):
        pass
    
    def __init__(self,repo_path):
        '''
           конструктор класса. Регестрирует EntityManager в конкретном хранилище
        '''
        self._repo_path = repo_path
    
    
    
        
        
        
    @staticmethod      
    def createEntity(entity_type, user_name,title='', file_path=None, list_tags=[], list_fields=[], 
                 file_size=0, file_date_modifired=None, file_hash=None, 
                 notes='', date_created=None, id=None):
        '''
            создание нового объекта класса Entity
        '''
        
        obj_entity = Entity(title, entity_type, user_name, file_path,list_tags, list_fields,file_size,
                            file_date_modifired,file_hash,notes,date_created,id)
#        print('obj_entity',obj_entity)
#        print('obj_entity.file_path',obj_entity.file_path)
        return obj_entity
        
 
        
     
    @staticmethod
    def __saveEntity(cursor,entity):
        '''
            сохранить объект в entity. Если такой объект сущесвтует, то перезапись и возращается флаг 0.
            если такого объекта нет, то записывается новый и возращается флаг 1
        '''
        
   
        if entity.id == None:
            if not entity.file_path == None:
                cursor.execute(' SELECT COUNT (*) FROM entity WHERE '
                               ' file_path = ? ',
                               (entity.file_path,) 
                               )
                if cursor.fetchone()[0]>0:
                    raise EntityManager.ExceptionEntityIsExist('косарезик. такой файл уже присвоин кому то')
            cursor.execute("INSERT INTO entity"
                           "(title, object_type, user_name, file_path, file_size, file_hash, date_create,notes )"
                           "VALUES(?,?,?,?,?,?,?,?)",
                          (entity.title, entity.object_type, entity.user_name,
                           entity.file_path,entity.file_size, entity.file_hash,entity.date_create,entity.notes))
            entity.id = cursor.lastrowid
        #если объект существует, то его модификация  
        else:
           cursor.execute(" UPDATE  entity "
                          " SET title = ?, object_type = ?, user_name = ?,  file_size = ?, file_hash =?, notes = ?"
                          " WHERE id= ?",
                          (entity.title, entity.object_type, entity.user_name,  entity.file_size, entity.file_hash, entity.notes, entity.id)
                          )
           
                  
    @staticmethod
    def __saveTag(cursor,entity_id,tag_attributes):
        '''
            сохранить тег в таблице tag  
        '''
        cursor.execute("SELECT COUNT (*) FROM tag "
                       " WHERE name = ? AND user_name = ? ",
                       (tag_attributes[0],tag_attributes[1])
                       )
        if cursor.fetchone()[0]==0:
            print('add tag')
            #добавление новой записи
            #сохранение в таблице tag
            cursor.execute("INSERT INTO tag "
                           "(name,user_name,description,date_create)"
                           "VALUES (?,?,?,?)",
                            tag_attributes  
                          )
        else: # модификация существующей записи
            print('tag is exist')
            print('do nothing')
            
        
            
            
    @staticmethod
    def __saveEntityTags(cursor,entity_id,tag_name,user_name):
        '''
            сохранение в таблице entity_tag
        '''
        cursor.execute("SELECT COUNT(*) FROM entity_tags "
                       " WHERE tag_name = ? AND user_name = ? AND entity_id = ? ",
                       (tag_name,user_name,entity_id)
                       )
        if cursor.fetchone()[0]==0:
            cursor.execute("INSERT INTO entity_tags "
                                   "(entity_id,tag_name,user_name)"
                                   "VALUES(?,?,?)",
                                   (entity_id,tag_name, user_name)
                                   )
        else:
            print('entity_tags record is exist')
            print('do nothing')
    
    @staticmethod
    def __saveField(cursor,entity_id,field_attributes):

        print('__saveField')
        cursor.execute("SELECT COUNT(*) FROM field "
                       " WHERE name = ? AND user_name = ? ",
                       (field_attributes[0][0],field_attributes[0][1])
                       )
        count = cursor.fetchone()[0]
        print('count of field is - ',count)
        if count ==0: 
            #добавление новой записи
            # запись в field
            print(field_attributes)
            cursor.execute("INSERT INTO field"
                            "(name,user_name,value_type,description,date_create)"
                            "VALUES(?,?,?,?,?)",
                            field_attributes[0]
            )    
        
        else: #модификация
            print('field is exist')
            print('do nothing')
        
            
    @staticmethod
    def __saveEntityFields(cursor,entity_id,field_name,user_name,value):
        '''
            запись в entity_fields
        '''
        print('YESSSSSSSSSSSSSS __saveENTITYFIELds!!!!!!!!!!!!!!!!!11')
        cursor.execute("SELECT COUNT(*) FROM entity_fields "
                       " WHERE field_name = ? AND user_name = ? AND entity_id = ? ",
                       (field_name,user_name ,entity_id)
                       )
        count =cursor.fetchone()[0] 
        if count ==0:
        # запись в entity_fields
            cursor.execute("INSERT INTO entity_fields"
                            "(entity_id,field_name,user_name,value)"
                            "VALUES(?,?,?,?)",
                            (entity_id,field_name,user_name, value)
            )
        else:
            print(count)
    
         
             
    def saveEntity(self,entity):
        '''
            запись entity в базу данных
        '''

        path_metadata_file = os.path.join(self._repo_path, SystemInfo.metadata_file_name)
        if os.path.exists(path_metadata_file):
            connect=sqlite.connect(path_metadata_file)
            cursor = connect.cursor()
            # запись entity
            EntityManager.__saveEntity(cursor, entity)

            # запись tag   
           
            for tag_attributes in entity.getTagAttributes():    
                EntityManager.__saveTag(cursor, entity.id,tag_attributes)
                                                                    #имя тега        #имя пользователя
                EntityManager.__saveEntityTags(cursor, entity.id, tag_attributes[0], tag_attributes[1])
            
                # запись field
            for field_attributes in entity.getFieldAttributes():
     #               print('вот вот начнется saveField')
                    EntityManager.__saveField(cursor, entity.id, field_attributes)
                                                                        #имя поля                
                    EntityManager.__saveEntityFields(cursor, entity.id, field_attributes[0][0], 
                                                        #имя пользователя        #значение
                                                     field_attributes[0][1], field_attributes[1][0])
            connect.commit()
        else:
            raise EntityManager.ExceptionNotFoundFileBD('saveEntity. "Не найден файл с метаданными - '+ path_metadata_file +'"')
        
            
    @staticmethod
    def __getListTags(cursor,entity_id,user_name):
        '''
            получить список тегов для entity
        '''
        list_tags = []
    
        cursor.execute("SELECT tag.* FROM tag "
                       "INNER JOIN (entity_tags INNER JOIN " 
                       " entity ON entity.id = entity_tags.entity_id AND entity.id = ? "
                       " AND entity.user_name = entity_tags.user_name) AS t1"
                       " ON t1.user_name = tag.user_name AND t1.tag_name = tag.name ",
                       (entity_id,)
                       )
        
        
        for tag_attributes in cursor.fetchall():
            list_tags.append(Tag(tag_attributes[0],tag_attributes[1],tag_attributes[2],tag_attributes[3]))
        return list_tags
        
    @staticmethod
    def __getListFields(cursor,entity_id,user_name):
        '''
            получить список полей для entity
        '''
        list_fields = []
        
       # print(entity_id)
        
        cursor.execute(" SELECT field.name, field.user_name, t1.value, field.value_type, " 
                       " field.date_create,field.description "
                       " FROM field "
                       " INNER JOIN (entity_fields INNER JOIN " 
                       " entity ON entity.id = entity_fields.entity_id AND entity.id = ? "
                       " AND entity.user_name = entity_fields.user_name) AS t1"
                       " ON t1.user_name = field.user_name AND t1.field_name = field.name ",
                       (entity_id,)
                       )
        
        
        for field_attributes in cursor.fetchall():
            list_fields.append(Field(field_attributes[0],field_attributes[1],field_attributes[2],field_attributes[3],field_attributes[4],field_attributes[5]))
#        print(cursor.fetchall())
        return list_fields
        
    def loadEntityObj(self,entity_id):
        path_metadata_file = os.path.join(self._repo_path,SystemInfo.metadata_file_name)
        if os.path.exists(path_metadata_file):
            connect = sqlite.connect(path_metadata_file)
            cursor = connect.cursor()
            
            cursor.execute("SELECT title, object_type, user_name, file_path FROM entity "
                           " WHERE id = ? ",
                           (entity_id,)
                           )
            entity_record = cursor.fetchone()
            print('loadEntityObj', entity_record)
            tags = EntityManager.__getListTags(cursor,entity_id, entity_record[2])
            fields = EntityManager.__getListFields(cursor, entity_id, entity_record[2])
            print('loadEntityObj',entity_id)
            
            entity = Entity(entity_record[0], entity_record[1],entity_record[2], entity_record[3], tags, fields, id = entity_id)     
            return entity
        else:
            raise EntityManager.ExceptionNotFoundFileBD('loadEntityObj не найден файл с метаданными '+ path_metadata_file)    
    @staticmethod   
    def __deleteEntity(cursor,id_entity):
        '''
            удаляет запись из enity и возращает id
        '''
        
        cursor.execute("DELETE FROM entity "
                       "WHERE id=?",
                       (id_entity,)
                       )
     
    @staticmethod
    def __deleteEntityTags(cursor,id_entity,tag_attributes):
        '''
            удаляютСя записи из entity_tags.
        '''
        
        cursor.execute("DELETE FROM entity_tags "
                       "WHERE entity_id = ? AND tag_name = ? AND user_name = ? ",
                       (id_entity,tag_attributes[0],tag_attributes[1])
                       )
      
      
    @staticmethod
    def __deleteTag(cursor,tag_name,user_name):
        '''
            удаление тега из базы
        '''
        cursor.execute("DELETE FROM tag "
                       "WHERE name=? AND user_name = ?",
                       (tag_name, user_name)
                       )
    def deleteTag(self,tag):
        '''
            удаление тега и всех записей связанных с ним в entity_tags
        '''
        path_metadata_file = os.path.join(self._repo_path,SystemInfo.metadata_file_name)
        if os.path.exists(path_metadata_file):
            connect=sqlite.connect(path_metadata_file)
            cursor = connect.cursor()
            EntityManager.__deleteTag(cursor, tag.name, tag.user_name)
            cursor.execute(" SELECT entity_id FROM entity_tags "
                           " WHERE tag_name = ? AND user_name = ? ",
                           (tag.name,tag.user_name)
                           )
            list_entity_id = cursor.fetchall()
            
            for entity_id in list_entity_id:
                EntityManager.__deleteEntityTags(cursor, entity_id[0], tag.getAttributes())
            EntityManager.__deleteTag(cursor, tag.name, tag.user_name)
            connect.commit()
        else:
            raise EntityManager.ExceptionNotFoundFileBD('deleteTag не найден файл с метаданными ' + path_metadata_file)
          
    def deleteField(self,field):
        '''
            удаления field и всех записей связанных с ним в entity_fields
        '''
        path_metadata_file = os.path.join(self._repo_path,SystemInfo.metadata_file_name)
        if os.path.exists(path_metadata_file):
            connect=sqlite.connect(path_metadata_file)
            cursor = connect.cursor()
            EntityManager.__deleteField(cursor, field.name, field.user_name)
            cursor.execute(" SELECT entity_id FROM entity_fields "
                           " WHERE field_name = ? AND user_name = ? ",
                           (field.name,field.user_name)
                           )
            list_entity_id = cursor.fetchall()
            for entity_id in list_entity_id:
                EntityManager.__deleteEntityFields(connect, entity_id[0], field.getAttributes())
            EntityManager.__deleteField(cursor, field.name, field.user_name)
            connect.commit()
        else:
            raise EntityManager.ExceptionNotFoundFileBD('deleteTag не найден файл с метаданными ' + path_metadata_file)
        
        
    @staticmethod    
    def __deleteEntityFields(cursor,id_entity,field_attributes):
        '''
            удаляютСя записи из entity_fields.
        '''
        cursor.execute("DELETE FROM entity_fields "
                       " WHERE entity_id = ? AND field_name = ? AND user_name = ? ",
                       (id_entity,field_attributes[0][0],field_attributes[0][1])
                       )
    
      
    @staticmethod
    def __deleteField(cursor,field_name,user_name):
        '''
            удалание поля из базы
        '''
        cursor.execute("DELETE FROM field "
                       "WHERE name=? AND user_name = ?",
                       (field_name, user_name)
                       )
        
    def deleteEntity(self,entity):
        '''
            удаление объекта Entity из базы
        '''
        path_metadata_file = os.path.join(self._repo_path,SystemInfo.metadata_file_name)
        if os.path.exists(path_metadata_file):
            connect=sqlite.connect(path_metadata_file)
            cursor = connect.cursor()
            # удаление всех записей entity_tags и при необходимости tag
            for tag_attributes in entity.getTagAttributes():
                EntityManager.__deleteEntityTags(cursor, entity.id, tag_attributes)
                cursor.execute(" SELECT COUNT(*) FROM entity_tags "
                               " WHERE tag_name = ? AND user_name = ? ",
                               (tag_attributes[0], entity.user_name) 
                               )
                if cursor.fetchone()[0] == 0:
                    EntityManager.__deleteTag(cursor, tag_attributes[0],entity.user_name)
            #удаление всех записей entity_fields и при необходимости записи из field
            for field_attributes in entity.getFieldAttributes(): 
                EntityManager.__deleteEntityFields(cursor, entity.id, field_attributes)
                cursor.execute(" SELECT COUNT(*) FROM entity_fields "
                               " WHERE field_name = ? AND user_name = ? ",
                               (field_attributes[0][0], entity.user_name) 
                               )
                if cursor.fetchone()[0] == 0:
                    EntityManager.__deleteField(cursor, field_attributes[0][0],entity.user_name)
            #удаление записи entity
            EntityManager.__deleteEntity(cursor, entity.id)
            connect.commit()
        else:
            raise EntityManager.ExceptionNotFoundFileBD('deleteEntity не найден файл с метаданными ' + path_metadata_file)
        
    def releaseEntityFromTag(self,entity,tag):
        '''
            освобождение сущности от тега
        '''
        path_metadata_file = os.path.join(self._repo_path,SystemInfo.metadata_file_name)
        if os.path.exists(path_metadata_file):
            connect=sqlite.connect(path_metadata_file)
            cursor = connect.cursor()
            self.__deleteEntityTags(cursor, entity.id, tag.getAttributes())
            connect.commit()
            cursor.execute(" SELECT count(*) FROM entity_tags "
                           " WHERE tag_name = ? AND user_name = ? ",
                           (tag.name, tag.user_name)
                           )
            
            if cursor.fetchone()[0]==0:
                self.__deleteTag(cursor, tag.name, tag.user_name)
                connect.commit()
            
        else:
            raise EntityManager.ExceptionNotFoundFileBD('deleteEntity не найден файл с метаданными ' + path_metadata_file)
    
    def releaseEntityFromField(self,entity,field):
        '''
            освобождение сущности от тега
        '''
        path_metadata_file = os.path.join(self._repo_path,SystemInfo.metadata_file_name)
        if os.path.exists(path_metadata_file):
            connect=sqlite.connect(path_metadata_file)
            cursor = connect.cursor()
            self.__deleteEntityFields(cursor, entity.id, field.getAttributes())
            connect.commit()
            cursor.execute(" SELECT count(*) FROM entity_fields "
                           " WHERE field_name = ? AND user_name = ? ",
                           (field.name, field.user_name)
                           )
            
            if cursor.fetchone()[0]==0:
                self.__deleteField(cursor, field.name, field.user_name)
                connect.commit()
            
        else:
            raise EntityManager.ExceptionNotFoundFileBD('deleteEntity не найден файл с метаданными ' + path_metadata_file)
        
    def modifiTag(self,tag):
        pass
    
            
    def markTag(self, entity,tag):
        '''
            добавление одного тега
        '''
        path_metadata_file = os.path.join(self._repo_path,SystemInfo.metadata_file_name)
        if os.path.exists(path_metadata_file):
            connect=sqlite.connect(path_metadata_file)
            cursor = connect.cursor()
            print(tag)
            atrribute = tag.getAttributes()
            self.__saveTag(cursor, entity.id, atrribute)
            self.__saveEntityTags(cursor,entity_id=entity.id,user_name=entity.user_name,tag_name=tag.name,)
            if not entity.isTagExist(tag.name):
                entity.addTag(tag)
            connect.commit()
            return entity
        else:
            raise EntityManager.ExceptionNotFoundFileBD('markTag не найден файл с метаданными ' + path_metadata_file)
            
    def modifiField(self,field):
        pass
    
    
    def addField(self,entity, field):
        '''
            добавление поля
        '''
        path_metadata_file = os.path.join(self._repo_path,SystemInfo.metadata_file_name)
        if os.path.exists(path_metadata_file):
            connect=sqlite.connect(path_metadata_file)
            cursor = connect.cursor()
            
            
            EntityManager.__saveField(cursor, entity.id, field.getAttributes())
            EntityManager.__saveEntityFields(cursor, entity.id, field.name, field.user_name, field.value)
            
            if not entity.isFieldExist(field.name):
                entity.addField(field)
            connect.commit()
        else:       
            raise EntityManager.ExceptionNotFoundFileBD('addField не найден файл с метаданными ' + path_metadata_file)
    

    
    
if __name__ == '__main__':
    
    repo_path = '/tmp/tmp/'


