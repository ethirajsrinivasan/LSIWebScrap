from flask import Flask, jsonify
from flask import request  as queryreceiver
from search_engine_interface import *

app = Flask(__name__)

@app.route('/fetch_from_google')
def fetch_from_google():
    search = queryreceiver.args.get('query')
    messages = SearchEngineInterface(search).search_query()   
    return jsonify(messages)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port= 5000)
