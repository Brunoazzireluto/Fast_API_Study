from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import HTMLResponse


app = FastAPI(title=' FastAPI Form Data')

@app.post('/login')
async def login(username: str = Form(...), password: str = Form(...)):
    return {'username': username}

# Request Files
@app.post("/files/")
async def create_file(file: bytes | None = File(None)):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}

# UploadFile with metadata
@app.post("/uploadfile2/")
async def create_upload_file(
    file: UploadFile = File(..., description="A file read as UploadFile", )
):
    return {"filename": file.filename}

# Multiple Files Uploads
@app.post("/files-multiples/")
async def create_files(files: list[bytes] = File(..., description="Multiple files as bytes")):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles-multiples/")
async def create_upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}


@app.get("/")
async def main():
    content = """
<body>
<form action="/files-multiples/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles-multiples/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)