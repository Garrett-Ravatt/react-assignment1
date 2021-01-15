from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS

from random import choices
from string import ascii_lowercase, digits

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

users = { 
   'users_list' :
   [
      { 
         'id' : 'xyz789',
         'name' : 'Charlie',
         'job': 'Janitor',
      },
      {
         'id' : 'abc123', 
         'name': 'Mac',
         'job': 'Bouncer',
      },
      {
         'id' : 'ppp222', 
         'name': 'Mac',
         'job': 'Professor',
      }, 
      {
         'id' : 'yat999', 
         'name': 'Dee',
         'job': 'Aspring actress',
      },
      {
         'id' : 'zap555', 
         'name': 'Dennis',
         'job': 'Bartender',
      }
   ]
}

@app.route('/users', methods=['GET', 'POST', 'DELETE'])
def handle_users():
    if request.method == 'GET':
        search_username = request.args.get('name') #accessing the value of parameter 'name'
        if search_username:
            n_subdict = {'users_list' : []}
            for user in users['users_list']:
                if user['name'] == search_username:
                    n_subdict['users_list'].append(user)
        else:
            n_subdict = users
        search_job = request.args.get('job') #accessing the value of parameter 'job'
        if search_job:
            j_subdict = {'users_list' : []}
            for user in n_subdict['users_list']:
                if user['job'] == search_job:
                    j_subdict['users_list'].append(user)
            return j_subdict
        return n_subdict

    elif request.method == 'POST':
        userToAdd = request.get_json()
        if (userToAdd==None):
            resp = jsonify(success=False)
        else:
            if not userToAdd.get('id'):
                id = ''.join(choices(ascii_lowercase + digits, k = 6))
                userToAdd['id'] = id
            users['users_list'].append(userToAdd)
            resp = jsonify(userToAdd)
            resp.status_code = 201
            #resp.status_code = 200 #optionally, you can always set a response code. 
            # 200 is the default code for a normal response
        return resp

    elif request.method == 'DELETE':
        deleteRequest = request.get_json()
        if deleteRequest:
            id = deleteRequest.get('id')
            if id:
                for user in users['users_list']:
                    if user['id'] == id:
                        users['users_list'].remove(user)
                        return jsonify(success=True)
                return jsonify(success=False)
            #resp.status_code = 200 #optionally, you can always set a response code. 
            # 200 is the default code for a normal response
        return jsonify(success=False)

@app.route('/users/<id>')
def get_user(id):
    if id:
        for user in users['users_list']:
            if user['id'] == id:
                return user
        return ({})
    return users