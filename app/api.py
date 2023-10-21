from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, create_user, get_user

app = FastAPI(
    title="template-api",
    version="1.0",
    description="API setup as simple as possible",
)

@app.get("/")
def docs_redirect():
    return RedirectResponse(f"/docs")


@app.post("/users/")
def create_user_endpoint(user: UserRegister, db: Session = Depends(SessionLocal)):
    return create_user(db, user)

@app.get("/users/{user_id}")
def get_user_endpoint(user_id: int, db: Session = Depends(SessionLocal)):
    return get_user(db, user_id)