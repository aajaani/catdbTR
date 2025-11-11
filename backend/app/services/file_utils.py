import hashlib, os
from typing import BinaryIO
from minio import Minio
from fastapi import UploadFile, HTTPException

MAX_FILE_MB = 20  
BUCKET = "tkk-cats"


def sha256_file(fileobj: BinaryIO, chunk: int=8192) -> str:
    h = hashlib.sha256()
    while True:
        data = fileobj.read(chunk)
        if not data:
            break
        h.update(data)
    fileobj.seek(0)
    return h.hexdigest()

def upload_to_minio(minio_client: Minio, file: UploadFile) -> str:
    # size guard
    file.file.seek(0, 2); size = file.file.tell(); file.file.seek(0)
    if size > MAX_FILE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail=f"File too large (> {MAX_FILE_MB}MB)")

    # keep original extension if present (broadly allowed)
    _, ext = os.path.splitext(file.filename or "")
    ext = ext.lower()
    digest = sha256_file(file.file)
    object_name = f"{digest}{ext}"

    # If exists, reuse 
    try:
        minio_client.stat_object(BUCKET, object_name)
        return object_name
    except Exception:
        pass

    # Upload
    try:
        minio_client.put_object(
            BUCKET,
            object_name,
            file.file,
            size,
            content_type=file.content_type or "application/octet-stream",
        )
        file.file.seek(0)
        return object_name
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Storage error: {e}")
