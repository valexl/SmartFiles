'''
Created on 18.05.2010

@author: valexl
'''

class MyClass(object):
    '''
    Класс с функциями которые могут еще пригодиться
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
 
 
 
 
         
    def splitDirPath(parent_dir,file_path):
        split_repodir_path = parent_dir.split(os.sep)
        split_file_path = file_path.split(os.sep)
        index = 0
        result_file_path =os.sep
        for dir_name in split_repodir_path:
            if not dir_name==split_file_path[index]:
                
                while index<len(split_file_path):
                    print(index,'=',result_file_path)
                    result_file_path += split_file_path[index] + os.sep
                    index+=1
                
                return result_file_path
            index +=1
    
