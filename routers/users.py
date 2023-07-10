from fastapi import APIRouter, HTTPException, status
from db.schemas.user import UserBase, CreateUserBase
from passlib.context import CryptContext
from db.models.models import User
from db.config.client import db_dependency


router = APIRouter(prefix="/users",
                   tags=["users"],
                   responses={404: {"message": "No encontrado."}})

crypt = CryptContext(schemes=["bcrypt"])


@router.get("/", description="Get all users")
async def find_all_users(db: db_dependency):
    users = db.query(User).all()
    if users is None:
        raise HTTPException(status_code=204)
    return users


@router.get("/{user_id}", status_code=status.HTTP_200_OK, description="Get user by id")
async def get_user(user_id: int, db: db_dependency):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        user_not_found()
    return user


@router.post("/", status_code=status.HTTP_201_CREATED, description="Create a new user")
def create_user(user: CreateUserBase, db: db_dependency):
    try:
        db_user = User(**user.dict())
        db_user.password = crypt.hash(db_user.password)
        db.add(db_user)
        db.commit()
        return search_user_by_email(db_user.email, db)
    except:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="No se pudo crear el usuario."
        )


@router.get("/account/{email}", status_code=status.HTTP_200_OK, description="Get user by email")
async def get_user_by_email(user_email: str, db: db_dependency):
    user = search_user_by_email(user_email, db)
    if user is None:
        raise HTTPException(status_code=204)
    return user


@router.post("/disable-account/{id}", status_code=status.HTTP_200_OK, description="Disable user")
async def disable_user(user_id: str, db: db_dependency):
    try:
        db_user = search_user_by_id(user_id, db)
        if db_user is None:
            user_not_found()
        db_user.is_active = False
        db.commit()
        return search_user_by_email(db_user.email, db)
    except:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="No se pudo desactivar al usuario."
        )


@router.post("/activate-account/{id}", status_code=status.HTTP_200_OK, description="Activate user")
async def activate_user(user_id: str, db: db_dependency):
    try:
        db_user = search_user_by_id(user_id, db)
        if db_user is None:
            user_not_found()
        db_user.is_active = True
        db.commit()
        return search_user_by_email(db_user.email, db)
    except:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="No se pudo activar al usuario."
        )


# TEMPORAL
@router.put("/{id}", status_code=status.HTTP_200_OK, description="Update all data of user")
def update_user(user_id: str, new_user: UserBase, db: db_dependency):
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user is None:
            user_not_found()
        db_user.email = new_user.email
        db_user.full_name = new_user.full_name
        db_user.password = crypt.hash(new_user.password)
        db_user.is_active = new_user.is_active
        db.commit()
    except:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="No se pudo crear el usuario."
        )


# TEMPORAL
@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT, description="Delete user from db")
async def delete_user(user_id: str, db: db_dependency):
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user is None:
            user_not_found()
        db.delete(db_user)
        db.commit()
    except:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="No se pudo elminar el usuario."
        )


def search_user_by_email(user_email: str, db: db_dependency):
    if user_email is None:
        raise HTTPException(
            status_code=204, detail="El usuario no es válido.")
    result = db.query(User).filter(User.email == user_email).first()
    return result


def search_user_by_id(user_id: str, db: db_dependency):
    if user_id is None:
        raise HTTPException(
            status_code=204, detail="El usuario no es válido.")
    result = db.query(User).filter(User.id == user_id).first()
    return result


def user_not_found():
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT, detail="El usuario no existe.")
