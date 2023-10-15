from __future__ import annotations
from datetime import datetime, timedelta
from typing import Union
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext


class AuthHandler:
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    def getPasswordHash(self, password):
        return self.pwd_context.hash(password)

    def verifyPassword(self, password, hashed_password):
        return self.pwd_context.verify(password, hashed_password)

    def createAccessToken(self, data, expires_delta: Union[timedelta, None] = None):
        # I can also encode dictionaries, make the data have the type of dict
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=1)
        payload = {
            'exp': expire,
            'iat': datetime.utcnow(),
            'sub': data
        }
        encoded_jwt = jwt.encode(payload, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt, expire

    def createRefreshToken(self, data):
        pass

    def decodeToken(self, token: str):

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            username: str = payload.get("sub")
            return username
        except jwt.ExpiredSignatureError:
            credentials_exception.detail = "Token Expired"
            raise credentials_exception
        except:
            credentials_exception.detail = "Invalid Token"
            raise credentials_exception

    def authWrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decodeToken(auth.credentials)
