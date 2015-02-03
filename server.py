from flask import Flask, url_for, render_template, jsonify
from flask.ext.pymongo import PyMongo
from pymongo import MongoClient
from bson.json_util import dumps
import ast

app = Flask(__name__)
uri = 'mongodb://localhost/routineapp'
c = MongoClient(uri)
db = c.get_default_database()

def mongoObj(jsn):
    jsn = ast.literal_eval(dumps(jsn))
    
    # mongo object returns BJSON as its id
    # this function will convert the BSJON to json
    # and at the same time will remove the oid,
    # and assign the oid's value to its parent id
    for i,v in enumerate(jsn):
        jsn[i]['_id'] = jsn[i]['_id']['$oid']
    
    return jsn


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    r = mongoObj(list(db.task.find()))
    
    return jsonify({'tasks': r})

if __name__ == '__main__':
    app.run(debug=True)
