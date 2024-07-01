# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from flask import current_app as app
from flask import render_template, redirect, request, session, url_for, copy_current_request_context, send_from_directory
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from .utils.database.database  import database
from werkzeug.datastructures   import ImmutableMultiDict
from pprint import pprint
import json
import random
import functools
from . import socketio
db = database()


#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################
def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "email" not in session:
            return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)
    return secure_function

def getUser():
	return session['email'] if 'email' in session else 'Unknown'

def format_email():
    user_decry = getUser()
    if user_decry != 'Unknown':
        user_decry = db.reversibleEncrypt('decrypt',user_decry)

    return user_decry

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
	session.pop('email', default=None)
	return redirect('/')

@app.route('/processlogin', methods=["POST", "GET"])
def processlogin():
    form_fields = dict((key, request.form.getlist(key)[0]) for key in list(request.form.keys()))
    email = form_fields['email']
    password = form_fields['password']
    response = db.authenticate(email,password)
    if response['success']:
        session['email'] = db.reversibleEncrypt('encrypt', form_fields['email'])
        print('successful login')
        return json.dumps({'success': 1})
    else:
        print('failed login')
        return json.dumps({'success': 0})


#######################################################################################
# CHATROOM RELATED
#######################################################################################
@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html', user=format_email())

@socketio.on('joined', namespace='/chat')
def joined(message):
    join_room('main')
    owner = db.isOwner(format_email())
    if owner:
        emit('status', {'msg': format_email() + ' has entered the room.', 'style': 'width: 100%;color:blue;text-align: right'}, room='main')
    else:
        emit('status', {'msg': format_email() + ' has entered the room.', 'style': 'width: 100%;color:gray;text-align: left'}, room='main')
    

@socketio.on('left', namespace='/chat')
def left(message):
    leave_room('main')
    owner = db.isOwner(format_email())
    if owner:
        emit('status', {'msg': format_email() + ' has left the room.', 'style': 'width: 100%;color:red;text-align: right'}, room='main')
    else:
        emit('status', {'msg': format_email() + ' has left the room.', 'style': 'width: 100%;color:gray;text-align: left'}, room='main')

    
@socketio.on('chat', namespace='/chat')
def chat(message):
    owner = db.isOwner(format_email())
    if owner:
        emit('chat', {'msg': message['text'], 'style': 'width: 100%;color:blue;text-align: right'}, room='main')
    else:
        emit('chat', {'msg': message['text'], 'style': 'width: 100%;color:gray;text-align: left'}, room='main') 
# for when a chat comes in

#######################################################################################
# OTHER
#######################################################################################
@app.route('/')
def root():
    return redirect('/home')

@app.route('/home')
def home():
    #print(db.query('SELECT * FROM users'))    
    x = random.choice(['I started university when I was a wee lad of 15 years.','I have a pet sparrow.','I write poetry.'])
    return render_template('home.html', user = format_email())

@app.route('/resume')
def resume():
	resume_data = db.getResumeData()
	return render_template('resume.html', resume_data = resume_data, user = format_email())

@app.route('/projects')
def projects():
	return render_template('projects.html', user = format_email())

@app.route('/piano')
def piano():
	return render_template('piano.html', user = format_email())

@app.route('/feedback', methods = ['POST'])
def processfeedback():
	feedback = request.form
	columns = []
	vals = []
	for item in feedback.items():
		columns.append(item[0])
		vals.append(item[1])
	db.insertRows('feedback',columns,vals)
	total_feedback = db.GetFeedback()
	print(total_feedback)
	return render_template('feedback.html', total_feedback = total_feedback, user = format_email())

@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r
