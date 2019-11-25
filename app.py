import os
from flask import Flask, redirect, url_for, request, render_template, jsonify
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
MONGODB_HOST = "mongodb"
MONGODB_PORT = 27017
MONGODB_USERNAME = os.environ['MONGODB_USER']
MONGODB_PASS = os.environ['MONGODB_PASS']

client = MongoClient(MONGODB_HOST, MONGODB_PORT)
db = client.tododb

# Authenticate with MongoDB if needed
if MONGODB_USERNAME != '':
    db.authenticate(MONGODB_USERNAME, MONGODB_PASS)
else:
    print("WARNING: Skipping Mongo DB Authentication - MONGODB_USER not provided")    


@app.route('/dbinfo')
def users():
    dbs = client.list_database_names()

    todoUsers = db.command('usersInfo')
    adminUsers = client.admin.command('usersInfo')

    return render_template('users.html', dbs=dbs, todoUsers=todoUsers, adminUsers=adminUsers)

@app.route('/')
def index():

    _items = db.tododb.find()
    items = [item for item in _items]

    return render_template('index.html', items=items)
    

@app.route('/new', methods=['POST'])
def new():

    if request.form['taskName'] != "":
        item_doc = {
            'name': request.form['taskName'],
            'description': request.form['taskDescription']
        }
        db.tododb.insert_one(item_doc)

    return redirect(url_for('index'))


@app.route('/item/<id>', methods=['GET'])
def get(id):
    
    myquery = {"_id": ObjectId(id)}

    item = db.tododb.find_one(myquery)
    
    return render_template('details.html', item=item)


@app.route('/item/update', methods=['POST'])
def update():
    
    id = request.form['id']
    selector = {"_id": ObjectId(id)}
    itemInfo = {
        '$set': {
            'name': request.form['name'],
            'description': request.form['description']
        }
    }
    
    result = db.tododb.update_one(selector, itemInfo)    
   
    return redirect(url_for('get', id=id))
    #return render_template('dbResult.html', result=result)
    
    
@app.route('/item/delete/<id>', methods=['DELETE', 'POST'])
def delete(id):
    myquery = {"_id": ObjectId(id)}

    result = db.tododb.delete_one(myquery)
    
    return redirect(url_for('index'))
    #return render_template('dbResult.html', result=result)
    
    
@app.errorhandler(404)
def page_not_found(e):
    """Send message to the user with notFound 404 status."""
    # Message to the user
    message = {
        "err":
            {
                "msg": "This route is currently not supported. Please refer API documentation."
            }
    }
    # Making the message look good
    resp = jsonify(message)
    # Sending OK response
    resp.status_code = 404
    # Returning the object
    return resp
    
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
