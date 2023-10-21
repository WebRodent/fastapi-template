import logging
from typing import List

from fastapi import Depends, FastAPI
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.config import get_config
from app.database.engine import get_db
from app.database.users import create_user, get_user, get_users
from app.schemas import User, UserRegister

config = get_config()
print(config.DATABASE_URL)
logging.basicConfig(level=config.LOG_LEVEL, format=config.LOG_FORMAT)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="template-api", version="1.0", description="API setup as simple as possible"
)


@app.get(
    "/",
    name="docs",
    description="Redirects to the docs",
    response_class=RedirectResponse,
    tags=["docs"],
)
def docs_redirect():
    return RedirectResponse("/docs")


@app.post(
    "/users/",
    name="create_user",
    description="Creates a new user",
    response_model=User,
    tags=["users"],
)
def create_user_endpoint(user: UserRegister, session: Session = Depends(get_db)):
    """
    Endpoint to create a new user.

    Args:
        user (UserRegister): The user data to create.
        session (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        User: The created user.
    """
    logger.debug(f"database url: {config.DATABASE_URL}")
    return create_user(session, user)


@app.get(
    "/users/",
    name="get_users",
    description="Gets all users",
    response_model=List[User],
    tags=["users"],
)
def get_users_endpoint(session: Session = Depends(get_db), limit: int = 100):
    return get_users(session, limit)


@app.get(
    "/users/{user_id}",
    name="get_user",
    description="Gets a user by id",
    response_model=User,
    tags=["users"],
)
def get_user_endpoint(user_id: int, session: Session = Depends(get_db)):
    return get_user(session, user_id)
