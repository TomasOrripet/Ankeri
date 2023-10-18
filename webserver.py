from flask import Flask, render_template, request, redirect, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
import pandas as pd
import requests

BASE = "http://127.0.0.1:5000/"




app = Flask(__name__)


@app.route("/")
def index():
    response = requests.get(BASE + "/").json()
    df = pd.DataFrame.from_dict(response)
    return render_template('index.html', shipinfo=df)


@app.route("/<string:row>")
def shipsort(row):
    
    response = requests.get(BASE + F"/{row}").json()
    if "message" in response:
        return response["message"]
    print(row)
    df = pd.DataFrame.from_dict(response)
    return render_template('index.html', shipinfo=df)

@app.route("/shipaverage")
def shipaverage():
    response = requests.get(BASE + "/shipaverage").json()
    df = pd.DataFrame.from_dict(response)
    return render_template('index.html', shipinfo=df)

@app.route("/shipsum")
def shipsum():
    response = requests.get(BASE + "/shipsum").json()
    df = pd.DataFrame.from_dict(response)
    return render_template('index.html', shipinfo=df)

@app.route("/shipsum/<string:row>")
def shipsumsort(row):
    response = requests.get(BASE + F"/shipsum/{row}").json()
    df = pd.DataFrame.from_dict(response)
    return render_template('index.html', shipinfo=df) 


if __name__ == "__main__":
	app.run(debug=True, port=5001)