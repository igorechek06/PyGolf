import database as db
import jwt
from fastapi import Header, HTTPException
from settings import settings


def auth(x_token: str | None = Header(None)) -> db.User:
    if x_token is None:
        raise HTTPException(401, "Не авторизованная сессия")
    else:
        data = jwt.decode(x_token, options={"verify_signature": False})

    with db.session.begin() as session:
        user = session.get(db.User, data["sub"])
        if user is None:
            raise HTTPException(401, "Сессия не действительна")
        else:
            try:
                jwt.decode(x_token, settings.secret + user.password, algorithms=["HS256"])
            except jwt.exceptions.InvalidSignatureError:
                raise HTTPException(401, "Сессия не действительна")
            session.expunge(user)
            return user
