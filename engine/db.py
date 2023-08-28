import psycopg2
from psycopg2 import sql
import json
import time

# Database connection parameters
DB_PARAMS = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'pass12345*',
    'host': 'db',  # By docker container name
    'port' : '5432',
}

DB_CUSTOM_PARAMS = {
    'default_table' : 'data_table'
}

#My custom postgres db connector 
class PostgresDbConnector:
    _db_params = {}
    _custom_params = {}
    connection = None

    def __init__(self, db_params:dict, custom_params:dict):
        self._db_params = db_params
        self._custom_params = custom_params

    def init(self):
        counter = 10
        while self.connection is None and counter > 0:
            print(f"Traing to connect database... {counter}/10")
            time.sleep(1)
            counter -=1
            self.connection = self.create_connection()
        if self.connection is None:
            raise psycopg2.DatabaseError("Initialization failed!")
        else:
            print("Database Initialization done!")
    
    def create_connection(self):
        try:
            connection = psycopg2.connect(**self._db_params)
            return connection
        except psycopg2.Error as e:
            print("Error: Unable to connect to the database")
            print(e)
            return None
    
    def drop_table(self):
        try:
            drop_table_query = f'''
                DROP TABLE {self._custom_params.get('default_table')};
            '''
            cursor = self.connection.cursor()
            cursor.execute(drop_table_query)
            self.connection.commit()
            print("Table droped successfully")
        except psycopg2.Error as e:
            print("Error: Unable to drop the table")
            print(e)

    def create_table(self):
        try:
            #Drop old table if exist
            self.drop_table()
            #Re-create table query
            create_table_query = f'''
                CREATE TABLE IF NOT EXISTS {self._custom_params.get('default_table')} (
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
        insert_query = sql.SQL(f"INSERT INTO {self._custom_params.get('default_table')} (data) VALUES (%s);")
        json_data = json.dumps(data)
        try:
            cursor = self.connection.cursor()
            cursor.execute(insert_query, (json_data,))
            self.connection.commit()
        except psycopg2.Error as e:
            print("Error: Unable to insert data")
            print(e)

    def load_all_data(self):
        select_query = sql.SQL(f"SELECT * FROM {self._custom_params.get('default_table')};")
        data_list = []
        try:
            cursor = self.connection.cursor()
            cursor.execute(select_query)
            rows = cursor.fetchall()
            for row in rows:
                data = dict(row[1])
                data['id'] = row[0]
                data_list.append(data)
            print(f"{len(data_list)} records loads...")
            return data_list
        except psycopg2.Error as e:
            print("Error: Unable to load data")
            print(e)
            return None     

    def close(self):
        self.connection.close()
        self.connection = None
        print("Connection closed...")



if __name__ == "__main__":
    db = PostgresDbConnector(DB_PARAMS, DB_CUSTOM_PARAMS)
    db.init()
    db.create_table()

    all_data= db.load_all_data()
    db.close()


