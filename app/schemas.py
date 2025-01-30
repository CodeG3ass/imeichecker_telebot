from pydantic import BaseModel

class IMEIRequest(BaseModel):
    imei: str
    token: str

class IMEIResponse(BaseModel):
    status: str
    data: dict

class WhitelistUserRequest(BaseModel):
    user_id: int

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None