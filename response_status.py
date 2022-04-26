from fastapi import FastAPI, status

app = FastAPI(title='FastAPI response code', version='0.1.1', description='Uma Api de teste')


@app.post('/items/', status_code=201)
async def create_item(name: str):
    return {'name': name}


# Shortcut to remember the names
@app.post('/items201/', status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {'name': name}