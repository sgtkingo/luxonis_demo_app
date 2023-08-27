from flask import Flask, render_template, request, jsonify
from engine.db import PostgresDbConnector
from engine import db
from engine import signals

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
    return render_template('index.html', items=data, progress_value=0, progress_status = '')

@app.route('/api/get_progress')
def get_progress():
    signals_data = {'progress_value': signals.SCRAPY_PROCESS, 'progress_status': str(signals.SCRAPY_STATUS)}
    print(signals_data)
    return signals_data

@app.route('/api/set_progress', methods=['POST'])
def post_progress():
    try:
        signals_data = request.get_json()  # Get the JSON data from the request
        signals.SCRAPY_PROCESS = signals_data['progress_value']
        signals.SCRAPY_STATUS = signals_data['progress_status'] 

        # Return positive response
        result = {'message': 'Data received successfully'}
        return jsonify(result), 200
    except:
        error = {'error': 'Error in processing your request.'}
        return jsonify(error), 500
    
if __name__ == '__main__':
    app.run()