import psycopg2
from psycopg2 import sql
import json

# Database connection parameters
DB_PARAMS = {
    'dbname': 'sreality_db',
    'user': 'postgres',
    'password': 'pass12345*',
    'host': 'localhost',  # Typically 'localhost'
    'port': '5432'   # Typically 5432
}

class PostgresDbConnector:
    _db_params = {}
    connection = None

    def __init__(self, db_params:dict):
        self._db_params = db_params

    def init(self):
        self.connection = self.create_connection()
        print("Database Initialization done!")
    
    def create_connection(self):
        try:
            connection = psycopg2.connect(**self._db_params)
            return connection
        except psycopg2.Error as e:
            print("Error: Unable to connect to the database")
            print(e)
            return None
    
    def create_table(self):
        try:
            create_table_query = '''
                CREATE TABLE IF NOT EXISTS data_table (
                    id serial PRIMARY KEY,
                    data JSONB
                );
            '''
            cursor = self.connection.cursor()
            cursor.execute(create_table_query)
            self.connection.commit()
            print("Table created successfully")
        except psycopg2.Error as e:
            print("Error: Unable to create the table")
            print(e)
            raise e
        
    def insert_data(self, data:dict):
        insert_query = sql.SQL('INSERT INTO data_table (data) VALUES (%s);')
        json_data = json.dumps(data)
        try:
            cursor = self.connection.cursor()
            cursor.execute(insert_query, (json_data,))
            self.connection.commit()
            print("Data inserted successfully")
        except psycopg2.Error as e:
            print("Error: Unable to insert data")
            print(e)

    def load_all_data(self):
        select_query = sql.SQL('SELECT * FROM data_table;')
        data_list = []
        try:
            cursor = self.connection.cursor()
            cursor.execute(select_query)
            rows = cursor.fetchall()
            for row in rows:
                print("ID:", row[0])
                print("Data:", row[1])
                print("-" * 20)
                data_list.append(row[1])
            return data_list
        except psycopg2.Error as e:
            print("Error: Unable to load data")
            print(e)
            return None     

    def close(self):
        self.connection.close()
        print("Connection closed...")

"""
if __name__ == "__main__":
    db = PostgresDbConnector(db_params)
    db.init()

    json_data = {'key1': 'value1', 'key2': 'value2'}
    db.insert_data(json_data)
    all_data= db.load_all_data()
    db.close()
"""
