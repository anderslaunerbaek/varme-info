import bcrypt
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from .models import UserModel


def create_hashpw(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def create_user(email: str, password: str) -> UserModel:
    hashed = create_hashpw(password)
    return UserModel(email=email, hashed_password=hashed)


def verify_login(
    engine: Engine, email: str, password: str
) -> tuple[bool, UserModel | None]:
    with Session(engine) as session:
        rec = session.query(UserModel).where(UserModel.email == email).first()

    if rec is None:
        return False, None

    return bcrypt.checkpw(password.encode(), rec.hashed_password.encode()), rec
