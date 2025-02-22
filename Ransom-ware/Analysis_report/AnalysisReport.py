import os
import hashlib
import magic
import math
from collections import Counter
from dotenv import load_dotenv
import subprocess


# Load environment variables
load_dotenv()
TARGET_FOLDER = os.getenv("TARGET_FOLDER")

# Dictionary of known ransomware extensions and families
RANSOMWARE_SIGNATURES = {
    ".wcry": {"family": "WannaCry", "encryption": "AES-128 + RSA-2048"},
    ".locky": {"family": "Locky", "encryption": "RSA-2048 + AES-128"},
    ".cerber": {"family": "Cerber", "encryption": "AES-256"},
    ".crypt": {"family": "CryptXXX", "encryption": "AES-256 + RSA-4096"},
    ".ragnar": {"family": "Ragnar Locker", "encryption": "ChaCha20 + RSA-2048"},
    ".REvil": {"family": "REvil (Sodinokibi)", "encryption": "AES-256 + RSA-4096"},
}

def calculate_entropy(file_path):
    """Calculate file entropy to check randomness (encrypted files have high entropy)."""
    with open(file_path, "rb") as f:
        data = f.read()
    
    if not data:
        return 0
    
    counter = Counter(data)
    length = len(data)
    entropy = -sum((count / length) * math.log2(count / length) for count in counter.values())
    
    return entropy

def analyze_file(file_path):
    """Analyze the file for ransomware indicators."""
    file_size = os.path.getsize(file_path)
    file_extension = os.path.splitext(file_path)[1]
    file_mime = magic.Magic(mime=True).from_file(file_path)
    entropy = calculate_entropy(file_path)

    # Determine if it's a ransomware-encrypted file
    if file_extension in RANSOMWARE_SIGNATURES:
        ransomware_details = RANSOMWARE_SIGNATURES[file_extension]
        ransomware_family = ransomware_details["family"]
        encryption_standard = ransomware_details["encryption"]
    else:
        ransomware_family = "Unknown"
        encryption_standard = "Unknown"

    # High entropy (>7.5) suggests strong encryption
    is_encrypted = entropy > 7.5

    return {
        "file_path": file_path,
        "size_bytes": file_size,
        "extension": file_extension,
        "mime_type": file_mime,
        "entropy": round(entropy, 2),
        "is_encrypted": is_encrypted,
        "ransomware_family": ransomware_family,
        "encryption_standard": encryption_standard,
    }

def analyze_folder(target_folder):
    """Scan and analyze all files in a target folder."""
    if not os.path.exists(target_folder):
        print(f"Error: Folder '{target_folder}' not found!")
        return []

    results = []
    for root, _, files in os.walk(target_folder):
        for file in files:
            file_path = os.path.join(root, file)
            analysis = analyze_file(file_path)
            results.append(analysis)

    return results

def print_report(results):
    """Print a formatted analysis report."""
    print("\n===== Ransomware Encrypted File Analysis Report =====")
    for result in results:
        print(f"\n🔍 File: {result['file_path']}")
        print(f"   📏 Size: {result['size_bytes']} bytes")
        print(f"   📂 Extension: {result['extension']}")
        print(f"   📄 MIME Type: {result['mime_type']}")
        print(f"   🔐 Entropy: {result['entropy']} (High entropy means likely encrypted)")
        print(f"   🛑 Ransomware Detected: {result['ransomware_family']}")
        print(f"   🔑 Encryption Standard: {result['encryption_standard']}")
        print(f"   ✅ Is Encrypted: {'Yes' if result['is_encrypted'] else 'No'}")

# Run the analysis
if __name__ == "__main__":
    if TARGET_FOLDER:
        report_results = analyze_folder(TARGET_FOLDER)

        if report_results:
            print_report(report_results)
        else:
            print("No files found for analysis.")
    else:
        print("Error: TARGET_FOLDER not found in .env file!")
