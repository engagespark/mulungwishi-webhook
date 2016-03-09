#!flask/bin/python
import sys
from app import mulungwishi_app

# This line below is used but not recognized by flake8. Must be ignored to pass the flake8 checking 
from app import views # flake8: noqa


try:
    host = sys.argv[1]
except:
    host = '127.0.0.1'

mulungwishi_app.run(debug=False, host=host)
