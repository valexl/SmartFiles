'''
Created on 15.05.2010

@author: valexl
'''
import os
class SystemInfo(object):
    metadata_dir_name = '.metadata'
    metadata_file_name = os.path.join(metadata_dir_name,'data_base.bd')
    
    #repo_files_info = os.path.join(metadata_dir_name,'repo_files.bd')
    entity_file_type = 'file'
    entity_link_type = 'url'
    field_type_int = 'integer'
    field_type_str = 'string'
    user_type_admin='admin'
    user_type_other='user'     

    home_dir = "/tmp"#'/home/smart_files/.metdata/'
    file_user_info = os.path.join(metadata_dir_name,'data_base.bd')
    
    neural_net_file_path = os.path.join(metadata_dir_name,'neural_net.sm') 
    
    
if __name__=='__main__':
    home_dir = '~'
    file='tmp'
    
    file_path = os.path.join(home_dir,file)
    print(file_path)
    os.mkdir(home_dir + os.path.sep + file)
    
    
    