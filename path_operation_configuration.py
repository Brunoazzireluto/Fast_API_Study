from enum import Enum

from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()


@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item


# Tags -> Passing Tags for the api documentation

@app.post("/items2/", response_model=Item, tags=["items"])
async def create_item(item: Item):
    return item


@app.get("/items/", tags=["items"])
async def read_items():
    return [{"name": "Foo", "price": 42}]


@app.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "johndoe"}]


# Tags with Enum

class Tags(Enum):
    items = "items"
    users = "users"

@app.get("/items2/", tags=[Tags.items])
async def get_items():
    return ["Portal gun", "Plumbus"]


@app.get("/users2/", tags=[Tags.users])
async def read_users():
    return ["Rick", "Morty"]


# Summary and description

@app.post("/item/", response_model=Item,
          summary="Create a Item",
          description="Create a item with all the information, name, description, price and tax",
          tags=["Item"]
          )
async def create_item(item: Item):
    return item


# Description from docstring

@app.post("/items/", response_model=Item, summary="Create an item")
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item


# Response description

@app.post(
    "/items-with-description-response/",
    response_model=Item,
    summary="Create an item",
    response_description="The created item",
)
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item


# Deprecate a path operation
@app.get("/elements/", tags=["items"], deprecated=True)
async def read_elements():
    return [{"item_id": "Foo"}]