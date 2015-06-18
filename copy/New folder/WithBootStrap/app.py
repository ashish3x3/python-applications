from flask import *
import functools
from functools import wraps
import sqlite3

DATABASE= 'users.db'



app=Flask(__name__)

app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

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

app.secret_key='my key'

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/welcome')
def welcome():
	return render_template('welcome.html')

@app.route('/hello')
def hello():
	if 'logged_in' in session:
		curr=g.db.execute('select username,password from user')
		users = [dict(username=row[0], password=row[1]) for row in curr.fetchall()]
		return render_template('hello.html',users=users)
	return 'You are not logged in'

@app.route('/log',methods=['GET','POST'])
def log():
	error=None
	if request.method =='POST':
		username =  request.form['username']
		password = request.form['password']
		c = g.db.execute("SELECT username, password from user where username = (?)", [username])
		#g.db.commit()
		user = c.fetchone()
		# don't forget to apply your hashing algorithm to form.password.data
		if user and user[1] == password:
			session['logged_in']=True
			flash('You were logged in')
			return redirect(url_for('hello'))  
    							
		else:
			error='Invalid login--------- credintials.'
			
	return render_template('log.html', error=error)

@app.route('/create',methods=['GET','POST'])
def create():
	if request.method =='POST':
		username =  request.form['username']
		password = request.form['password']
		g.db.execute("INSERT INTO user(username,password) VALUES (?,?)", [username,password])
		curr=g.db.execute('select username,password from user')
		users = [dict(username=row[0], password=row[1]) for row in curr.fetchall()]
		g.db.commit()
		return render_template('hello.html',users=users)
	return render_template('hello.html')

    

@app.route('/register',methods=['GET','POST'])
def register():
	if request.method =='POST':
		username =  request.form['username']
		password = request.form['password']
		g.db.execute("INSERT INTO user(username,password) VALUES (?,?)", [username,password])		
		g.db.commit()
		return redirect(url_for('log'))
	return render_template('register.html')

def login_required(test):
	@wraps(test)
	def wrap(self,*args,**kwargs):
		if 'logged_in' in session:
			return test(self,*args, **kwargs)
		else:
			flash('You are logged out')
			return redirect(url_for('log'))
	return wraps



def home():
	return render_template('home.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('home'))


if __name__ == '__main__':
	app.run(debug=True) 

	