import os
import zipfile
import paramiko
from datetime import datetime

# === CONFIGURATION ===
LOCAL_DIR = "/path/to/your/directory"
REMOTE_SERVER = "your.remote.server.com"
REMOTE_USER = "username"
REMOTE_PASSWORD = "password"
REMOTE_PATH = "/remote/backup/path"
REPORT_PATH = "backup_report.log"

def create_zip(source_dir, zip_name):
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for foldername, _, filenames in os.walk(source_dir):
            for filename in filenames:
                filepath = os.path.join(foldername, filename)
                arcname = os.path.relpath(filepath, source_dir)
                zipf.write(filepath, arcname)
    return zip_name

def upload_via_scp(zip_file):
    try:
        transport = paramiko.Transport((REMOTE_SERVER, 22))
        transport.connect(username=REMOTE_USER, password=REMOTE_PASSWORD)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put(zip_file, os.path.join(REMOTE_PATH, os.path.basename(zip_file)))
        sftp.close()
        transport.close()
        return True
    except Exception as e:
        return str(e)

def log_report(message):
    with open(REPORT_PATH, 'a') as f:
        f.write(f"{datetime.now()} - {message}\n")

def main():
    zip_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    try:
        zip_path = create_zip(LOCAL_DIR, zip_name)
        result = upload_via_scp(zip_path)
        if result is True:
            log_report(f"Backup successful: {zip_path} uploaded to {REMOTE_SERVER}")
        else:
            log_report(f"Backup failed: {result}")
    finally:
        if os.path.exists(zip_path):
            os.remove(zip_path)

if __name__ == "__main__":
    main()
