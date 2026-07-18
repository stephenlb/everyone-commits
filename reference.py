import os
import shutil
from fastapi import FastAPI, UploadFile, File

app = FastAPI()

# Define the target directory to store files
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def save_uploaded_file(file: UploadFile = File(...)):
    # 1. Create the complete file destination path
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    # 2. Open a local file in write-binary mode
    with open(file_path, "wb") as buffer:
        # 3. Stream and copy the uploaded file object into the buffer
        shutil.copyfileobj(file.file, buffer)
        
    return {"filename": file.filename, "saved_to": file_path}
