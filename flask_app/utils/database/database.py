import mysql.connector
import glob
import json
import csv
from io import StringIO
import itertools
import hashlib
import os
import cryptography
from cryptography.fernet import Fernet
from math import pow

class database:

    def __init__(self, purge = False):

        # Grab information from the configuration file
        self.database       = 'db'
        self.host           = '127.0.0.1'
        self.user           = 'master'
        self.port           = 3306
        self.password       = 'master'
        self.tables         = ['institutions', 'positions', 'experiences', 'skills','feedback', 'users']
        
        # NEW IN HW 3-----------------------------------------------------------------
        self.encryption     =  {   'oneway': {'salt' : b'averysaltysailortookalongwalkoffashortbridge',
                                                 'n' : int(pow(2,5)),
                                                 'r' : 9,
                                                 'p' : 1
                                             },
                                'reversible': { 'key' : '7pK_fnSKIjZKuv_Gwc--sZEMKn2zc8VvD6zS96XcNHE='}
                                }
        #-----------------------------------------------------------------------------

    def query(self, query = "SELECT * FROM users", parameters = None):

        cnx = mysql.connector.connect(host     = self.host,
                                      user     = self.user,
                                      password = self.password,
                                      port     = self.port,
                                      database = self.database,
                                      charset  = 'latin1'
                                     )


        if parameters is not None:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query, parameters)
        else:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query)

        # Fetch one result
        row = cur.fetchall()
        cnx.commit()

        if "INSERT" in query:
            cur.execute("SELECT LAST_INSERT_ID()")
            row = cur.fetchall()
            cnx.commit()
        cur.close()
        cnx.close()
        return row

    def createTables(self, purge=False, data_path = 'flask_app/database/'):
        ''' FILL ME IN WITH CODE THAT CREATES YOUR DATABASE TABLES.'''

        #should be in order or creation - this matters if you are using forign keys.
         
        if purge:
            for table in self.tables[::-1]:
                self.query(f"""DROP TABLE IF EXISTS {table}""")
            
        # Execute all SQL queries in the /database/create_tables directory.
        for table in self.tables:
            
            #Create each table using the .sql file in /database/create_tables directory.
            with open(data_path + f"create_tables/{table}.sql") as read_file:
                create_statement = read_file.read()
            self.query(create_statement)

            # Import the initial data
            try:
                params = []
                with open(data_path + f"initial_data/{table}.csv") as read_file:
                    scsv = read_file.read()            
                for row in csv.reader(StringIO(scsv), delimiter=','):
                    params.append(row)
            
                # Insert the data
                cols = params[0]; params = params[1:] 
                self.insertRows(table = table,  columns = cols, parameters = params)
            except:
                print('no initial data')

    def insertRows(self, table='table', columns=['x','y'], parameters=[['v11','v12'],['v21','v22']]):
        
        # Check if there are multiple rows present in the parameters
        has_multiple_rows = any(isinstance(el, list) for el in parameters)
        keys, values      = ','.join(columns), ','.join(['%s' for x in columns])
        
        # Construct the query we will execute to insert the row(s)
        query = f"""INSERT IGNORE INTO {table} ({keys}) VALUES """
        if has_multiple_rows:
            for p in parameters:
                query += f"""({values}),"""
            query     = query[:-1] 
            parameters = list(itertools.chain(*parameters))
        else:
            query += f"""({values}) """                      
        
        insert_id = self.query(query,parameters)[0]['LAST_INSERT_ID()']         
        return insert_id
    
    def GetFeedback(self):
        feedback = self.query("""SELECT * FROM `feedback`""")
        total = {}
        for i in range(len(feedback)):
            total[i] = feedback[i]
        return total
    
    def getResumeData(self):
        # Pulls data from the database to genereate data like this:
        #print("yo")
        resume = {}
        institutions = self.query("""SELECT * FROM `institutions`""")
        positions = self.query("""SELECT * FROM `positions`""")
        experiences = self.query("""SELECT * FROM `experiences`""")
        skills = self.query("""SELECT * FROM `skills`""")
        count = 1
        for i in range(len(institutions)):
            institutions[i]['positions'] = {}
            for j in range(len(positions)):
                if positions[j]['inst_id'] == institutions[i]['inst_id']:
                    institutions[i]['positions'][positions[j]['position_id']] = positions[j]
                    institutions[i]['positions'][positions[j]['position_id']]['experiences'] = {}
                    for k in range(len(experiences)):
                        if institutions[i]['positions'][positions[j]['position_id']]['position_id'] == experiences[k]['position_id']:
                            institutions[i]['positions'][positions[j]['position_id']]['experiences'][experiences[k]['experience_id']] = experiences[k]
                            institutions[i]['positions'][positions[j]['position_id']]['experiences'][experiences[k]['experience_id']]['skills'] = {}
                            for l in range(len(skills)):
                                if institutions[i]['positions'][positions[j]['position_id']]['experiences'][experiences[k]['experience_id']]['experience_id'] == skills[l]['experience_id']:
                                    institutions[i]['positions'][positions[j]['position_id']]['experiences'][experiences[k]['experience_id']]['skills'][skills[l]['skill_id']] = skills[l]



            resume[i+1] = institutions[i]
            count += 1
        #print(resume)
        return resume  

#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################
    def createUser(self, email='me@email.com', password='password', role='user'):        
        try:
            query = f"""
                    SELECT email
                    FROM `users`
                    WHERE email = \'{email}\';
                    """
            exists = self.query(query)
            if exists:
                print('Creation Failed: Already Exists')
                return  {'success' : 0}
            encrypted_Pass = self.onewayEncrypt(password)
            parameters = [[role,email,encrypted_Pass]]
            columns = ['role','email','password']
            self.insertRows('users', columns, parameters)
            print('Creation Success')
            return {'success': 1}
        except:
            print('Creation Failed: Bad Request')
            return {'success' : 0}

    def authenticate(self, email='me@email.com', password='password'):
        encrypted_pass = self.onewayEncrypt(password)
        encrypted_email = self.onewayEncrypt(email)
        query = f"""
                    SELECT email
                    FROM `users`
                    WHERE email = \'{email}\'
                    AND password = \'{encrypted_pass}\';
                    """
        exists = self.query(query)
        if exists:
            print('Login Success')
            return {'success': 1}
        else:
            print('Login Failed')
            return {'success' : 0}

    def isOwner(self, email='me@email.com'):
        encrypted_email = self.onewayEncrypt(email)
        query = f"""
                    SELECT email
                    FROM `users`
                    WHERE email = \'{email}\'
                    AND role = 'owner';
                    """
        exists = self.query(query)
        if exists:
            return True
        else:
            return False

    def onewayEncrypt(self, string):
        encrypted_string = hashlib.scrypt(string.encode('utf-8'),
                                          salt = self.encryption['oneway']['salt'],
                                          n    = self.encryption['oneway']['n'],
                                          r    = self.encryption['oneway']['r'],
                                          p    = self.encryption['oneway']['p']
                                          ).hex()
        return encrypted_string


    def reversibleEncrypt(self, type, message):
        fernet = Fernet(self.encryption['reversible']['key'])
        
        if type == 'encrypt':
            message = fernet.encrypt(message.encode())
        elif type == 'decrypt':
            message = fernet.decrypt(message).decode()

        return message


