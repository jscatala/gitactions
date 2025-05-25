#!/usr/bin/python
# -*- coding: utf-8 -*-


from datetime import datetime
from flask import Flask, jsonify, request
import logging
import requests
import socket
import sys

FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(threadName)s - %(message)s"
formatter = logging.Formatter(FORMAT)

# single app logger:
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# 2 handlers for the same logger:
h1 = logging.StreamHandler(sys.stdout)
h1.setLevel(logging.DEBUG)
# filter out everything that is above Warning level (ERROR, ...)
h1.addFilter(lambda record: record.levelno <= logging.WARNING)
h1.setFormatter(formatter)
log.addHandler(h1)

h2 = logging.StreamHandler(sys.stderr)
# take only error logs
h2.setLevel(logging.ERROR)
h2.setFormatter(formatter)
log.addHandler(h2)


logw = logging.getLogger("werkzeug")
logw.setLevel(logging.ERROR)

app = Flask(__name__)


@app.route("/")
def main():
    return jsonify(message="Hello, Flask!")


@app.route("/version")
def version():
    data = {"tag": "v0.1", "build": "some datetime"}

    return jsonify(data, status=200, mimetype="application/json")


@app.route("/capital", methods=["GET"])
def get_capital_info():
    # Get the city parameter from the request
    city = request.args.get("city")

    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    # Construct the URL for the API request
    url = f"https://restcountries.com/v3.1/capital/{city}"

    try:
        # Make the request to the external API
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses

        # Return the JSON response from the external API
        return jsonify(response.json()), 200

    except requests.exceptions.HTTPError as http_err:
        return jsonify({"error": str(http_err)}), response.status_code
    except Exception as err:
        return jsonify({"error": str(err)}), 500


@app.route("/hello", methods=["GET"])
def hello_world():
    # Get the current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Get the hostname
    hostname = socket.gethostname()

    # Create the response
    response = {"message": "Hello World!", "time": current_time, "hostname": hostname}

    log.info(response)

    return jsonify(response), 200


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
