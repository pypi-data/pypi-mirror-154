import importlib
import json
import os

import bottle
import waitress

_app = bottle.app()

_request = bottle.request
_response = bottle.response
_get = bottle.get
_post = bottle.post


def _filter(func):
    return _app.add_hook('before_request', func)


class _Api:
    def load(package):
        moduleDir = os.getcwd() + "/" + package.replace(".", "/")
        for moduleFile in os.listdir(os.path.abspath(moduleDir)):
            if moduleFile[-3:] == '.py' and moduleFile != '__init__.py':
                moduleName = package + "." + moduleFile[:-3]
                importlib.import_module(moduleName)

    def run(host, port):
        print(f"@app run {host}:{port}")
        waitress.serve(_app, host=host, port=port, ident="")

    def Error(code, msg=''):
        return bottle.HTTPResponse(status=code, body=msg)


class _R:
    def data(value):
        result = {"code": 200, "msg": "success", "data": value}
        body = json.dumps(result, ensure_ascii=False)
        return bottle.HTTPResponse(content_type="application/json", body=body)

    def success():
        result = {"code": 200, "msg": "success", "data": {}}
        body = json.dumps(result, ensure_ascii=False)
        return bottle.HTTPResponse(content_type="application/json", body=body)

    def fail(msg):
        result = {"code": 400, "msg": msg, "data": {}}
        body = json.dumps(result, ensure_ascii=False)
        return bottle.HTTPResponse(content_type="application/json", body=body)


_app.default_error_handler = lambda res: ""
