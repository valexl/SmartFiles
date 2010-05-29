'''
Created on 18.05.2010

@author: valexl
'''

class MyClass(object):
    '''
    classdocs
    '''


    def __init__(selfparams):
        '''
        Constructor
        '''
        
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
 
