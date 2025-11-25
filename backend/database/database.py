from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel, select

from crud.user import create_user
from models.user import User, UserCreate

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def initialize_database(session: Session) -> None:
    SQLModel.metadata.create_all(engine)

    user = session.exec(select(User).where(User.email == "admin@gmail.com")).first()
    if not user:
        user_in = UserCreate(
            name="Admin",
            surname="Admin",
            age=40,
            email="admin@gmail.com",
            password="admin_password",
            is_superuser=True,
        )
        user = create_user(session=session, user_create=user_in)
