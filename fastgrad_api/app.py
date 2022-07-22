"""
app.py
====================================
The core module of the project.
"""
import redis
from flask import Flask

import os
import time
#from core import get_hit_count

app = Flask(__name__)
cache = redis.Redis(host="redis", port=6379)


@app.route("/")
def hello():
    """
    Return the most important thing about a person.
    Parameters
    ----------
    your_name
        A string indicating the name of the person.
    """
    count: int = cache
    retries: int = 5
    while True:
        try:
            return cache.incr("hits")
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)
    return "Hello World! I have been seen {} times.\n".format(count)


@app.route("/getall")
def getAll():
    """
    Return the most important thing about a person.
    Parameters
    ----------
    your_name
        A string indicating the name of the person.
    """
    return "kuy"


@app.route("/hee")
def hee():
    """
    Return the most important thing about a person.
    Parameters
    ----------
    your_name
        A string indicating the name of the person.
    """
    return "CMU SO FUN"

