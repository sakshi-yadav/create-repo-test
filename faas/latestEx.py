import json
from collections import defaultdict
from http import HTTPStatus
import pymongo as pymongo
import urllib.parse
import logging
import requests
from pymongo import database, MongoClient

error_codes = {

    1003: "Connection Not Established",
    1006: "id required",
    1007: "No record exists with this id",

}

def error_response(error_code, http_status):
    return {
        "body": {
            "code": error_code,
            "message": error_codes.get(error_code),
            "data": {}
        },
        "statusCode": http_status,
        "headers": {'Content-Type': 'application/json'}
    }

def connectToMongo(args,collection):
    doc = args.get("__ow_headers")
    mongo = doc.get("mongo")
    mongo = mongo.split("=")
    mongo = mongo.__getitem__(1)
    mongo_connect_url = mongo.split(",")
    mongo_connect_url = mongo_connect_url.__getitem__(0)
    try:
        database = pymongo.MongoClient(mongo_connect_url)
    except:
        return error_response(500, "cannot connnect to mongodb")
    database=database.get_database()
    connect=database[collection]
    return connect

def success_response(data, status_code):
    return {
        "body": {
        "code": 0,
        "message": "Request Completed Successfully",
        "data": data
        },
        "statusCode": status_code,
        "headers": {'Content-Type': 'application/json'}
        }

def main(args):
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    data={}
    availableAttributes=["bin","timestamp"]
    data["availableAttributes"]=availableAttributes
    units=["%"]
    data["units"]=units
    chartData=[]
    data["chartData"]=chartData
    connection=connectToMongo(args,"ETL_analytics_smartbinsimulator")
    id=args.get("id")
    for i in connection.find({"data.serial_id":id}).sort([("timestamp",-1)]).limit(300):
      dic={}
      dic["bin"]=i.get("data").get("bin_fill1")
      dic["timestamp"]=i.get("timestamp")
      chartData.append(dic)
    return success_response(data, 200)