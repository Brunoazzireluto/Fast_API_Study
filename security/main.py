from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/items")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"Token": token}

# https://fastapi.tiangolo.com/pt/tutorial/security/get-current-user/
