
from typing import Annotated, Union
from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from loguru import logger
from sqlalchemy import select
from templates import templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio.session import AsyncSession
from database.models import Product, User
from database.base import get_session
from utils import get_admin, get_current_user
from serializer import PydanticProduct, PydanticProductsArray
import aiofiles

router = APIRouter()

@router.post("/catalog")
@router.get("/catalog", response_class=HTMLResponse)
async def read_item(
    request: Request,
    user: Annotated[str, Depends(get_current_user), None],
    sort: str = "date",
    session: AsyncSession = Depends(get_session),
    ):
    if sort == "price":
        q = await session.execute(select(Product).order_by(Product.price.asc()))
    else:
        q = await session.execute(select(Product).order_by(Product.date.desc()))
    
    products = q.scalars()
    return templates.TemplateResponse(
        request=request, name="shop.html", context={
            "user": user,
            "products": products
        }
)


@router.get('/products/add')
async def add_product(
    request: Request,
    user: Annotated[User, Depends(get_admin)],
    session: AsyncSession = Depends(get_session),
    ):
    return templates.TemplateResponse(
        request=request, name="add_product.html",
        context={
            "success": False
        }
    )
    

@router.post("/add_product_action")
async def add_product_act(
    user: Annotated[User, Depends(get_current_user)],
    name: Annotated[str, Form()],
    articule: Annotated[str, Form()],
    description: Annotated[str, Form()],
    price: Annotated[str, Form()],
    request: Request,
    photo: UploadFile,
    session: AsyncSession = Depends(get_session),
    ):
    q = await session.execute(select(Product).where(Product.articule == articule))
    exist = q.scalar_one_or_none()
    if exist:
        return templates.TemplateResponse(
        request=request, name="add_product.html",
        context={
            "success": False,
            "error": "Артикул уже существует"
        })
    product = Product()
    product.name = name
    product.articule = articule
    product.description = description
    product.price = price
    path = f"images/{photo.filename}"
    async with aiofiles.open(path, 'wb') as out_file:
        content = await photo.read()  # async read
        await out_file.write(content)  # async write
    # product.photo = photo
    product.photo = path
    
    
    session.add(product)
    await session.commit()
    
    return  templates.TemplateResponse(
        request=request, name="add_product.html",
        context={
            "success": True
        }
    )

@router.get("/product/delete/{id}")
async def delete_product(
    request: Request,
    id: str,
    user: Annotated[User, Depends(get_admin)],
    session: AsyncSession = Depends(get_session),
    ):
    product = await session.get(Product, id)
    # logger.debug(product)
    await session.delete(product)
    await session.commit()
    return RedirectResponse("/catalog")

@router.get("/product/{id}")
async def product(
    request: Request,
    id: str,
    user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
    ):
    product = await session.get(Product, id)
    
    return  templates.TemplateResponse(
        request=request, name="shop-single.html",
        context={
            "product": product,
            "user": user
        }
    )

@router.post("/delete_by_art")
async def delete_by_atr(
    art: Annotated[str, Form()],
    session: AsyncSession = Depends(get_session),
):
    q = await session.execute(select(Product).where(Product.articule==art))
    product = q.scalar_one_or_none()
    
    if product:
        await session.delete(product)
        await session.commit()
    return RedirectResponse("/catalog")
    
