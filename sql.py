import sqlite3 
import os
import io

class DB():
    def __init__(self):
        self.name = 'data.db'
        self.exists = False
        if os.path.isfile(self.name):
            self.exists = True
        self.pedidos = "(client_id)"

    def initDB(self):
        self.connection = sqlite3.connect(self.name) 
        self.crsr = self.connection.cursor() 
        if not self.exists:
            sql_command = """CREATE TABLE impressoras (  
                                impressora_id INTEGER PRIMARY KEY,  
                                impressora_nome VARCHAR(15)
                                );"""
                            
            # execute the statement 
            self.crsr.execute(sql_command) 

            sql_command = """CREATE TABLE manutencao (  
                                impressora_id INTEGER,  
                                man_inicio DATE,
                                man_fim DATE,
                                FOREIGN KEY(impressora_id) REFERENCES impressoras(impressora_id)
                                );"""
                            
            # execute the statement 
            self.crsr.execute(sql_command) 


            # SQL command to create a table in the database 
            sql_command = """CREATE TABLE pecas (  
                                peca_id INTEGER PRIMARY KEY,  
                                peca_nome VARCHAR(30),
                                n_orcamento INTEGER,
                                material VARCHAR(5),
                                qualidade VARCHAR(5),
                                tempo_de_impressao REAL,
                                finalizada BOOLEAN,
                                massa REAL);"""
                            
            # execute the statement 
            self.crsr.execute(sql_command) 
            
            sql_command = """CREATE TABLE colaboradores (  
                                colaborador_id INTEGER PRIMARY KEY,  
                                colaborador_nome VARCHAR(20) ,
                                colaborador_contato VARCHAR(30),
                                colaborador_associacao VARCHAR(20),
                                colaborador_data_associacao DATE,
                                colaborador_data_desassociacao DATE);"""
                            
           
            self.crsr.execute(sql_command) 
            
            sql_command = """CREATE TABLE clientes (  
                                cliente_id INTEGER PRIMARY KEY,  
                                cliente_nome VARCHAR(20) ,
                                cliente_contato VARCHAR(30),
                                cliente_data_de_contato DATE);"""
                            
           
            self.crsr.execute(sql_command) 
            sql_command = """CREATE TABLE pedidos (  
                                n_orcamento INTEGER PRIMARY KEY,  
                                cliente_id INTEGER,
                                coladorador_id INTEGER,
                                origem VARCHAR(5),  
                                data_pedido DATE,
                                data_deadline DATE,
                                preco REAL,
                                finalizada BOOLEAN,
                                FOREIGN KEY(cliente_id) REFERENCES clientes(cliente_id),  
                                FOREIGN KEY(coladorador_id) REFERENCES colaboradores(colaborador_id)
                                );"""
                            
            
            self.crsr.execute(sql_command) 
            #save
            self.connection.commit()

    def insertInDB(self, tableName, data):
        #TODO: insert name of table
        aux = """ VALUES ("""
        for i in range(len(data)):
            if i != len(data)-1:
                aux = aux + """?,"""
            else:
                aux = aux + """?)"""

        command = """INSERT INTO """  + tableName + aux 
        self.crsr.execute(command, data)
        self.connection.commit()
    
    def search(self, datas, tables, conditions='', modifiers=''):
        command = "SELECT {0} FROM {1}".format(datas, tables)
        if conditions != '':
            command = command + " WHERE {0}".format(conditions)
        if modifiers != '':
            command = command + " {0}".format(modifiers)
        #self.crsr.execute("SELECT * FROM impressoras")        
        self.crsr.execute(command)
        rows = self.crsr.fetchall()
        print(rows)
    
    

    def createBackup(self):
        with io.open('db.bu', 'w') as f:
            for linha in self.connection.iterdump():
                f.write('%s\n' % linha)
    
if __name__ == "__main__":
    db = DB()
    db.initDB()
    #db.insertInDB('impressoras',(1,'bla'))
    db.search('*', 'impressoras', "impressora_id=1")
