import secrets
from typing import Annotated
from fastapi import APIRouter, Depends, Form, HTTPException, Header, Request, Response, status
from fastapi.responses import RedirectResponse
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from database.base import get_session
from database.models import Token, User
from utils import get_current_user
from serializer import PydanticUser
from loguru import logger
from templates import templates


router = APIRouter()


@router.post("/authorize")
async def login_for_access_token(
    response: Response,
    request: Request,
    username: Annotated[str, Form()], password: Annotated[str, Form()],
    session: AsyncSession = Depends(get_session),
    ):
    """Эндпоинт для получения токена

    Args:
        form_data (PydanticUser)
        request (Request): 
        session (AsyncSession, optional): Defaults to Depends(get_session).
    """
    q = await session.execute(select(User).where(User.username==username))
    user = q.scalar_one_or_none()
    if user:
        q = await session.execute(select(Token).where(Token.user==user.id))
        token = q.scalar_one_or_none()
        if user.password == password:
            if token:
                r = RedirectResponse("/")
                r.set_cookie("Authorization", token.token)
                return r

            token = secrets.token_urlsafe(16)
            token_object = Token()
            token_object.token = token
            token_object.user = user.id
            session.add(token_object)
            await session.commit()
            response.set_cookie("Authorization", token)

            r = RedirectResponse("/")
            r.set_cookie("Authorization", token)
            return r
        return templates.TemplateResponse(
                    request=request, name="login.html", context={"errors": "Неверные имя пользователя или пароль"}
                )
    else:
        return templates.TemplateResponse(
                    request=request, name="login.html", context={"errors": "Неверные имя пользователя или пароль"}
                )


# @router.post("/register")
# async def register(
#     data: PydanticUser,
#     session: AsyncSession = Depends(get_session)
#     ):
#     q = await session.execute(select(User).where(User.username==data.username))
#     user = q.scalar_one_or_none()
#     if user:
#         return {"message":"already registred"}
#     user = User()
#     user.password = data.password
#     user.username = data.username
#     session.add(user)
#     await session.commit()
#     return {
#         "username": data.username,
#         "password": data.password
#     }
    



# @router.patch("/auth/token")
# async def update_token(
#         user: Annotated[str, Depends(get_current_user)],
#         Authorization: Annotated[str, Header()],
#         session: AsyncSession = Depends(get_session),
#     ):
#     """Хэндлер перевыпуска токена

#     Args:
#         user (Annotated[str, Depends): Объект пользователя
#         Authorization (Annotated[str, Header): Хедер авторизации
#         session (AsyncSession, optional): Defaults to Depends(get_session).

#     Returns:
#         _type_: _description_
#     """
#     q = await session.execute(select(Token).where(Token.token==Authorization))
#     token = q.scalar_one_or_none()
#     if token:
#         await session.delete(token)
#     token = Token()
#     token.token = secrets.token_urlsafe(16)
#     token.user = user.id
    
#     session.add(token)
#     await session.commit()
    
#     return {"token": token.token}


@router.get("/login")
async def login(request: Request):
    """Роут шаблона авторизации

    Args:
        request (Request): _description_
    """
        
    return templates.TemplateResponse(
        request=request, name="login.html"
)
    

# @router.post("/authorize")
# async def authorize(
#         request: Request,
#         username: Annotated[str, Form()], password: Annotated[str, Form()],
#         session: AsyncSession = Depends(get_session),
#     ):
#     q = await session.execute(select(User).where(User.username == username))
#     user = q.scalar_one_or_none()
#     if user:
        
    