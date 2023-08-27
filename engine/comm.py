import requests
from engine import signals

flask_url = 'http://localhost:5000'  # Replace with your Flask server's URL

def post_signals():
    signals_data = {'progress_value': signals.SCRAPY_PROCESS, 'progress_status': str(signals.SCRAPY_STATUS)}
    response = requests.post(flask_url+'/api/set_progress', json=signals_data)

    if response.status_code == 200:
        print("Request posted succesfully!")
    else:
        print("Request failed with status code:", response.status_code)
    
    return response.json()
