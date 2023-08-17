import time
from flask import Flask, render_template

app = Flask(__name__)

def fetch_data():
    # time.sleep(2.5)
    return [
        {'title':'Item 1', 'img':'https://cdn.pixabay.com/photo/2018/06/26/11/35/letter-3499237_960_720.png'},
        {'title':'Item 2', 'img':'https://cdn.pixabay.com/photo/2018/06/26/11/35/letter-3499237_960_720.png'},
        {'title':'Item 3', 'img':'https://cdn.pixabay.com/photo/2018/06/26/11/35/letter-3499237_960_720.png'}
    ]
            

@app.route('/')
def init():
    data=fetch_data()
    return render_template('index.html', items=data)

if __name__ == '__main__':
    app.run()