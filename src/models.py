from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class Error(BaseModel):
    status: int
    detail: str

class LoginSuccessful(BaseModel):
    message: str
    data: Token

