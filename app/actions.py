
import os
from flask import redirect

def hello_handler():
	return redirect('/page/hello', code=302)
