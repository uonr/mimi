import os
import shutil
from typing import Optional
import uuid

def move(id: Optional[str]=None):
    # Create staging directory if it doesn't exist
    os.makedirs('./staging', exist_ok=True)
    os.chmod('./staging', 0o700)

    # Assign ID if provided, otherwise generate one
    id = id or str(uuid.uuid4())

    print(f"ID {id}")

    # Create secrets directory for the ID
    secrets_dir = f"./secrets/{id}/secret"
    os.makedirs(secrets_dir, exist_ok=True)
    os.chmod(secrets_dir, 0o700)

    # Move files from staging to secrets directory
    staging_files = os.listdir('./staging')
    for file_name in staging_files:
        file_path = os.path.join('./staging', file_name)
        # Skip directories
        if os.path.isdir(file_path):
            print(f"Skipping directory {file_path}")
            continue
        os.chmod(file_path, 0o600)
        shutil.move(file_path, os.path.join(secrets_dir, 'secret', file_name))
