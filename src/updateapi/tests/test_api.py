from updateapi.app import app
from updateapi.config import config

api_prefix = config.get("api.prefix")
upload_dir = config.get("storage.uploads.dir")

client = app.test_client()

def test_empty_devices() -> bool:
    response = client.get(api_prefix + "/devices")
    assert response.status_code == 200
    assert response.json["status"] == "ok"
    assert response.json["response"] == list()
    return True

def test_bad_put_devices() -> bool:
    response = client.put(api_prefix + "/devices")
    assert response.status_code == 400
    assert response.json["status"] == "error"
    assert response.json["error"] == "bad_format"
    return True
