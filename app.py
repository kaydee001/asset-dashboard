import scanner
from pathlib import Path
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)
extensions = [".blend", ".fbx", ".obj"]


@app.route("/")
def hello_world():
    return "<p>Asset Dashboard Routes</p>"


@app.route("/scan")
def scan():
    folder = request.args.get("folder")
    if not folder:
        return "No folder path provided", 400
    if not Path(folder).exists():
        return "Path does not exist", 404
    data = scanner.run_scan(folder, extensions)
    return jsonify(data)


@app.route("/dashboard")
def dashboard():
    folder = request.args.get("folder")
    if not folder:
        return "No folder path provided", 400
    if not Path(folder).exists():
        return "Path does not exist", 404
    data = scanner.run_scan(folder, extensions)
    return render_template("dashboard.html", data=data)
