'''
Created on 15.05.2010

@author: valexl
'''
import os
import subprocess
import sys

class SystemInfo(object):
    '''
        статический класс содержащий не изменные
    '''
    metadata_dir_name = '.metadata'
    metadata_file_name = os.path.join(metadata_dir_name,'data_base.bd')
    
    
    entity_file_type = 'file'
    entity_link_type = 'url'
    field_type_int = 'integer'
    field_type_str = 'string'
    user_type_admin='admin'
    user_type_other='user'     

    home_dir = "/tmp/smart_files"
    file_user_info = 'data_base.bd'
    
    last_repo_info = 'last_repo.info'
    
    
    neural_net_file_path = os.path.join(metadata_dir_name,'neural_net.sm') 
    

if __name__=='__main__':
    home_dir = sys.prefix
    print(sys.prefix)
    file=os.path.join(home_dir,'ПЛАН НА ДЕНЬ.odt')
#    
#    file_path = os.path.join(home_dir,file)
#    print(file_path)
    command = 'xdg-open'
    subprocess.call([command, file])

    
    