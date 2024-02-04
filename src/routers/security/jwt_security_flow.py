import os
from datetime import timedelta, datetime
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from typing import Annotated
from src.exceptions.security_exceptions import CREDENTIALS_EXCEPTION
from src.schemas.user_pydantic_model import User as UserPydanticModel
from src.schemas.token_pydantic_model import Token
from src.config.database import local_session
from src.models.users import User as UserDBModel

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

security_router = APIRouter(prefix="/auth", tags=["SECURITY AUTH"])

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


def authenticate_user(db, username: str, password: str) -> UserPydanticModel:
    user = db.query(UserDBModel).filter(username == UserDBModel.username).first()

    if not user:
        return False
    
    if not bcrypt_context.verify(password, user.password):
        return False
    
    return user


def create_access_token(username: str, id: int, token_expires: timedelta):
    """ Generate token. """
    encode = {"sub": username, "id": id, "exp": datetime.utcnow() + token_expires}

    return jwt.encode(encode, key=SECRET_KEY, algorithm=ALGORITHM)


@security_router.post("/", status_code=201)
def create_user(db: db_dependency, new_user: UserPydanticModel):
    """ Create a new user. """
    new_user_to_db = UserDBModel(username= new_user.username, password=bcrypt_context.hash(new_user.password))

    db.add(new_user_to_db)
    db.commit()

    return JSONResponse(content={"message":"Nuevo usuario creado!"}, status_code=201)


@security_router.post("/token", response_model=Token)
def jwt_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    """ Retorna token único de cada usuario. """
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise CREDENTIALS_EXCEPTION
    
    print("\n", user, type(user), "\n")
    
    access_token = create_access_token(user.username, user.user_id, timedelta(minutes=30))

    return {"access_token": access_token, "token_type": "bearer"}

