from datetime import datetime

import dat as dat
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

fake_db = {}


class Item(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None


app = FastAPI(title='Fake DB API')


@app.put('/items/{id}')
def update_item(id: str, item: Item):
    json_compatible_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_data
    return fake_db
