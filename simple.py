from flask import Flask, render_template, request, redirect
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
import pandas as pd
import requests

#import datatime
BASE = "http://127.0.0.1:5000/"

app = Flask(__name__)
api = Api(app)


class Shipdata(pd.DataFrame):
     
    def __init__(self) -> None:
        shipdata = pd.read_csv("shipdata.csv",delimiter=";")
        super().__init__(shipdata)


    def sortby(self, row):
        #sorteddata = self.sort_values(row,inplace=True)
        return self.sort_values(row,inplace=True)
         
shipdata = Shipdata()	

@app.route("/")
def index():
    sortby = request.args.get("sortby")
    df = pd.read_csv("shipdata.csv",delimiter=";")
    if sortby:
        df.sort_values(sortby,ascending=False, inplace=True)
    return render_template('indexsimple.html', shipinfo=df)

@app.route("/<string:row>")
def shipsort(row):
    return "This url can't be found"


@app.route("/shipsum")
def shipsum():
    sortby = request.args.get("sortby")
    df = pd.read_csv("shipdata.csv",delimiter=";")
    df = df.groupby('imo',as_index=False)[["mainEngineConsumption","DistanceOverGround","Speed"]].sum().round(2)
    if sortby:
        df.sort_values(sortby,ascending=False, inplace=True)
    return render_template('indexsimple.html', shipinfo=df)

@app.route("/shipaverage")
def shipaverage():
    sortby = request.args.get("sortby")
    df = pd.read_csv("shipdata.csv",delimiter=";")
    df = df.groupby('imo',as_index=False)[["mainEngineConsumption","DistanceOverGround","Speed"]].mean().round(2)
    if sortby:
        df.sort_values(sortby,ascending=False, inplace=True)
    return render_template('indexsimple.html', shipinfo=df)

    


if __name__ == "__main__":
	app.run(debug=True)