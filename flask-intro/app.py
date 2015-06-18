# all the imports
import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash,jsonify
from contextlib import closing

# create our little application :)
app = Flask(__name__)


     # configuration
DATABASE = "C:/Users/Ashish/Desktop/flask-intro/students.db"
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/show_entries')
def show_entries():
    cur = g.db.execute('select * from users order by username desc')
    entries = [dict(email=row[0], username=row[1], password=row[2]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)



# @app.route('/show_entries')
# def show_entries():
#     cur = g.db.execute('select name,branch from students order by id desc')
#     entries = [dict(name=row[0], branch=row[1]) for row in cur.fetchall()]
#     return render_template('show_entries.html', entries=entries)
# start the server with the 'run()' method

@app.route('/add', methods=['GET', 'POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into users (email,username, password) values (?, ?, ?)',
                 [request.args.get('email'),request.args.get('username'), 
                 request.args.get('password')])
    g.db.commit()
    flash('New entry was successfully posted')
    cur = g.db.execute('select * from users order by username desc')
    entries = [dict(username=row[0], password=row[1]) for row in cur.fetchall()]
    return jsonify(entries)
    #return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    #show = 10
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = g.db.execute('select username,password from users where username=? AND password=? ',[username,password])
        g.db.commit()
                 
        if cur is None:
            error = 'No such user'
        else:
            session['logged_in'] = True
            flash('You are logged in')
            return redirect(url_for('show_entries'))
           # return ;
             
    return render_template('login.html', error=error)



@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        #email = request.form['email']
        # username = request.form['username']
        # password = request.form['password']
        email=request.args.get('email');
        username=request.args.get('username');
        password=request.args.get('password');
        
        g.db.execute('insert into users(email, username,password) values (?, ?, ?)',
                 ["abc",username,password])
        g.db.commit()
        flash('You are successfully Registered ! Please Login')
        return render_template('login.html')
        # cur = g.db.execute('select * from students order by id desc')
        # entries = [dict(username=row[0], password=row[1]) for row in cur.fetchall()]
        # return render_template('homepage.html', entries=entries,username=username)
        
    return render_template('register.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)