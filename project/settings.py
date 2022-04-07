

from os import getenv


SLAVE_URL = getenv("SLAVE_URL")
IAM_URL = getenv("IAM_URL")
MONGO_HOST = getenv("MONGO_HOST", "localhost")
MONGO_PORT = str(getenv("MONGO_PORT", 27017))
MONGO_USER = getenv("MONGO_USER", None)
MONGO_PASSWORD = getenv("MONGO_PASSWORD", None)
PYMONGO_DEFAULT_KWARGS = {"compressors": "snappy"}

SECRET = getenv("secret_key")
