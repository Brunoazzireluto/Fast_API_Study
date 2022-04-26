from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from typing import Union

app = FastAPI(title='teste FastAPI', version='0.1.1', description='Uma Api de teste')

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: str | None = None


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password

def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    print(user_in_db)
    return user_in_db


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved

# Reduce duplication
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserInb(UserBase):
    password: str


class UserOutb(UserBase):
    pass


class UserInDBb(UserBase):
    hashed_password: str

def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.post("/user2/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved

# Union or anyOf
class BaseItem(BaseModel):
    description: str
    type: str

class CarItem(BaseItem):
    type = 'Car'

class PlaneItem(BaseItem):
    type = 'plane'
    size: int

items = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}

@app.get('/items/{item_id}', response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: str):
    return items[item_id]

# List of models
class Item2(BaseModel):
    name: str
    description: str

items2 = [
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "It's my aeroplane"},
]

@app.get('/items2/', response_model=list[Item2])
async def read_item():
    return items2

@app.get("/keyword-weights/", response_model=dict[str, float])
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.4}