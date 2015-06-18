
import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash,jsonify
from contextlib import closing



#=================================================
from flask import Flask, jsonify, render_template, request
app = Flask(__name__)

DATABASE = "C:/Users/Ashish/Desktop/flask-intro/user.db"
#DATABASE=os.path.join(app.root_path, 'students.db')
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(DATABASE)

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()



#================================================================
 
@app.route('/')
def index():
    return render_template('index.html')

@app.before_request
def before_request():
    if request.path != '/':
        if request.headers['content-type'].find('application/json'):
            return 'Unsupported Media Type', 415
 
@app.route('/echo', methods=['GET'])
def echo():
    ret_data = {"value": request.args.get('echoValue')}
    return jsonify(ret_data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    #show = 10
    if request.method == 'GET':
        username = request.args.get('username')
        password = request.args.get('password')
        email = request.args.get('email')
        g.db.execute('insert into users (email,username, password) values (?, ?, ?)',
                 [gmail.username,password])
        # g.db.commit()
                 
        # if cur is None:
        #     error = 'No such user'
        # else:
        #     session['logged_in'] = True
        #     flash('You are logged in')
        ret_data = {"value": request.args.get('username')}
        return jsonify(ret_data)
             
    return render_template('index.html', error=error)

 
if __name__ == '__main__':
    app.run(port=8090, debug=True)