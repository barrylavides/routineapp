from flask import Flask
from flask.ext.pymongo import PyMongo
from pymongo import MongoClient

app = Flask(__name__)
uri = 'mongodb://localhost/routineapp'
c = MongoClient(uri)
db = c.get_default_database()

@app.route('/')
def index():
    r = list(db.yo.find())

    print list(r)

    return 'Hello World'

if __name__ == '__main__':
    app.run(debug=True)
