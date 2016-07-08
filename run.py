#!../venv/bin/python
<<<<<<< HEAD
# under normal circumstances, this script would not be necessary. the
# sample_application would have its own setup.py and be properly installed;
# however since it is not bundled in the sdist package, we need some hacks
# to make it work

import os
import sys

sys.path.append(os.path.dirname(__name__))

from dash import create_app

# create an app instance
app = create_app()

app.run(debug=True, host='0.0.0.0', port=8000)
=======
from app import app


app.run(debug=True, host="0.0.0.0", port=8000)
>>>>>>> 93b030a6f6b2a025630ebe6c8af9f1de4c93a36a
