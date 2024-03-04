
from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException

from jwt_manager import validate_token
class JWTBearer(HTTPBearer):

    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        #TODO: leave this validation to the db
        if data["email"] != "test@test.com" or data["password"] != "test": 
            raise HTTPException(status_code=403, detail="invalid credentials")