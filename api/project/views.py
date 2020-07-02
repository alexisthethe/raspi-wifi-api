import os

from flask import Flask, jsonify
from flask_basicauth import BasicAuth
from flask_restful import Api
from project.resources import *


app = Flask(__name__)
app.config.from_object("project.config.ApiConfig")

basic_auth = BasicAuth(app)
api = Api(app)

@app.route("/")
def hello_world():
    return jsonify(api="rpiwifi")

api.add_resource(InternetStatus, "/internet_status")
api.add_resource(NetScan, "/netscan")
api.add_resource(StartAp, "/start_ap")
api.add_resource(StopAp, "/stop_ap")
api.add_resource(ConnectWifi, "/connect_wifi")
api.add_resource(DisconnectWifi, "/disconnect_wifi")
api.add_resource(WifiStatus, "/wifi_status")
