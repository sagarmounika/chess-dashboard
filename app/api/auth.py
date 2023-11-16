from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin,TokenSchema
from app.db.session import get_db
from app.db.base import SessionLocal
from app.models.user import User,TokenTable
from app.security import hash_password, verify_password , create_jwt_token
from fastapi.security import OAuth2PasswordBearer
import jwt
router = APIRouter()

@router.post("/signup", response_model=dict)
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User registered successfully"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/login", response_model=dict)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user and verify_password(user.password, db_user.hashed_password):
        token = create_jwt_token(user_id=db_user.id)
        token_db = TokenTable(user_id=db_user.id,  access_token=token,status=True)
        db.add(token_db)
        db.commit()
        return {"token": token, "message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid credentials")
