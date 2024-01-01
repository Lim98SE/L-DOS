# This is the source code for PKMAN. Hosted by PythonAnywhere for free!

import flask
from flask import Flask, request, render_template, send_file

import os

app = Flask(__name__)

@app.route("/search")
def search():
    query = request.args.get("q")

    if query is None:
        return []

    found_querys = []

    for i in os.listdir("pkgs"):
        if query in i.replace(".py", ""):
            found_querys.append(i.replace(".py", ""))

    return str(found_querys)

@app.route("/size")
def size():
    query = request.args.get("q")

    if query is None:
        return "*** ERROR ***"

    query += ".py"

    try:
        with open("pkgs/" + query) as file:
            size = len(file.read())

        return str(size)

    except:
        return "*** ERROR ***"

@app.route("/download")
def download():
    query = request.args.get("q")

    if query is None:
        return "*** ERROR ***"

    query += ".py"

    try:
        return send_file("pkgs/" + query)

    except:
        return "*** ERROR ***"
