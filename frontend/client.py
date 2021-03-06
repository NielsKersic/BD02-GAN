from typing import Text
from flask import Flask, redirect, url_for, render_template, request, jsonify
from flask.wrappers import Response
from flask_restful import Resource
import requests
import os
import random

app = Flask(__name__)

# Get environment from env variables, but set default to dev
ENV = os.getenv('ENV', 'dev')
SERV_URL = os.getenv('SERV_URL', 'https://gan-dev.apis.niels.codes/')


BASE = SERV_URL

#Homepage
@app.route("/")
def home():
    return render_template("index.html")

#Homepage with user input
@app.route("/", methods=["POST"])
def home_post():
    input = request.form.get("input")
    if(input != ""):
        # SEND data to API
        response = requests.post(BASE + "mnist", {'value': input})
        response = response.json()
        
        # RECEIVE base64 image from API (and store it in the page)
        return render_template("index.html", encoded_img_string = response.get('img'), forward_message = "Getal: " + input)

    else:
        return render_template("index.html")


#About us page
@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")

#About GAN page
@app.route("/aboutgan")
def aboutgan():
    return render_template("aboutgan.html")

#Error 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

#Error 500
@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500    

#To do: In production: get rid of debug=True
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)