from flask import Flask, render_template, request, redirect, make_response
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
import pandas as pd

#import datatime


app = Flask(__name__)
api = Api(app)


class Shipdata(pd.DataFrame):
     
    def __init__(self) -> None:
        shipdata = pd.read_csv("shipdata.csv",delimiter=";")
        super().__init__(shipdata)


    def sortby(self, row):
        self.sort_values(row,inplace=True)
        return self

class ShipHome(Resource):

    def get(self):
         return make_response(Shipdata().to_json(),200)
        

class ShipSort(Resource):
     
    def get(self, row):
        if row not in Shipdata().columns:
            abort(404, message="Link can not be found")
        return make_response(Shipdata().sortby(row).to_json(),200)

class ShipAverage(Resource):

    def get(self):
        df = Shipdata().groupby('imo',as_index=False)[["mainEngineConsumption","DistanceOverGround","Speed"]].mean()
        return make_response(df.to_json(),200)

class ShipSum(Resource):

    def get(self):
        df = Shipdata().groupby('imo',as_index=False)[["mainEngineConsumption","DistanceOverGround","Speed"]].sum()
        return make_response(df.to_json(),200)
         
class ShipSumSort(Resource):

    def get(self, row):
        df = Shipdata().sortby(row)
        df = df.groupby('imo',as_index=False)[["mainEngineConsumption","DistanceOverGround","Speed"]].sum()
        return make_response(df.to_json(), 200)
    
class ShipAverageSort(Resource):

    def get(self, row):
        df = Shipdata().sortby(row)
        df = df.groupby('imo',as_index=False)[["mainEngineConsumption","DistanceOverGround","Speed"]].mean()
        return make_response(df.to_json(), 200)
#    def sortby(self, row):
        #sorteddata = self.sort_values(row,inplace=True)
#        return self.sort_values(row,inplace=True)
         
#class HelloWorld(Resource):
# shipdata = Shipdata()	
# 	#data.to_json()
# @app.route("/")
# def index():
#     sortby = request.args.get("sortby")
#     df = pd.read_csv("shipdata.csv",delimiter=";")
#     if sortby:
#         df.sort_values(sortby, inplace=True)
#     return render_template('index.html', shipinfo=df)

# @app.route("/shipsum")
# def shipsum():
#     sortby = request.args.get("sortby")
#     df = pd.read_csv("shipdata.csv",delimiter=";")
#     df = df.groupby('imo',as_index=False)[["mainEngineConsumption","DistanceOverGround","Speed"]].sum()
#     return render_template('index.html', shipinfo=df)

# @app.route("/shipaverage")
# def shipaverage():
#     sortby = request.args.get("sortby")
#     df = pd.read_csv("shipdata.csv",delimiter=";")
#     df = df.groupby('imo',as_index=False)[["mainEngineConsumption","DistanceOverGround","Speed"]].mean()
#     return render_template('index.html', shipinfo=df)


api.add_resource(ShipHome, "/")
api.add_resource(ShipSort, "/<string:row>")
api.add_resource(ShipAverage, "/shipaverage")
api.add_resource(ShipSum, "/shipsum")
api.add_resource(ShipAverageSort, "/shipaverage/<string:row>")
api.add_resource(ShipSumSort, "/shipsum/<string:row>")

if __name__ == "__main__":
	app.run(debug=True, port="5000")