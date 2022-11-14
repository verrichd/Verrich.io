
from abc import ABCMeta
from abc import abstractclassmethod
from psycopg2 import connect


class Task():
    def run(self):
        return
    
class createConnection(Task) :
    def __init__(self):
       self.run()
        
    def run(**params):
        connect(params)
        
class createTable(Task):
    def __init__(self, dbName:str, tblName:str, creds:dict):
        print("createTable() Not yet implemented")
        return
    
class createSchema(Task):
    def __init__(self):
        print("createSchema() not yet implemented")
        return

class createWarehouse(Task):
    def __init__(self):
        print("createWarehouse() not yet implemented")
        return