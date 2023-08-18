from flask import Flask, render_template
from engine.db import PostgresDbConnector
from engine import db

app = Flask(__name__)
local_db = PostgresDbConnector(db.DB_PARAMS, db.DB_CUSTOM_PARAMS)
data = []

def fetch_data():
    local_db.init()
    data = local_db.load_all_data()
    local_db.close()
    return data
            
@app.route('/')
def render_index():
    #return render_template('index.html', items=data)
    return render_template('test.html', items=data)

if __name__ == '__main__':
    data = fetch_data()
    app.run()