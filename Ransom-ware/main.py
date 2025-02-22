from flask import Flask, request, jsonify
import os
import subprocess
from dotenv import load_dotenv
from decrypter.decrypter import Decryptor

# Load environment variables
load_dotenv()

target_folder = os.getenv("TARGET_FOLDER")

app = Flask(__name__)

@app.route('/')
def home():
    return "File Analysis and Decryption Server is Running!"

@app.route('/analyze', methods=['POST'])
def analyze_files():
    """Run the analysis script."""
    try:
        analysis_dir = os.path.join(os.getcwd(), "Analysis_report")
        script_path = os.path.join(analysis_dir, "AnalysisReport.py")
        
        if os.path.exists(script_path):
            subprocess.run(["python", script_path], cwd=analysis_dir)
            return jsonify({"message": "Analysis completed successfully."})
        else:
            return jsonify({"error": "AnalysisReport.py not found!"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/decrypt', methods=['POST'])
def decrypt_files():
    """Decrypt files using the Decryptor class."""
    if target_folder:
        try:
            decryptor = Decryptor(target_folder)
            decryptor.decrypt_all_files()
            return jsonify({"message": "Files decrypted successfully."})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "TARGET_FOLDER not set in .env file!"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
