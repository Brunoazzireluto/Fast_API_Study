from fastapi import FastAPI, Depends, Header, HTTPException

app = FastAPI()


async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-token header invalid")


async def verify_key(x_key: str = Header(...)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-key header invalid")


@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_item():
    return [{"item": "foo"}, {"Item": "bar"}]

# https://fastapi.tiangolo.com/pt/tutorial/dependencies/dependencies-in-path-operation-decorators/#dependencies-errors-and-return-values
