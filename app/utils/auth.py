
from jose import jwt, JWTError
from datetime import datetime, timedelta
from passlib.context import CryptContext
from typing import Optional
from fastapi import HTTPException, Header
from app.utils.config import Config
from typing import Union, Dict

# # Configuration for JWT
# SECRET_KEY = "your_secret_key"  # Replace with a secure key.
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Hash the password using bcrypt algorithm."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify the plain password against the stored hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

# def create_access_token(data: dict) -> str:
#     """
#     Create a JWT access token.

    
#     """
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# def validate_token(token: str) -> dict:
#     """
#     Validate the Bearer token and decode its contents.

#     """
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         return payload
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid or expired token.")




def create_access_token(data: dict) -> str:
    """
    Generate an access token with an expiration time.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Config.JWT_SECRET_KEY, algorithm=Config.ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    """
    Generate a refresh token with a longer expiration time.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=Config.REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Config.JWT_REFRESH_SECRET_KEY, algorithm=Config.ALGORITHM)
    return encoded_jwt

def validate_access_token(token: str) -> Union[Dict, None]:
    """
    Validate and decode an access token.
    """
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=[Config.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired access token.")

def validate_refresh_token(token: str) -> Union[Dict, None]:
    """
    Validate and decode a refresh token.
    """
    try:
        payload = jwt.decode(token, Config.JWT_REFRESH_SECRET_KEY, algorithms=[Config.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token.")

def get_bearer_token(authorization: Optional[str] = Header(None)) -> str:
    """
    Extract and validate the Bearer token from the Authorization header.
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing.")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header format.")
    return authorization[len("Bearer "):]