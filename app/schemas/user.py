from pydantic import BaseModel
import datetime
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class TokenSchema(BaseModel):
    access_token: str

class TokenCreate(BaseModel):
    user_id:str
    access_token:str
    status:bool
    created_date:datetime.datetime
