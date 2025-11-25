import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import select, func

import crud
from api.dependencies import SessionDependency
from models.user import UsersPublic, User, UserPublic, UserCreate

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserPublic)
def create_user(*, session: SessionDependency, user_in: UserCreate) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )

    user = crud.user.create_user(session=session, user_create=user_in)
    return user


@router.get("/", response_model=UsersPublic)
def read_users(session: SessionDependency, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve users.
    """

    count_statement = select(func.count()).select_from(User)
    count = session.exec(count_statement).one()

    statement = select(User).offset(skip).limit(limit)
    users = session.exec(statement).all()

    return UsersPublic(data=users, count=count)


@router.get("/{user_id}", response_model=UserPublic)
def read_user_by_id(user_id: uuid.UUID, session: SessionDependency) -> Any:
    """
    Get a specific user by id.
    """
    user = session.get(User, user_id)
    return user
