import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash,jsonify
from contextlib import closing

import sqlite3

app = Flask(__name__)

#email_addresses = []

@app.before_request
def before_request():
    #g.db = sqlite3.connect("emails.db")
    g.db = sqlite3.connect("user.db")


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/')
def hello_world():
    author = "Me"
    
    return render_template('login.html', author=author)




@app.route('/signup', methods = ['POST','GET'])
def signup():
	if request.method == 'POST':
		
  		email = request.get_json('email')
        username = request.get_json('username')
        password = request.get_json('password')
        g.db.execute("INSERT INTO email(username,password,email) VALUES (?,?,?)", [username,password, email])
        email_addresses = g.db.execute("SELECT * FROM email").fetchall()
    	g.db.commit()
    	#ret_val={"value": "A"}
    	#return jsonify(ret_data)
    	return render_template('login.html')   #return hello_world
   		# email_addresses.append(email)
   		#return redirect(url_for('login'))
   		#return render_template('login.html')
   	return render_template('index.html', email=email_addresses)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
    	username = request.get_json('username')
        password = request.get_json('password')
        cur = g.db.execute('select username,password from email where username=? AND password=? ',[username,password])
        g.db.commit()
                 
        # if cur.fetchone() is None:
        #     error = 'No such user'
        # else:
        # 	return render_template('index.html') 
        	#return redirect(url_for('show_entries'))
           #session['logged_in'] = True
            #flash('You are logged in')
            #return redirect(url_for('show_entries'))
           # return ;
             
    return render_template('login.html', error=error)


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     error = None
#     if request.method == 'POST':
#         email = request.form['email']
#         username = request.form['username']
#         password = request.form['password']
#         # email=request.args.get('email');
#         # username=request.args.get('username');
#         # password=request.args.get('password');
        
#         g.db.execute('insert into users(username,password) values (?, ?, ?)',
#                  ["abc",username,password])
#         g.db.commit()
#         flash('You are successfully Registered ! Please Login')
#         return render_template('login.html')
#         # cur = g.db.execute('select * from students order by id desc')
#         # entries = [dict(username=row[0], password=row[1]) for row in cur.fetchall()]
#         # return render_template('homepage.html', entries=entries,username=username)
        
#     return render_template('index.html', error=error)

@app.route('/home', methods=['GET', 'POST'])
def home():
	if request.method == 'POST':
		email = request.get_json('email')
        username = request.get_json('username')
        password = request.get_json('password')
		# username = request.args.get('username')
  #       password = request.args.get('password')
  #       email = request.args.get('email')
        g.db.execute("INSERT INTO email(username,password,email) VALUES (?,?,?)", [username,password, email])
        email_addresses = g.db.execute("SELECT * FROM email").fetchall()
    	g.db.commit()
    	#ret_val={"value": "A"}
    	#return jsonify(ret_data)
    	return render_template('home.html')   #return hello_world
   		# email_addresses.append(email)
   		#return redirect(url_for('login'))
   		#return render_template('login.html')
   	return render_template('index.html')

# @app.route('/emails')
# def emails():
#     email_addresses = g.db.execute("SELECT title FROM email").fetchall()
#     return render_template('email.html', email=email_addresses)
#     #return render_template('emails.html', email_addresses=email_addresses)  #using array emailList


if __name__ == '__main__':
 app.run(port=8080, debug=True)