from fastapi import APIRouter, Depends, HTTPException
from starlette import BaseModel
from dependencies import auth
import database as db
import models as m


class PushScoreData(BaseModel):
    score: int


router = APIRouter(prefix="/scores", tags=["scores"])


@router.get("/{level_id}")
async def get_top_scores(
    level_id: int,
    limit: int = 10,
    offset: int = 0,
) -> list[m.Score]:
    if limit > 10:
        raise HTTPException(400, "limit должен быть <=10")
    with db.session() as session:
        query = (
            session.query(db.Score)
            .filter(db.Score.level_id == level_id)
            .order_by(db.Score.score.asc())
            .offset(offset)
            .limit(limit)
        )

        return [m.Score.from_orm(o) for o in query.all()]
    pass


@router.get("/{level_id}")
async def push_score(
    level_id: int,
    score_data: PushScoreData,
    user: db.User = Depends(auth),
) -> None:
    with db.session.begin() as session:
        level = session.get(db.Level, level_id)
        if level is None:
            raise HTTPException(404, "Уровень не найден")

        score = (
            session.query(db.Score)
            .filter(db.User.id == user.id and db.Level.id == level.id)
            .one_or_none()
        )

        if score is None:
            score = db.Score(
                user_id=user.id,
                level_id=level.id,
                score=score,
            )
            session.add(score)
        else:
            if score_data.score > score.score:
                session.add(score)
                score.score = score_data.score
