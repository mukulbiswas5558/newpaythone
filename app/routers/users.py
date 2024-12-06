from fastapi import APIRouter, HTTPException,Depends
from app.models.user_model import CreateUser, LoginUser,UpdateUser
from app.services.user_service import (
    create_user_service,
    login_user_service,
    update_user_service,
  
)
from pydantic import BaseModel

from app.utils.auth import get_bearer_token, validate_access_token

router = APIRouter()


# @router.post("/", response_model=User)
# async def create_user(user: User):
#     return await create_user_service(user)

@router.post("/auth/register")
async def create_user(user: CreateUser):
    try:

        # Pass the user to the service to save
        return await create_user_service(user)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
@router.post("/auth/login")
async def login_user(user: LoginUser):
    try:
        data = await login_user_service(user)
        
        return data

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

# @router.put("/update")
# async def update_user(
#     token: str = Depends(get_bearer_token)
# ):
#     try:
#         payload = validate_token(token)
#         print(f"Decoded Token: {payload}")
#         return {"message": "User updated successfully.", "user": payload}
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         print(f"Unexpected Error: {str(e)}")
#         raise HTTPException(status_code=500, detail="An unexpected error occurred.")



@router.put("/update")
async def update_user(
    user: UpdateUser,
    token: str = Depends(get_bearer_token)
):
    """
    Updates a user's details after validating the JWT token.
    """
    try:
        # Validate the token
        payload = validate_access_token(token)
        print(f"Decoded Token: {payload}")

        # Extract username from the token payload
        username = payload.get("username")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token payload. Username not found.")

        # Call the service to update the user
        result = await update_user_service(username, user)
        return result
    
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
