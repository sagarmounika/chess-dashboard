from fastapi import FastAPI, Depends, HTTPException,status
import berserk
from app.api.auth import router as auth_router
from app.api.players import router as chess_router
from app.security import hash_password, verify_password
app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(chess_router, prefix="/chess", tags=["Chess"])

