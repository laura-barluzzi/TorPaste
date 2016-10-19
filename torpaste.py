#!bin/python
# -*- coding: utf-8 -*-

import importlib
import time
from datetime import datetime
from os import getenv
import sys
import logic

from flask import *

app = Flask(__name__)

VERSION = "0.6"
COMPATIBLE_BACKENDS = ["filesystem"]


@app.route('/')
def index():
    return render_template(
        "index.html",
        config=config,
        version=VERSION,
        page="main"
    )


@app.route("/new", methods=["GET", "POST"])
def new_paste():
    if request.method == "GET":
        return render_template(
            "index.html",
            config=config,
            version=VERSION,
            page="new"
        )
    else:
        if (request.form['content']):
            status, message = logic.create_new_paste(
                request.form['content'],
                config
            )
            if (status == "ERROR"):
                return Response(
                    render_template(
                        "index.html",
                        config=config,
                        version=VERSION,
                        page="new",
                        error=message
                    ),
                    400
                )

            if (status == "OK"):
                return redirect("/view/" + message)
        else:
            return Response(
                render_template(
                    "index.html",
                    config=config,
                    version=VERSION,
                    error="Please enter some text to include in the paste.",
                    page="new"
                ),
                400
            )


@app.route("/view/<pasteid>")
def view_paste(pasteid):
    status, data, code = logic.view_existing_paste(pasteid, config)

    if (status == "ERROR"):
        return Response(
            render_template(
                "index.html",
                config=config,
                version=VERSION,
                error=data,
                page="new"
            ),
            code
        )

    if (status == "OK"):
        paste_date = datetime.fromtimestamp(
            int(
                data[1]
            ) + time.altzone + 3600).strftime("%H:%M:%S %d/%m/%Y")

        paste_size = logic.format_size(len(data[0].encode('utf-8')))

    if (status == "WARNING"):
        paste_date = "Not available."

    return Response(
        render_template(
            "view.html",
            content=data[0],
            date=paste_date,
            size=paste_size,
            pid=pasteid,
            config=config,
            version=VERSION,
            page="view"
        ),
        200
    )


@app.route("/raw/<pasteid>")
def raw_paste(pasteid):
    status, data, code = logic.view_existing_paste(pasteid, config)

    if (status == "ERROR" and code >= 500):
        return Response(data, code, mimetype="text/plain")
    if (status == "ERROR"):
        return Response("No such paste", code, mimetype="text/plain")
    return Response(data[0], mimetype="text/plain")


@app.route("/list")
def list():
    status, data, code = logic.get_paste_listing(config)

    if (status == "ERROR"):
        return Response(
            render_template(
                "index.html",
                config=config,
                version=VERSION,
                page="new",
                error=data
            ),
            code
        )

    return Response(
        render_template(
            "list.html",
            pastes=data,
            config=config,
            version=VERSION,
            page="list"
        )
    )


@app.route("/about")
def about_tor_paste():
    return render_template(
        "about.html",
        config=config,
        version=VERSION,
        page="about"
    )


@app.after_request
def additional_headers(response):
    response.headers["X-Frame-Options"] = "NONE"
    response.headers["X-Xss-Protection"] = "1; mode=block"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Content-Security-Policy"] = "default-src 'none'; "
    response.headers["Content-Security-Policy"] += "img-src 'self'; "
    response.headers["Content-Security-Policy"] += "style-src 'self'; "
    if (config['CSP_REPORT_URI']):
        response.headers["Content-Security-Policy"] += "report-uri "
        response.headers["Content-Security-Policy"] += config['CSP_REPORT_URI']
    return response

# Required Initialization Code

# necessary for local modules import (backends, exceptions)
sys.path.append('.')


# Handle Environment Variables (for configuration)
def load_config():
    # Web App <title>
    WEBSITE_TITLE = getenv("TP_WEBSITE_TITLE") or "Tor Paste"

    # Backend Used
    BACKEND = getenv("TP_BACKEND") or "filesystem"

    if BACKEND in COMPATIBLE_BACKENDS:
        b = importlib.import_module('backends.'+BACKEND)
    else:
        print(
            "Configured backend (" + BACKEND + ") is not compatible with " +
            "current version."
        )
        exit(1)

    # Maximum Paste Size
    MAX_PASTE_SIZE = getenv("TP_PASTE_MAX_SIZE") or "1 P"

    if MAX_PASTE_SIZE[0] == "0":
        MAX_PASTE_SIZE = "1 P"

    MAX_PASTE_SIZE = MAX_PASTE_SIZE.split(" ")

    try:
        AMOUNT = int(MAX_PASTE_SIZE[0])
        UNIT = MAX_PASTE_SIZE[1]
    except:
        print("Invalid TP_PASTE_MAX_SIZE: " + " ".join(MAX_PASTE_SIZE))
        exit(1)

    orders = ["B", "k", "M", "G", "T", "P"]

    if UNIT not in orders:
        print("Invalid Unit Size: " + UNIT)

    try:
        MAX_PASTE_SIZE = AMOUNT * 1024**orders.index(UNIT)
    except:
        print("An unknown error occured while determining max paste size.")
        exit(1)

    # Disable the paste listing feature
    PASTE_LIST_ACTIVE = getenv("TP_PASTE_LIST_ACTIVE") or True
    if PASTE_LIST_ACTIVE in ["False", "false", 0, "0"]:
        PASTE_LIST_ACTIVE = False

    # Content Security Policy Handling
    CSP_REPORT_URI = getenv("TP_CSP_REPORT_URI") or False

    return {
        "MAX_PASTE_SIZE": MAX_PASTE_SIZE,
        "WEBSITE_TITLE": WEBSITE_TITLE,
        "PASTE_LIST_ACTIVE": PASTE_LIST_ACTIVE,
        "b": b,
        "CSP_REPORT_URI": CSP_REPORT_URI
    }

config = load_config()
b = config['b']

# Initialize Backend
try:
    b.initialize_backend()
except:
    print("Failed to initialize backend")
    exit(1)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
