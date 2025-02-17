import argparse
import encryptor

def decrypt_file(file_path: str, key: str):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            decrypted_lines = []
            decryptor = encryptor.Encryptor(key)
            for line in lines:
                try:
                    timestamp, encrypted_data = line.strip().split("] ")
                    encrypted_data = encrypted_data.rstrip("']")
                    encrypted_data = encrypted_data.lstrip("'")
                    decrypted_data = decryptor.decrypt(encrypted_data)
                    decrypted_lines.append(f"{timestamp}] '{decrypted_data}'")
                except ValueError:
                    print(f"Skipping line due to format error: {line.strip()}")
            return "\n".join(decrypted_lines)
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
        print(f"Here is the decryped data: {decrypted_data}")
    else:
        print("Failed to decrypt the file")

if __name__ == "__main__":
    main()