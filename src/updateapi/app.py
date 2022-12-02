import os
import json

from flask import Flask, request

from updateapi.util import todo, check_keys_in_dict
from updateapi.util.api import ok, error
from updateapi.util.auth import check_authentication
from updateapi.config import config
from updateapi.db.models import Package, Device, Token

api_prefix = config.get("api.prefix")
upload_dir = config.get("storage.uploads.dir")
mod_name = config.get("meta.modname")
app = Flask(__name__)
app.secret_key = config.get("api.secrets.secret_key")

@app.route(api_prefix + "/<device>/<flavour>/packages", methods=["GET", "PUT"])
def packages_by_device_flavour(device: str, flavour: str):
    packages = Device.objects(__raw__=dict(codename=device, #pylint:disable=no-member
                                                packages=dict(
                                                    build_flavour=flavour,
                                                    ),
                                                ))
    if len(packages) == 0:
        return error("device_or_flavour_not_found", 404)
    if request.method == "GET":
        return ok(dict(packages=packages))
    elif request.method == "PUT":
        data = str(request.files['request'].read(), 'utf-8')
        try:
            data = json.loads(data)
        except:
            return error("bad_format", 400)
        if "token" not in data:
            return error("unauthorized", 401)
        if not check_authentication(data["token"]):
            return error("unauthorized", 401)
        if not check_keys_in_dict(["version",
                                   "incremental_version",
                                   "datetime", "package_type",
                                   "raw_filetype"], data):
            return error("bad_fields", 400)
        file_ = request.files['package']
        device_path = os.path.join(upload_dir, device)
        if not os.path.commonprefix([upload_dir, device_path]) != upload_dir:
            return error("bad_path", 400)
        if not os.path.isdir(device_path):
            os.mkdir(device_path)
        filetype = data["raw_filetype"]
        version = data["version"]
        incremental_version = data["incremental_version"]
        package_type = data["package_type"]
        filename = f"{mod_name}-{package_type}-{version}-{incremental_version}.{filetype}"
        upload_path = os.path.join(device_path, filename)
        if not os.path.commonprefix([device_path, upload_path]) != device_path:
            return error("bad_fields", 400)
        file_.save(upload_path)


@app.route(api_prefix + "/devices", methods=["GET", "PUT"])
def devices():
    if request.method == "GET":
        # For speed up we would not send all packages with
        # a device
        short_devices = list()
        for device in Device.objects(): #pylint: disable=no-member
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
        obj = data["object"]
        if not check_keys_in_dict(["name", "codename"], obj):
            return error("bad_fields")
        name = obj["name"]
        codename = obj["codename"]
        if len(Device.objects(name=name)) != 0: #pylint: disable=no-member
            return error("already_exists", 409)
        Device(name=name, codename=codename, n_packages=0, packages=list()).save()
        return ok(status_code=201)


