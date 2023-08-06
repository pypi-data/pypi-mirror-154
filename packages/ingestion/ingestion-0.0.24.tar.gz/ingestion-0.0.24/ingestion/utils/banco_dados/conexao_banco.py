import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import mysql.connector
import os
from sqlalchemy import create_engine

class ConexaoBanco():

    def __init__(self):
            
        self.connection = None
        self.conn = None
        self.user="admin_iot@pro-iotbd-mysql"
        self.password="Tivit!010"   
        self.database="iotbd"
        self.host="pro-iotbd-mysql.mysql.database.azure.com"
        self.port=3306
        self.ssl_verify_cert=True

        self.ssl_ca= os.getcwd() + "\\cargas\\ingestao\\utils\\banco_dados\\ssl_ca_file\\iotbd.crt.pem"

        self.db_url = f'mysql+mysqlconnector://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}'

        self.ssl_args = {'ssl_ca': self.ssl_ca,
                          'ssl_verify_cert': self.ssl_verify_cert
                         }
      
    def get_connection(self): 

        try:
            if( self.connection == None ):
                self.connection = create_engine(self.db_url, connect_args=self.ssl_args, isolation_level="AUTOCOMMIT")
                print("Database connection!")
        except mysql.connector.Error as error:
            if error.errno == errorcode.ER_BAD_DB_ERROR:
                print(f"Database doesn't exist {error}")
            elif error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print(f"User name or password is wrong {error}")
            else:
                print(error)

    def close_connection(self):
    
        if( self.conn != None ):
            self.conn.close()
            print(f"Close com o data base")

    def insert(self, df, table, if_exists, chunksize=None):

        if(if_exists == 'replace' or if_exists == 'truncate'):
            print(f"Foi solicitado a inserção na tabela como truncate, pelo paramentro {if_exists}")
            self.truncate(table)

        self.get_connection()
        with self.connection.begin() as conn:
            
            if chunksize == None:
                df.to_sql(name=table, con=conn, if_exists='append', index=False )
            else:
                df.to_sql(name=table, con=conn, if_exists='append', index=False , chunksize=chunksize)
            #conn.close()
            self.conn = conn
            print(f"Dados salvos com sucesso na tabela {table}")


    def truncate(self, table):
        self.get_connection()
        with self.connection.begin() as conn:
            _pd = self.select(f"SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table}'")
            if len(_pd) > 0:
                conn.execution_options(autocommit=True).execute(f"truncate table {table}")
            #conn.close()
            self.conn = conn

    def select(self, query) -> pd.DataFrame:
        self.get_connection()
        with self.connection.begin() as conn:
            result = pd.read_sql(query,conn)
            #conn.close()
            self.conn = conn
            return result



if __name__ == '__main__':
    conexaoBanco = ConexaoBanco()
    #conexaoBanco.get_connection()
    #d = { 'nome': ['nome_1', 'nome_2'], 'email': ['email_1', 'email_2']}
    #name_table = 'teste'
    #conexaoBanco.insert(pd.DataFrame(data=d),name_table)
    #pd_ = conexaoBanco.select("select codigo, nome from iotbd.teste")

    #conexaoBanco.teste()

    #print( pd_ )

    d = conexaoBanco.select('select id_cliente, documento from CLIENTE')

    print(d)
