from flask_restful import Resource, reqparse
import time
from flask import jsonify
from project.netrpi import (
    have_internet_connection,
    scan_networks,
    ap_start,
    ap_stop,
    connect_wifi,
    disconnect_wifi,
    get_network_status)

class InternetStatus(Resource):
    def get(self):
        print("> GET internet status")
        # Default to 200 OK
        internet_status = have_internet_connection()
        return jsonify(status=internet_status)

class NetScan(Resource):
    def get(self):
        print("> GET netscan")
        nb_try = 5
        for i in range(nb_try):
            if i > 0:
                time.sleep(1)
            netscan = scan_networks()
            if netscan is not None and len(netscan) > 0:
                break
        return jsonify(netscan)

class StartAp(Resource):
    def get(self):
        print("> GET start ap")
        ok = ap_start()
        return jsonify(success=ok)

class StopAp(Resource):
    def get(self):
        print("> GET stop ap")
        ok = ap_stop()
        return jsonify(success=ok)

class ConnectWifi(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ssid', type=str)
        parser.add_argument('psk', type=str)
        args = parser.parse_args()
        ssid = args["ssid"]
        psk = args["psk"]
        print("> GET connect wifi: ssid:{}".format(ssid))
        ok = connect_wifi(ssid, psk)
        return jsonify(success=ok)

class DisconnectWifi(Resource):
    def get(self):
        print("> GET disconnect wifi")
        ok = disconnect_wifi()
        return jsonify(success=ok)

class WifiStatus(Resource):
    def get(self):
        print("> GET wifi status")
        return jsonify(get_network_status())
