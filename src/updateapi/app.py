from flask import Flask, request

from updateapi.util import todo
from updateapi.util.api import ok, error
from updateapi.util.auth import check_authentication
from updateapi.config import config
from updateapi.db.models import Package, Device, Token

api_prefix = config.get("api.prefix")
upload_dir = config.get("storage.uploads.dir")
app = Flask(__name__)
app.secret_key = config.get("api.secrets.secret_key")

@app.route(api_prefix + "/<str:device>/<str:flavour>/packages", methods=["GET", "PUT"])
def packages_by_device_flavour(device: str, flavour: str):
    if request.method == "GET":
         packages = Deivce.objects(__raw__=dict(codename=device,
                                                packages=dict(
                                                    build_flavour=flavour,
                                                    ),
                                                ))
         if len(packages) == 0:
             return error("device_or_flavour_not_found", 404)


@app.route(api_prefix + "/devices", methods=["GET", "PUT"])
def devices():
    if request.method == "GET":
        # For speed up we would not send all packages with
        # a device
        short_devices = list()
        for device in Device.objects():
            short_devices.append(dict(
                name=device.name,
                codename=device.codename,
                n_packages=device.n_packages,))
        return ok(short_devices)
    elif request.method == "PUT":
        content_type = request.headers.get("Content-Type", "application/x-octet-stream")
        if content_type.strip().lower() != "application/json":
            return error("bad_format")
        data = request.get_json()
        if "token" not in data:
            return error("unauthorized", 401)
        if not check_authentication(data["token"]):
            return error("unauthorized", 401)
        if "object" not in data:
            return error("no_object")
        if not check_in_list(["name", "codename"], list(obj.keys())):
            return error("bad_fields")
        name = obj["name"]
        codename = obj["codename"]
        if len(Devices.objects(name=name)) != 0:
            return error("already_exists", 409)
        Device(name=name, codename=codename, n_packages=0, packages=list()).save()
        return ok(status_code=201)


