from flask import Flask, url_for, render_template, jsonify, request
from flask.ext.pymongo import PyMongo
from pymongo import MongoClient
from bson.json_util import dumps
import ast
from bson.objectid import ObjectId

from datetime import datetime
from datetime import timedelta
import datetime

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


@app.route('/tasks', methods=['POST'])
def update_tasks():
    data = request.json
    rid = data['id']

    db.task.update(
        {'_id': ObjectId(rid)},
        {
            '$addToSet': {
                'updated': str(datetime.datetime.now())
            }
        }
    )

    return jsonify({'status': 'Success'})

@app.route('/tracker', methods=['GET'])
def tracker():
    r = list(db.task.find())
    arr = []

    for i in range(len(r)):
        if len(r[i]['updated']) == 1:
            arr.append(r[i]['updated'][0])
    
        if len(r[i]['updated']) > 1:
            for x in range(len(r[i]['updated'])):
                arr.append(r[i]['updated'][x])

    oldest = min(arr)

    return jsonify({
        'oldest': oldest,
        'dates': arr
    })


if __name__ == '__main__':
    app.run(debug=True)
