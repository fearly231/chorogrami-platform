from typing import Any

from sqlmodel import Session, select

from models.user import User, UserCreate, UserUpdate
from security.password import get_password_hash, verify_password


def create_user(*, session: Session, user_create: UserCreate) -> User:
    database_object = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(database_object)
    session.commit()
    session.refresh(database_object)
    return database_object


def update_user(*, session: Session, database_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    database_user.sqlmodel_update(user_data, update=extra_data)
    session.add(database_user)
    session.commit()
    session.refresh(database_user)
    return database_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    database_user = get_user_by_email(session=session, email=email)
    if not database_user:
        return None
    if not verify_password(password, database_user.hashed_password):
        return None
    return database_user
