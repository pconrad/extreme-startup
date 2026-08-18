import json
import os
import shutil
import subprocess

import pymongo
from pathlib import Path


def _connect_with_ping(uri):
    """Create a client and verify connectivity immediately."""
    cli = pymongo.MongoClient(uri, serverSelectionTimeoutMS=3000)
    cli.admin.command("ping")
    return cli


def _connect_local_candidates():
    """Try the common local/container Mongo endpoints in order."""
    last_error = None
    for uri in ("mongodb://localhost:27017", "mongodb://mongo:27017"):
        try:
            return _connect_with_ping(uri)
        except pymongo.errors.PyMongoError as err:
            last_error = err

    raise RuntimeError(
        "Unable to connect to MongoDB at localhost:27017 or mongo:27017. "
        "Start a MongoDB service/container, set MONGO_URL, or provide "
        "flaskr/mongo_config.json for an external MongoDB connection."
    ) from last_error

def get_mongo_client(local=False):
    """
    Attempts to open flaskr/mongo_config.json and connect to the database there.
    If not found, or if local=True, then boots a local server and connects to it.
    This local server will be completely fresh
    """

    mongo_url = os.environ.get("MONGO_URL")
    if mongo_url:
        return _connect_with_ping(mongo_url)

    if "USE_LOCAL_MONGO_DB" in os.environ:
        destructive_start_localhost_mongo()
        return _connect_local_candidates()

    if local:
        destructive_start_localhost_mongo()
        return _connect_local_candidates()

    config_path = os.path.join(os.path.dirname(__file__), "mongo_config.json")

    # Try to update connect to json config, if it exists
    if os.path.isfile(config_path):
        with open(config_path) as f:
            cfg = json.load(f)
            try:
                conn_str = (
                    f"mongodb+srv://{cfg['user']}:{cfg['password']}@{cfg['address']}"
                )
                return _connect_with_ping(conn_str)
            except KeyError:
                print("Warning: malformed mongo_config.json. Using localhost DB.")
                return get_mongo_client(local=True)
    else:
        print("Warning: mongo_config.json not found. Using localhost DB")
        return get_mongo_client(local=True)


def destructive_start_localhost_mongo():
    """
    Kill any existing mongo server instance.
    Clean flaskr/_db.
    Starts a local mongod database using flaskr/db as the store.
    """
    # Only try to start mongod when the binary is available in this container.
    if shutil.which("mongod") is None:
        return

    # Remove and remake flaskr/db
    Path("/data/db").mkdir(parents=True, exist_ok=True)
    subprocess.Popen(["mongod"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
