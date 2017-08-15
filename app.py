# app.py

import os
import sqlite3 as sql
from flask import Flask,render_template, url_for,session,request,redirect, g
app = Flask(__name__)

app.secret_key = os.urandom(24)
	
# conn = sqlite3.connect('database.db')
# print "Opened database successfully";
# conn.execute('CREATE TABLE events (id integer primary key autoincrement, eventtitle text not null, college text not null, doe datetime not null, category text not null)')
# print "Table created successfully";
# conn.close()

# @app.route('/result/')
# def result():
# 	msg = "Record Successfully Added."
# 	return render_template('result.html',msg=msg)


@app.route('/')
def coevent():
	return redirect(url_for('home'))


@app.before_request
def before_request():
	g.user = None
	if 'user' in session:
		g.user = session['user']


@app.route('/login',methods = ['POST','GET'])
def login():
	if g.user:
		msg = 'You Are Already Logged In.'
		return render_template("logout.html",msg = msg)

	if request.method == 'POST':
		session.pop('user',None)

		if request.form['psw'] == 'password':
			session['user'] = request.form['uname']
			msg='Successfully Logged In'
			return render_template("result.html",msg = msg)

		else:
			msg='Not Logged In'
			return render_template("result.html",msg = msg)
		
	return render_template('login.html')


@app.route('/logout')
def logout():
	session.pop('user',None)
	msg='Successfully Logged Out'
	return render_template("result.html",msg = msg)


@app.route('/home')
def home():
	con = sql.connect("database.db")
	con.row_factory = sql.Row
	cur = con.cursor()
	cur.execute("select * from events where doe = (select min(doe) from events)")
	rows = cur.fetchall();
	return render_template('home.html',row=rows)


@app.route('/createevent')
def createevent():
	if g.user:
		return render_template('create_event.html')

	return redirect(url_for('login'))


@app.route('/addrecord',methods = ['POST', 'GET'])
def addrecord():

	if request.method == 'POST':
   		try:
   			eventtitle = request.form['eventtitle']
   			college = request.form['college']
   			doe = request.form['doe']
   			category = request.form['category']
   			with sql.connect("database.db") as con:
   				cur = con.cursor()
   				cur.execute("INSERT INTO events (eventtitle,college,doe,category) VALUES (?,?,?,?)",(eventtitle,college,doe,category) )
				con.commit()
				msg = "Record Successfully Added."
		except:
			con.rollback()
			msg = "Error In Inserting Record."
		finally:
			return render_template("result.html",msg = msg)
			con.close()
	else:
		msg = "Error In Inserting Record."
		return render_template("result.html",msg = msg)


@app.route('/elist', methods = ['POST','GET'])
def elist():
	con = sql.connect("database.db")
	con.row_factory = sql.Row
	cur = con.cursor()

	if request.method == 'POST':

		if request.form['selector']=='ename':
			cur.execute("select * from events where eventtitle = '%s' ORDER BY doe" %request.form['searchby'])

		if request.form['selector']=='cname':
			cur.execute("select * from events where college = '%s' ORDER BY doe" %request.form['searchby'])

		if request.form['selector']=='date':
			cur.execute("select * from events where doe = '%s' ORDER BY doe" %request.form['searchby'])

		if request.form['selector']=='category':
			cur.execute("select * from events where category = '%s' ORDER BY doe" %request.form['searchby'])
	
	else:

		cur.execute("select * from events ORDER BY doe")
	
	rows = cur.fetchall();
	return render_template("event_list.html",rows = rows)




if __name__=="__main__":
	app.run(debug=True)