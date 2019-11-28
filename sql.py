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
            # SQL command to create a table in the database 
            sql_command = """CREATE TABLE pecas (  
                                peca_id INTEGER PRIMARY KEY,  
                                peca_nome VARCHAR(30),
                                n_orcamento INTEGER,
                                material VARCHAR(5),
                                qualidade VARCHAR(5),
                                tempo_de_impressao REAL,
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
                                FOREIGN KEY(cliente_id) REFERENCES clientes(cliente_id),  
                                FOREIGN KEY(coladorador_id) REFERENCES colaboradores(colaborador_id)
                                );"""
                            
            
            self.crsr.execute(sql_command) 
            #save
            self.connection.commit()

    def insertInDB(self, tableName, data):
        #TODO: insert name of table
        self.crsr.execute("""
        INSERT INTO clientes (cliente_id, cliente_nome, cliente_contato, cliente_data_de_contato)
        VALUES (?,?,?,?,?,?,?,?)
        """, data)
        self.connection.commit()

    def createBackup(self):
        with io.open(self.name, 'w') as f:
            for linha in self.connection.iterdump():
                f.write('%s\n' % linha)
    
if __name__ == "__main__":
    db = DB()
    db.initDB()
    #db.insertInDB