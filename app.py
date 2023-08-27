from flask import Flask, render_template, request, jsonify
from engine.db import PostgresDbConnector
from engine import db

app = Flask(__name__)
local_db = PostgresDbConnector(db.DB_PARAMS, db.DB_CUSTOM_PARAMS)

def fetch_data():
    local_db.init()
    data = local_db.load_all_data()
    local_db.close()
    if data is None:
        data = []
    return data
            
@app.route('/')
def render_index():
    data = fetch_data()
    return render_template('index.html', items=data)
    
if __name__ == '__main__':
    app.run()