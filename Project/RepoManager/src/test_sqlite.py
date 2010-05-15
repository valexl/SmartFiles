'''
Created on 15.05.2010

@author: vlkv
'''
import sqlite3

if __name__ == '__main__':
    
    repoDB = sqlite3.connect('/tmp/test_sqlite.db')
    cursor = repoDB.cursor()
#    cursor.execute("CREATE TABLE users ( "
#            " name VARCHAR2(255) NOT NULL PRIMARY KEY, "
#            " password INTEGER, "
#            " description VARCHAR2(255), "
#            " date_create TIMESTAMP) ")
#    repoDB.commit()
    
    cursor.execute(" INSERT INTO users "
                " (name, description) "
                " VALUES (?, ?) ",
                ('usr2','descr'))
    
    repoDB.commit()
        