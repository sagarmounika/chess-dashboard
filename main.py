from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.players import router as chess_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def read_root():
    return "Welcome to Chess Dashboard"

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(chess_router, prefix="/chess", tags=["Chess"])

