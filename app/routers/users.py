from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer, HTTPAuthorizationCredentials
from app.database import SessionLocal
from app.models import User
from app.auth import hash_password, verify_password, create_access_token
from pydantic import BaseModel

router = APIRouter()

oauth2_scheme = HTTPBearer()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

@router.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    return {"message": "Access granted", "token": token}

@router.post("/register")
def register_user(user: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
        credits=5
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}

# Step 2: Change login route to use OAuth2PasswordRequestForm
@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == form_data.username).first()
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}

# Step 3: Create a protected test route
@router.get("/me")
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    return {"message": "You're authorized!", "token": credentials.credentials}

