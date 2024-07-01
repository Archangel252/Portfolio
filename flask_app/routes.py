# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from flask import current_app as app
from flask import render_template, redirect, request, session, url_for, copy_current_request_context, send_from_directory

@app.route('/')
def root():
    return redirect('/home')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/resume')
def resume():
	return render_template('resume.html')

@app.route('/projects')
def projects():
	return render_template('projects.html')

@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r
