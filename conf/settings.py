import os
from os.path import join, dirname
from dotenv import load_dotenv

import psycopg2
 
dotenv_path = join(dirname(__file__), 'prod.env')
load_dotenv(dotenv_path)
 
# Accessing variables.
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASS')

 

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:        
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host=db_host,database=db_name, user=db_user, password=db_password)
 
        # create a cursor
        cur = conn.cursor()
        
        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
 
        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        print('Data Sample:')
        cur.execute('SELECT * from base_models.customer')
        test = cur.fetchall()
        print(test)
       
     # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
 
 
if __name__ == '__main__':
    connect()