from typing import List, Optional
from fastapi import FastAPI, Query, Path, Body, Cookie, Header
from enum import Enum
from pydantic import BaseModel, EmailStr, Field, HttpUrl
from datetime import datetime, time, timedelta
from uuid import UUID

app = FastAPI(title='teste FastAPI', version='0.1.1', description='Uma Api de teste',)


# Definindo parametros prédefinidos
class ModelName(str, Enum):
    alexnet = 'alexnet'
    restnet = 'restnet'
    lenet = 'lenet'


@app.get('/models/{model_name}')
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {'model_name': model_name, 'message': 'deep learning'}
    elif model_name.value == 'lenet':
        return {'mode_name': model_name, 'message': 'LeCCN all the images'}
    else:
        return {'model_name': model_name, 'message': 'have some residual'}


# rota async
@app.get('/')
async def root():
    return {'message': 'hello Word'}


# parametro de rota com tipos
@app.get('/items/{item_id}')
async def read_item(item_id: int):
    return {'item_id': item_id}


# rota post
@app.post('/nome/{name}')
def name(name):
    return {'your name': name}


# parametros de Query

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get('/items/')
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]


# parametros de Query opcionais
@app.get("/items2/{item_id}")
async def read_item2(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


# Parametros de Query com conversão
@app.get('/items3/{item_id}')
async def read_item3(item_id: str, q: str | None = None, short: bool = False):
    item = {'item_id': item_id}
    if q:
        item.update({'q': q})
    if not short:
        item.update(
            {'Description': 'This is amazing item'}
        )
    return item


# Multiple path and query parameters
@app.get('/users/{user_id}/items/{item_id}')
async def read_user_item(
        user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {'item_id': item_id, 'owner_id': user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# Required query parameters
@app.get('/items4/{item_id}')
def read_user_item2(item_id: str, needy: str):
    item = {'item_id': item_id, 'needy': needy}
    return item


@app.get("/items5/{item_id}")
async def read_user_item3(
        item_id: str, needy: str, skip: int = 0, limit: int | None = None
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item


# Request Body

class Item(BaseModel):
    name: str
    description: str | None = Field(None, title='the description of item', max_length=300)
    price: float = Field(..., gt=0, description='the price must be greate than zero')
    tax: float | None = None


# Post with the model
@app.post('/items/')
async def create_item(item: Item):
    return item


# Using the Model
@app.post('/items2/')
async def create_item2(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({'price_with_tax': price_with_tax})
    return item_dict


# Request body + path parameters
@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}


# Request body + path + query parameters
@app.put("/items2/{item_id}")
async def create_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result


# Aditional validation to query parameters

@app.get('/items6')
async def read_items6(q: str | None = Query(None, min_length=3, max_length=50, regex="^fixedquery$")):
    # async def read_items(q: str = Query("fixedquery", min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Paramentro Obrigatorio usando o Query
@app.get('/items7')
async def read_items(q: str = Query(..., min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get('/items8')
async def read_items8(q: Optional[List[str]] = Query(None)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get('/items9')
async def read_items9(q: List[str] = Query(
    ['foor', 'bar'],
    title="Query string",
    description="Query string for the items to search in the database that have a good match",
    alias="item-query",
    deprecated=True, )):
    # async def read_items9(q: list = Query([])):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Path Parameters
@app.get('/items10/{item_id}')
async def read_item10(
        item_id: int = Path(..., title="The ID of the item to get", description='agluglu'),
        q: str | None = Query(None, alias="item-query")
):
    result = {'item_id': item_id}
    if q:
        result.update({'q': q})
    return result


# Number validations: greater than or equal
"""
Tipos de Validação de Números
g = greater
e = equal
t = than
l = less

ge = greater or equal
le = less or equal
e = equal
gt =  greater than
"""


@app.get("/items11/{item_id}")
async def read_items11(
        *, item_id: int = Path(..., title="The ID of the item to get", gt=0, le=1000), q: str
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


# Floats greater than and less than

@app.get('/items12/{item_id}')
async def read_item12(
        *,
        item_id: int = Path(..., title='The Id of the item to get', gt=0, le=1000),
        q: str,
        size: float = Query(..., gt=0, lt=10.5)
):
    result = {'item_id': item_id}
    if q:
        result.update({'q': q})
    return result


# mix Path, query and Body parameters

@app.put('/items13/{item_id}')
async def update_item13(
        *,
        item_id: int = Path(..., title='The Id of the item to get', gt=0, le=1000),
        q: str | None = None,
        item: Item | None = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results


# Multiple body parameters

class User(BaseModel):
    username: str
    full_name: str | None = None


@app.put("/items14/{item_id}")
async def update_item14(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results


# Singular values in body
@app.put("/items15/{item_id}")
async def update_item(
        item_id: int, item: Item,
        user: User = Body(..., title="Usuario", description='O usuario que está fazendo a operação'),
        importance: int = Body(..., title='1alguma coisa', description='abccs')
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results


# Multiple body params and query
@app.put("/items16/{item_id}")
async def update_item(
        *,
        item_id: int,
        item: Item,
        user: User,
        importance: int = Body(..., gt=0),
        q: str | None = None
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results


# Embed a single body parameter
@app.put("/items17/{item_id}")
async def update_item(item_id: int, item: Item = Body(..., embed=True)):
    results = {"item_id": item_id, "item": item}
    return results


# body - Nested Models

class Item2(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


@app.put("/items18/{item_id}")
async def update_item(item_id: int, item: Item2):
    results = {"item_id": item_id, "item": item}
    return results


# Set types
"""Para Valores que não se repetem usamos o método Set, ele vai receber os valores duplicados e transformar em valores unícos"""


class Item3(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()  # Valores unicos


@app.put("/items19/{item_id}")
async def update_item(item_id: int, item: Item3):
    results = {"item_id": item_id, "item": item}
    return results


# Nested Models
"""Modelos Mistos, (ou alinhados) servem para trabalhar com Modelos dentro de modelos."""


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item4(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = []
    image: Image | None = None


@app.put("/items20/{item_id}")
async def update_item(item_id: int, item: Item4):
    results = {"item_id": item_id, "item": item}
    return results


# Attributes with lists of submodels

class Item5(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    images: list[Image] | None = None


@app.put("/items21/{item_id}")
async def update_item(item_id: int, item: Item5):
    results = {"item_id": item_id, "item": item}
    return results


# Deeply nested models

class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item5]


@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer


# Bodies of pure lists
@app.post("/images/multiple/")
async def create_multiple_images(images: list[Image]):
    return images


# Bodies of arbitrary dicts
@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
    return weights


# Declare Request Example Data
# Pydantic schema_extra

class Item6(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            },
            'example2': {"name": "Foo",
                         "description": "A very nice Item",
                         "price": 35.4,
                         "tax": 3.2, }
        }


@app.put("/items23/{item_id}")
async def update_item(item_id: int, item: Item6):
    results = {"item_id": item_id, "item": item}
    return results


# Field additional arguments
class Item7(BaseModel):
    name: str = Field(..., example="Foo")
    description: str | None = Field(None, example="A very nice Item")
    price: float = Field(..., example=35.4)
    tax: float | None = Field(None, example=3.2)


@app.put("/items24/{item_id}")
async def update_item(item_id: int, item: Item7):
    results = {"item_id": item_id, "item": item}
    return results


# Body with example
class Item8(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.put("/items25/{item_id}")
async def update_item(
        item_id: int,
        item: Item8 = Body(
            ...,
            example={
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            },
        ),
):
    results = {"item_id": item_id, "item": item}
    return results


# Body with multiple examples

class Item9(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.put("/items26/{item_id}")
async def update_item(
        *,
        item_id: int,
        item: Item9 = Body(
            ...,
            examples={
                "normal": {
                    "summary": "A normal example",
                    "description": "A **normal** item works correctly.",
                    "value": {
                        "name": "Foo",
                        "description": "A very nice Item",
                        "price": 35.4,
                        "tax": 3.2,
                    },
                },
                "converted": {
                    "summary": "An example with converted data",
                    "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                    "value": {
                        "name": "Bar",
                        "price": "35.4",
                    },
                },
                "invalid": {
                    "summary": "Invalid data is rejected with an error",
                    "value": {
                        "name": "Baz",
                        "price": "thirty five point four",
                    },
                },
            },
        ),
):
    results = {"item_id": item_id, "item": item}
    return results

# Extra Data Types
@app.put("/items27/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: datetime | None = Body(None),
    end_datetime: datetime | None = Body(None),
    repeat_at: time | None = Body(None),
    process_after: timedelta | None = Body(None),
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration,
    }

# Cookie Parameters
@app.get('/items-cookie')
async def read_items(ads_id: str | None = Cookie(None)):
    return {"ads_id": ads_id}


# Header Parameters
@app.get("/items-header/")
async def read_items(user_agent: str | None = Header(None)):
    return {"User-Agent": user_agent}


@app.get("/strange-header/")
async def read_items(
    strange_header: str | None = Header(None, convert_underscores=False)
):
    return {"strange_header": strange_header}


# Duplicate headers
@app.get("/duplicate-headers/")
async def read_items(x_token: list[str] | None = Header(None)):
    return {"X-Token values": x_token}


# Response Model

@app.post("/items-response/", response_model=Item, )
async def create_item(item: Item):
    return item


# Return the same input data
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None

@app.post('/user/', response_model=UserIn)
async def create_user(user:UserIn):
    return user

# Add a output model
class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

@app.post("/user-with-response/", response_model=UserOut)
async def create_user(user: UserIn):
    return user


# Response Model encoding parameters
class Item10(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}

@app.get("/items28/{item_id}", response_model=Item10, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]


# response_model_include and response_model_exclude
items2 = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}

@app.get(
    "/items29/{item_id}/name",
    response_model=Item,
    response_model_include={"name", "description"},
)
async def read_item_name(item_id: str):
    return items2[item_id]


@app.get("/items30/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
async def read_item_public_data(item_id: str):
    return items2[item_id]


# Using lists instead of sets
@app.get(
    "/items31/{item_id}/name",
    response_model=Item,
    response_model_include=["name", "description"],
)
async def read_item_name(item_id: str):
    return items2[item_id]



# https://pydantic-docs.helpmanual.io/usage/types/
# https://medium.com/data-hackers/como-criar-a-sua-primeira-api-em-python-com-o-fastapi-50b1d7f5bb6d