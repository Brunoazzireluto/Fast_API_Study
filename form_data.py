from fastapi import FastAPI, Form

app = FastAPI(title=' FastAPI Form Data')

@app.post('/login')
async def login(username: str = Form(...), password: str = Form(...)):
    return {'username': username}

# Request Files
#https://fastapi.tiangolo.com/pt/tutorial/request-files/#import-file