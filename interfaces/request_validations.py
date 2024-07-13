from pydantic import BaseModel, field_validator, EmailStr, ValidationError


class SignUpValidator(BaseModel):
    username : str
    email : EmailStr
    password : str


class VerifyOtp(BaseModel):
    id : int
    otp : int


class VerifyOtpChangePassword(BaseModel):
    token : str
    id :int
    otp : int
    password : str


class SignIn(BaseModel):
    username : str
    password : str

class PasswordChange(BaseModel):
    token : str
    email : EmailStr

class Token(BaseModel):
    token : str