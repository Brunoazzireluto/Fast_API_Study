from typing import List, Optional
from fastapi import FastAPI, Query, Path
from enum import Enum

from pydantic import BaseModel

app = FastAPI(title='teste FastAPI', version='0.1.1', description='Uma Api de teste')

#Definindo parametros prédefinidos
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

#rota async
@app.get('/')
async def root():
    return {'message': 'hello Word'}

#parametro de rota com tipos
@app.get('/items/{item_id}')
async def read_item(item_id: int):
    return {'item_id': item_id}

#rota post
@app.post('/nome/{name}')
def name(name):
    return {'your name': name}


#parametros de Query

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get('/items/')
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip+limit]

#parametros de Query opcionais
@app.get("/items2/{item_id}")
async def read_item2(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

#Parametros de Query com conversão
@app.get('/items3/{item_id}')
async def read_item3(item_id: str, q: str | None=None, short: bool = False ):
    item = {'item_id': item_id}
    if q:
        item.update({'q':q})
    if not short:
        item.update(
            {'Description': 'This is amazing item'}
        )
    return item

#Multiple path and query parameters
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

#Required query parameters
@app.get('/items4/{item_id}')
def read_user_item2(item_id: str, needy: str):
    item = {'item_id': item_id, 'needy':needy}
    return item

@app.get("/items5/{item_id}")
async def read_user_item3(
    item_id: str, needy: str, skip: int = 0, limit: int | None = None
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item

#Request Body

class Item(BaseModel):
    name: str
    description: str | None = None
    price : float
    tax : float | None = None


#Post with the model
@app.post('/items/')
async def create_item(item:Item):
    return item

#Using the Model
@app.post('/items2/')
async def create_item2(item:Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price+item.tax
        item_dict.update({'price_with_tax': price_with_tax})
    return item_dict

#Request body + path parameters
@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}

#Request body + path + query parameters
@app.put("/items2/{item_id}")
async def create_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result

#Aditional validation to query parameters

@app.get('/items6')
async def read_items6(q: str  | None = Query(None, min_length=3 ,max_length=50, regex="^fixedquery$" )):
#async def read_items(q: str = Query("fixedquery", min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


#Paramentro Obrigatorio usando o Query
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

#Path Parameters
@app.get('/items10/{item_id}')
async def read_item10(
    item_id: int = Path(..., title="The ID of the item to get", description='agluglu'),
    q: str |  None = Query(None, alias="item-query")
):
    result = {'item_id': item_id}
    if q:
        result.update({'q':q})
    return result

#Number validations: greater than or equal
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


#https://fastapi.tiangolo.com/pt/tutorial/path-params-numeric-validations/#number-validations-floats-greater-than-and-less-than