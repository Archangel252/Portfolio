import os
from flask_app import create_app

app  = create_app(debug = True)
if __name__ == "__main__":

	app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 443)), use_reloader=True)
	app.run()