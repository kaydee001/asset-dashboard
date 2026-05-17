import scanner
import json
from pathlib import Path
from flask import Flask, redirect, jsonify, request, render_template

app = Flask(__name__)

try:
    with open('config.json', 'r') as f:
        data = json.load(f)
        allowed_extensions = data['allowed_extensions']

except FileNotFoundError:
    print(f"error : config file was not found")

except json.JSONDecodeError as e:
    print(f"error : failed to decode json; {e.msg} at line {e.lineno}")

allowed_extensions = data.get(
    'allowed_extensions', [".fbx", ".obj", ".glb", ".gltf", ".blend"])


@app.route("/")
def hello_world():
    return redirect("/dashboard")


@app.route("/scan")
def scan():
    folder = request.args.get("folder")
    if not folder:
        return "No folder path provided", 400
    if not Path(folder).exists():
        return "Path does not exist", 404
    data = scanner.run_scan(folder, allowed_extensions)
    return jsonify(data)


@app.route("/dashboard")
def dashboard():
    folder = request.args.get("folder")
    if not folder:
        return render_template("dashboard.html")
    if not Path(folder).exists():
        return "Path does not exist", 404
    data = scanner.run_scan(folder, allowed_extensions)
    return render_template("dashboard.html", data=data)
