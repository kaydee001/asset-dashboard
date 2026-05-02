import scanner
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)
folder_ext = r"D:\Users\kartik\Desktop\pipeline-projects\asset-pipeline"
extensions = [".blend", ".fbx", ".obj"]


@app.route("/")
def hello_world():
    return "<p>Yo</p>"


@app.route("/scan")
def scan():
    folder = request.args.get("folder")
    if not folder:
        folder = folder_ext
    data = scanner.run_scan(folder, extensions)
    return jsonify(data)


@app.route("/dashboard")
def dashboard():
    folder = request.args.get("folder")
    if not folder:
        folder = folder_ext
    data = scanner.run_scan(folder, extensions)
    return render_template("dashboard.html", data=data)
