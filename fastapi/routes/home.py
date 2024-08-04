
from typing import Annotated
from fastapi import APIRouter, Depends, Request
from loguru import logger
from sqlalchemy import select
from database.base import get_session
from sqlalchemy.ext.asyncio.session import AsyncSession
from database.models import Product, User
from utils import get_current_user
from templates import templates
from fastapi.responses import HTMLResponse


router = APIRouter()

@router.post("/")
@router.get("/", response_class=HTMLResponse)
async def index(
    request: Request,
    user: Annotated[User, Depends(get_current_user), None],
    session: AsyncSession = Depends(get_session),
    ):
    """Роут главной страницы

    Args:
        request (Request): _description_
        user (Annotated[str, Depends): _description_
        session (AsyncSession, optional): _description_. Defaults to Depends(get_session).

    """
    q = await session.execute(select(Product).limit(3))
    products = q.scalars()
    return templates.TemplateResponse(
        request=request, name="index.html", context={
            "user": user,
            "products": products
        }
)
    
