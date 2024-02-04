import subprocess

from flask import Blueprint
from flask_restful import Resource, Api
from .utils import get_state_info
from constance import redis_get

api_bp = Blueprint('api', __name__)
api = Api(api_bp)


class Info(Resource):
    def get(self):
        # Set the response code to 201
        task = get_state_info()
        return task, 201


class Stop(Resource):
    def get(self):
        # Set the response code to 201
        context = {'status': 'busy', 'msg': 'Stop du Raspberry Pi en cours ...'}
        if redis_get("prog_status") in ["Libre", "Hors ligne"]:
            subprocess.Popen(["sudo", "shutdown", "-h", "now"])
            context['status'] = 'stop'
        else:
            context['msg'] = 'Arret impossible, Raspberry Pi occupe'
        return context, 201


class Restart(Resource):
    def get(self):
        # Set the response code to 201
        context = {'status': 'busy', 'msg': 'Restart du Raspberry Pi en cours ...'}
        if redis_get("prog_status") in ["Libre", "Hors ligne"]:
            subprocess.Popen(["sudo", "reboot"])
            context['status'] = 'reboot'
        else:
            context['msg'] = 'Restart impossible, Raspberry Pi occupe'
        return context, 201


##
# Actually setup the Api resource routing here
##
api.add_resource(Info, '/api/info/')
api.add_resource(Stop, '/api/stop/')
api.add_resource(Restart, '/api/restart/')
