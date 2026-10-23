# Your auth code goes here.
import jwt 
import os 

from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt 

JWT_SECRET = os.environ["JWT_SECRET"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(volunteer_id : int) -> str: 
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub" : str(volunteer_id), 
        "exp" : expire

    }
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)

def get_current_volunteer_id(token : str) -> int:
    credentials_exception = HTTPException(
        status_code = 401, 
        detail = "Invalid or expired token", 
        headers={"WWW-Authenticate" : "Bearer"}
    )
    try: 
        payload = jwt.decode(
            token, JWT_SECRET, algorithms=[ALGORITHM]
        )

        subject = payload.get("sub")
        if subject is None: 
            raise credentials_exception
        return int(subject)

    except (JWTError, ValueError):
        raise credentials_exception

def create_hashed_passwords(password : str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password : str, hashed_password : str) -> str: 
    return pwd_context.verify(plain_password, hashed_password)