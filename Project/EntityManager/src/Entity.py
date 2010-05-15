'''
Created on 20.04.2010

@author: valexl
'''
from Tag import Tag
from Field import Field
class Entity(object):
    '''
    Класс "Сущность". 
    '''    

    def __init__(self, title, entity_type, user_name, list_tags=[], list_fields=[], 
                 file_path=None, file_size=0, file_date_modifired=None, file_hash=None, 
                 notes='', date_created=None, id=None):
        '''
        Constructor
        '''
        
        self.id = id
        self.file_path = file_path
        self.file_size = file_size
        self.file_date_modifired = file_date_modifired
        
        self.list_tags = list_tags
        self.list_fields = list_fields
        self.user_name = user_name
   
        
#    def add_tag (self,tag_name,tag_date_created='NONE',tag_description=''):
#        '''
#            пометка сущности новым тегом
#        '''
#        
#        new_tag = Tag(tag_name,self.user_name,tag_date_created,tag_description)
#        self.list_tags.append(new_tag)
#        
    def add_tag (self,tag):
        '''
            пометка сущности тегом
        '''
        self.list_tags.append(tag)

    def delete_tag(self,tag_name):
        '''
            тег отделяется от объекта entity
        '''
        index = 0
        for tag in self.list_tags:
            if tag.name == tag_name:
                break
            index+=1
        if index <= len(self.list_tags):
            self.list_tags.pop(index)
                
        
        
    def is_tag_exist(self,tag_name):
        '''
            помечен ли данным тегом объект entity
        '''
        for tag in self.list_tags:
            if tag.name == tag_name:
                return 1
        return 0 
    
    
#    def add_field (self, field_name,field_value,type_value,field_date_create='NONE',field_description=''):
#        '''
#            пометка полем сущности
#        '''
#        new_field = Field(field_name,self.user_name,field_value,type_value,field_date_create,field_description)
#        self.list_fields.append(new_field)
    def add_field(self,field):
        '''
            пометка полем сущности
        '''
        self.list_fields.append(field)
    def delete_field(self,field_name):
        '''
            особождает объект entity от данного поля
        '''
        index = 0
        for field in self.list_fields:
            if field.name == field_name:
                break
            index+=1
        if index <= len(self.list_fields):
            self.list_fields.pop(index)
        
    def is_field_exist(self,field_name):
        '''
            помечен ли данным полем объект entity
        '''
        for field in self.list_fields:
            if field.name == field_name:
                return 1
        return 0

    
    def get_tag_attributes(self):
        '''
            возращает список списков атрибутов тегов, помечающих данный объект entity
        '''
        result_list = []
        for tag in self.list_tags:
            #print(tag)
            result_list.append(tag.get_attirbutes())
        return result_list
        
        
    def get_field_attributes(self):
        '''
            возращает список списоков атрибутов полей, помечающих данный объект entity
        '''
        result_list = []
        for field in self.list_fields:
            result_list.append(field.get_attributes())
        return result_list
    
    
    
        
#if __name__ == "__main__":
#    
#    tags = []
#    fields = []
#    users = 'user1'
#    name = 'entity_by_user'
#    
#    
#    #Ent = Entity(name,tags,fields,users)
#    Ent=''
#    Ent = Entity(name,users,tags,fields)
#    Ent.add_field('field1', 'value1','type1')
#    Ent.add_tag('tag1')
#    Ent.add_field('field2', 'value2','type2')
#    Ent.add_tag('tag2')
#    Ent.add_field('field3', 'value3','type3')
#    Ent.add_tag('tag3')
#    
#    print('the field attributes is -')
#    Ent.get_field_attributes()
#    
#    print('the tags attributes is - ')
#    Ent.get_tag_attributes()
#    

    
#    
#    print('ent.name=',Ent.file_path)
#    print('ent_tag=',Ent.list_tags)
#    print('ent_tag[2].tag_name=',Ent.list_tags[2].tag_name)
#    print('ent_tag[2].tag_user=',Ent.list_tags[2].tag_user_name)
#    print('ent_fields=',Ent.list_fields)
#    print('ent_users=',Ent.user_name)
#    
    