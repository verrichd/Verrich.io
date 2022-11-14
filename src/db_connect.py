from configparser import ConfigParser

from psycopg import Connection, connect
from psycopg.conninfo import make_conninfo


class Connector:
    
    def __init__(self, host:str=None,
                 port:int=None,user:str=None,
                 password:str=None,dbname:str=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.dbname = dbname
    
    def config_connect(self, path:str, section:str, **kwargs) -> Connection:
        credentials = {}
        parser = ConfigParser()
        
        parser.read(path)
        if parser.has_section(section):
            params = parser.items(section)
            for k,v in params:
                credentials[k] = v

        conn = connect(conninfo=make_conninfo(**credentials),**kwargs)
                
        conn._check_connection_ok()
        print(conn.ConnStatus)
        return conn