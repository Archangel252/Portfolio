#--------------------------------------------------
# Import Requirements
#--------------------------------------------------
import os
from flask import Flask
from flask_failsafe import failsafe

#--------------------------------------------------
# Create a Failsafe Web Application
#--------------------------------------------------
# portfolio-428612
# Set-ExecutionPolicy RemoteSigned -Scope Process
# gcloud builds submit --tag gcr.io/portfolio-428612/portfolio_flask-app:v2
# gcloud run deploy --image gcr.io/portfolio-428612/portfolio_flask-app:v2 --platform managed
@failsafe
def create_app(debug=False):
	app = Flask(__name__)

	# This will prevent issues with cached static files
	app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
	#app.debug = debug

	# ----------------------------------------------

	with app.app_context():
		from . import routes
		return app
