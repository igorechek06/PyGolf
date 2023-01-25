import secrets

import database as db
import dependencies
import jwt
import models as m
import utils
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from settings import settings

router = APIRouter(prefix="/user", tags=["users"])


class User(BaseModel):
    username: str
    password: str


class Username(BaseModel):
    username: str


class Password(BaseModel):
    password: str


@router.post("/register")
async def register(register: User) -> None:
    if not register.username:
        raise HTTPException(400, "Имя не может быть пустым")
    if not register.password:
        raise HTTPException(403, "Пароль не может быть пустым")

    salt = secrets.token_hex(8)
    password_hash = utils.hash(register.password, salt)

    with db.session.begin() as session:
        if (
            session.query(db.User).filter(db.User.username == register.username).count()
            > 0
        ):
            raise HTTPException(403, "Имя занято другим пользователем")

        session.add(
            db.User(
                username=register.username,
                password=password_hash,
                salt=salt,
            )
        )


@router.post("/login")
async def login(login: User) -> str:
    with db.session.begin() as session:
        user = (
            session.query(db.User)
            .filter(db.User.username == login.username)
            .one_or_none()
        )
        if user is None:
            raise HTTPException(401, "Неверное имя пользователя или пароль")

        if user.password == utils.hash(login.password, user.salt):
            return jwt.encode(
                {"sub": user.id},
                settings.secret + user.password,
            )
        else:
            raise HTTPException(401, "Неверное имя пользователя или пароль")


@router.get("/get/{id}")
async def get(id: int) -> m.User | None:
    with db.session.begin() as session:
        user = session.get(db.User, id)
        if user is not None:
            return m.User.from_orm(user)
        else:
            return None


@router.get("/me")
async def me(user: db.User = Depends(dependencies.auth)) -> m.User:
    return m.User.from_orm(user)


@router.put("/update/username")
async def update_username(
    update: Username,
    user: db.User = Depends(dependencies.auth),
) -> None:
    if not update.username:
        raise HTTPException(400, "Имя не может быть пустым")

    with db.session.begin() as session:
        if (
            session.query(db.User).filter(db.User.username == update.username).count()
            > 0
        ):
            raise HTTPException(403, "Имя занято другим пользователем")

        session.add(user)
        user.username = update.username


@router.put("/update/password")
async def update_password(
    update: Password,
    user: db.User = Depends(dependencies.auth),
) -> None:
    if not update.password:
        raise HTTPException(400, "Пароль не может быть пустым")

    with db.session.begin() as session:
        session.add(user)
        user.salt = secrets.token_hex(8)
        user.password = utils.hash(update.password, user.salt)


@router.delete("/delete")
async def delete(user: db.User = Depends(dependencies.auth)) -> None:
    with db.session.begin() as session:
        session.add(user)
        session.delete(user)
