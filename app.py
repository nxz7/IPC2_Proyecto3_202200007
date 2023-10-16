from flask import Flask, request, jsonify
from flask_cors import CORS
import xml.etree.ElementTree as ET
import base64

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return "<h1> PRUEBA FLASK! </h1>"


if __name__ == '__main__':
    app.run(threaded=True, port=5000, debug=True)
