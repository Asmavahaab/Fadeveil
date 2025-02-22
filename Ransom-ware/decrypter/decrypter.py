import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Decryptor:
    def __init__(self, folder_path):
        self.folder_path = folder_path or "D:/My_final_project/Gama/files"  # Set default folder
        self.rsa_private_key_file = os.path.join(os.path.dirname(__file__), "..", "key", "private_key.pem")
        self.encrypted_aes_key_file = os.path.join(os.path.dirname(__file__), "..", "key", "encrypted_aes_key.bin")


    def decrypt_aes_key(self):
        """Decrypt AES key using RSA private key."""
        with open(self.rsa_private_key_file, "rb") as priv_file:
            private_key = serialization.load_pem_private_key(priv_file.read(), password=None)

        with open(self.encrypted_aes_key_file, "rb") as enc_key_file:
            encrypted_aes_key = enc_key_file.read()

        aes_key = private_key.decrypt(
            encrypted_aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return aes_key

    def decrypt_file(self, file_path, aes_key):
        """Decrypt the given file and remove .wcry extension."""
        try:
            with open(file_path, "rb") as file:
                file_data = file.read()

            iv = file_data[:16]  # Extract IV
            ciphertext = file_data[16:]

            cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
            decryptor = cipher.decryptor()
            plaintext = decryptor.update(ciphertext) + decryptor.finalize()

            # Remove padding
            padding_length = plaintext[-1]
            plaintext = plaintext[:-padding_length]

            original_filepath = file_path[:-5]  # Remove .wcry extension
            with open(original_filepath, "wb") as file:
                file.write(plaintext)

            os.remove(file_path)  # Delete encrypted file
            print(f"File '{file_path}' decrypted successfully to '{original_filepath}'.")
        
        except Exception as e:
            print(f"Error during decryption: {e}")

    def decrypt_all_files(self):
        """Decrypt all files in the specified folder."""
        try:
            aes_key = self.decrypt_aes_key()
            for root, _, files in os.walk(self.folder_path):
                for file in files:
                    if file.endswith(".wcry"):
                        file_path = os.path.join(root, file)
                        self.decrypt_file(file_path, aes_key)
        except Exception as e:
            print(f"Decryption process failed: {e}")

# Usage example
if __name__ == "__main__":
    target_folder = os.getenv("TARGET_FOLDER", "D:/My_final_project/Gama/files")  # Set default folder
    decryptor = Decryptor(target_folder)
    decryptor.decrypt_all_files()
