import json
import os
import shutil

import numpy as np
import requests

from .config import DATA_FILES_PATH, RAVENVERSE_URL, TEMP_FILES_PATH
from .socket_client import SocketClient


def save_data_to_file(data_id, data):
    """
    Method to save data in a pickle file
    """
    file_path = os.path.join(DATA_FILES_PATH, "data_{}.json".format(data_id))

    if os.path.exists(file_path):
        os.remove(file_path)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        if isinstance(data, np.ndarray):
            data = data.tolist()
        json.dump(data, f)

    return file_path


def load_data_from_file():
    pass


def delete_data_file(data_id):
    file_path = os.path.join(DATA_FILES_PATH, "data_{}.json".format(data_id))
    if os.path.exists(file_path):
        os.remove(file_path)


class Singleton:
    def __init__(self, cls):
        self._cls = cls

    def Instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._cls()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._cls)


def dump_data(data_id, value):
    """
    Dump ndarray to file
    """
    file_path = os.path.join(DATA_FILES_PATH, "data_{}.pkl".format(data_id))
    if os.path.exists(file_path):
        os.remove(file_path)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    value.dump(file_path)
    return file_path


def copy_data(source, destination):
    try:
        shutil.copy(source, destination)
        print("File copied successfully.")
    # If source and destination are same
    except shutil.SameFileError:
        print("Source and destination represents the same file.")
    # If there is any permission issue
    except PermissionError:
        print("Permission denied.")
    # For other errors
    except:
        print("Error occurred while copying file.")


def inform():
    socket_client = SocketClient(server_url=RAVENVERSE_URL).connect()
    socket_client.emit("inform", data={"type": "event"}, namespace="/ravop")


def make_request(endpoint, method, payload={}, headers=None):
    if method == "post":
        return requests.post(
            "{}/{}".format(RAVENVERSE_URL, endpoint), json=payload, headers=headers
        )
    elif method == "get":
        return requests.get(
            "{}/{}".format(RAVENVERSE_URL, endpoint), headers=headers
        )


def convert_to_ndarray(x):
    if isinstance(x, str):
        x = np.array(json.loads(x))
    elif isinstance(x, list) or isinstance(x, tuple) or isinstance(x, int) or isinstance(x, float):
        x = np.array(x)

    return x


def convert_ndarray_to_str(x):
    return str(x.tolist())


def dump_data(data_id, value):
    """
    Dump ndarray to file
    """
    file_path = os.path.join(TEMP_FILES_PATH, "data_{}.npy".format(data_id))
    if os.path.exists(file_path):
        os.remove(file_path)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    np.save(file_path, value)
    return file_path
