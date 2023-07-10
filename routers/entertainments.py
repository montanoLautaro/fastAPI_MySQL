from fastapi import APIRouter, HTTPException, status
from db.schemas.entertainment import EntertainmentBase
from db.models.models import Entertainment
from db.config.client import db_dependency

router = APIRouter(prefix="/entertainments",
                   tags=["Entertainments"],
                   responses={404: {"message": "No encontrado."}})


@router.get("/", description="Get all entertainments")
async def find_all_entertainments(db: db_dependency):
    users = db.query(Entertainment).all()
    if users is None:
        raise HTTPException(status_code=204)
    return users


@router.post("/{user_id}", status_code=status.HTTP_201_CREATED, description="Create a new entertainment")
def create_user(entertainment: EntertainmentBase, user_id: str, db: db_dependency):
    try:
        db_entertainment = Entertainment(
            **entertainment.dict(), user_id=user_id)
        db.add(db_entertainment)
        db.commit()
        return search_entertainment_by_title(db_entertainment.title, db)
    except:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="No se pudo guardar el registro."
        )


def search_entertainment_by_title(title: str, db: db_dependency):
    if title is None:
        raise HTTPException(status_code=204)
    result = db.query(Entertainment).filter(
        Entertainment.title == title).first()
    return result
