from typing import Annotated, List, Union
from pydantic import BaseModel
from fastapi import Form


class PydanticUser(BaseModel):
    username: str = Form(...)
    password: str = Form(...)


class PydanticProduct(BaseModel):
    name: str = Form(...)
    articule: str = Form(...)
    description: str =Form(...)
    price: str = Form(...)
    photo: str = Form()

class PydanticProductUpdate(BaseModel):
    name: Union[str, None] = ""
    articule: Union[str, None] = ""
    description: Union[str, None] = ""
    price: Union[float, None] = None
    photo: Union[str, None] = "" 


class PydanticProductsArray(BaseModel):
    prodcuts: List[PydanticProduct]