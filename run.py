#!../venv/bin/python

from app import app

# run the app
app.run(debug=True, host="0.0.0.0", port=8000)
