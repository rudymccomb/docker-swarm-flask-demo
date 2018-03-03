import socket
import uuid
import time
import ctypes
import random

from flask import Flask, render_template
from redis import Redis

from secrets import secret, SecretNotFoundError

# Create the flask application
app = Flask("__name__", static_folder="static")

# Connect to redis and set num_requests to 0 if it doesn't exist
redis = Redis(host='redis')
redis.setnx('num_requests', 0)

# Get the id of the docker container we're running in (it's our hostname)
container_id = socket.gethostname()

# Read our example secret
try:
    db_password = secret('db_password')
except SecretNotFoundError:
    db_password = 'NOT SET'

@app.route("/hello")
def hello():
    return "Hey there test"

@app.route("/text")
def text():
    return app.send_static_file('file.txt')

@app.route("/hex")
def hex():
    return app.send_static_file('hexdump.txt')

@app.route("/pic")
def pic():
    return app.send_static_file('3192.png')

@app.route("/random")
def random():
    value = random.random()

    if value > .9:
        return str(None / 1)

    if value < .1:
        pointer = ctypes.pointer(ctypes.c_char.from_address(5))
        pointer[0] = "5"
        return "Type of value is now {}".format(type(5))

    if value > .2 or value < .5:
        time.sleep(random.randint(0, 3))

    return "Hello, world!"

@app.route('/')
def home():
    # Increment the number of requests
    redis.incr('num_requests')

    # Display process information to the user
    return render_template(
        'home.html',
        container_id=container_id,
        num_requests=int(redis.get('num_requests')),
        db_password=db_password,
    )

if __name__ == '__main__':
    # This will only run when using docker-compose.override.yml
    app.run(debug=True, host='0.0.0.0')
