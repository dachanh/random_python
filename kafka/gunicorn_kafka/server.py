import re 
from kafka import KafkaProducer
from datetime import datetime
from flask import Flask , request , jsonify , redirect 


app = Flask(__name__)

@app.route('/',methods =['POST'])
def test_api():
    return 'hello world'

if __name__ == "__main__":
    app.run('0.0.0.0',8179)