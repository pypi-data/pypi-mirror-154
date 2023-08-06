import os

CONTEXT_PREFIX = "QANTIO_"


def add_to_context(key: str, value: str):
    os.environ[f"{CONTEXT_PREFIX}{key}"] = value


def get_context():
    return {
        x.replace(CONTEXT_PREFIX, "").lower(): os.environ[x]
        for x in os.environ
        if x.startswith(CONTEXT_PREFIX)
    }
