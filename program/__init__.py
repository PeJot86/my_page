from flask import *

app = Flask(__name__)

from program import routes

if __name__ == '__main__':
    app.run(debug=True)