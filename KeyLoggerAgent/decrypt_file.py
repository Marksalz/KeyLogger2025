import argparse
import json
import encryptor

def decrypt_file(file_path: str, key: str):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            decryptor = encryptor.Encryptor(key)
            for date_key, entries in data.items():
                for entry in entries:
                    if "data" in entry:
                        try:
                            entry["data"] = decryptor.decrypt(entry["data"])
                        except Exception as e:
                            print(f"Skipping entry due to decryption error: {entry}, Error: {e}")
            return json.dumps(data, indent=4)
    except Exception as e:
        print(f"Error: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Decrypt a file using a specified key.")
    parser.add_argument("file_path", type=str, help="The path to the encrypted file.")
    parser.add_argument("key", type=str, help="The decryption key.")
    args = parser.parse_args()

    decrypted_data = decrypt_file(args.file_path, args.key)
    if decrypted_data:
        print(f"Here is the decrypted data: {decrypted_data}")
    else:
        print("Failed to decrypt the file")

if __name__ == "__main__":
    main()
