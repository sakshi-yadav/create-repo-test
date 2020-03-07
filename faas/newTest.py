import jsonfrom collections import defaultdictfrom http import HTTPStatusimport pymongo as pymongofrom elasticsearch import Elasticsearchimport paho.mqtt.client as mqttClientimport urllib.parseimport loggingimport requestsfrom pymongo import database, MongoClienterror_codes = {    1003: "Connection Not Established",    1006: "id required",    1007: "No record exists with this id",}def error_response(http_status, message_code):    data=[]    data.append(error_codes.get(message_code))    return {        "body": {            "code": http_status,            "message": "exception",            "data": data        },        "statusCode": http_status,        "headers": {'Content-Type': 'application/json'}    }def success_response(data, status_code):    return {        "body": {            "code": 0,            "message": "Request Completed Successfully",            "data": data        },        "statusCode": status_code,        "headers": {'Content-Type': 'application/json'}    }def connectToElastic(args):    headers=args.get("__ow_headers")    url=headers.get("elastic_url")    try:        es = Elasticsearch(url)        logging.info("Connection Established")    except Exception as ex:        logging.info("Cannot connect to Elastic Search"   ex)    return esdef connectToMqtt(args):    mqtt = args.get("__ow_headers").get("mqtt")    mqtt=mqtt.split(",")    user=mqtt.__getitem__(0)    password=mqtt.__getitem__(1)    broker=mqtt.__getitem__(2)    port=int(mqtt.__getitem__(3))    mqtt_client = mqttClient.Client()    mqtt_client.username_pw_set(user, password=password)    mqtt_client.connect(broker, port=port)    mqtt_client.loop_start()    return mqtt_clientdef connectToMongo(args,collection):    doc = args.get("__ow_headers")    mongo = doc.get("mongo")    mongo = mongo.split("=")    mongo = mongo.__getitem__(1)    mongo_connect_url = mongo.split(",")    mongo_connect_url = mongo_connect_url.__getitem__(0)    try:        database = pymongo.MongoClient(mongo_connect_url)    except:        return error_response(500, "cannot connnect to mongodb")    database=database.get_database()    connect=database[collection]    return connectdef main(args):    data= [        {        "category": "Floor 1",        "value": 320      },      {        "category": "Floor 2",        "value": 220      },      {        "category": "Floor 3",        "value": 300      },      {        "category": "Floor 4",        "value": 150      },      {        "category": "Floor 5",        "value": 275      }    ]    return success_response(data, 200)