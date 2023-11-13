import logging
from contextlib import asynccontextmanager
from typing import List

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app.config import get_config
from app.database.engine import get_db
from app.database.users import create_user, get_user, get_users
from app.schemas import Task, User, UserRegister
from app.worker import Worker

config = get_config()
logging.basicConfig(level=config.LOG_LEVEL, format=config.LOG_FORMAT)

logger = logging.getLogger(__name__)


class WorkerAPI(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generator: Worker = None

    def startup(self):
        try:
            # Perform any initialization operations
            logger.info("Starting up the app")
            self.generator = Worker(config, get_db())
        except Exception as e:
            # Handle exceptions
            logger.error(f"Could not initialize the app: {e}")

    def shutdown(self):
        if self.generator:
            # Perform any cleanup operations
            self.generator.shutdown()
            logger.info("Shutting down the app")


@asynccontextmanager
async def lifespan_context(app: WorkerAPI):
    app.startup()
    try:
        yield
    finally:
        app.shutdown()


app = WorkerAPI(
    title="template-api",
    version="1.0",
    description="API for the avalue project",
    lifespan=lifespan_context,
)

# FIXME: Bad practice, should be changed to a list of allowed origins,
# also dynamic with APP_ENV
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/main", StaticFiles(directory="public"), name="main")


@app.get("/", name="main", description="Serves the main page", tags=["main"])
def main_page():
    return FileResponse("public/index.html")


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


@app.post(
    "/tasks/add",
    name="add_task",
    description="Adds a list of tasks to the queue",
    tags=["tasks"],
)
def add_task_endpoint(tasks: List[Task]):
    for task in tasks:
        app.generator.add_task(task)
    return {"message": "Tasks added to the queue"}


@app.get(
    "/tasks/start",
    name="start_tasks",
    description="Starts the task generator",
    tags=["tasks"],
)
def start_tasks_endpoint():
    app.generator.start()
    return {"message": "Task generator started"}
