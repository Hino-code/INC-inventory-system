from app.database.connection import db
from app.models.user_model import UserRegister, UserLogin
from app.utils.jwt_handler import create_access_token
from passlib.context import CryptContext
from fastapi import HTTPException, status

# Setup password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash a plain password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify a plain password against the hashed one
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Register a new user with hashed password
async def register_user(user: UserRegister):
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed_pwd = hash_password(user.password)
    user_dict = user.dict()
    user_dict["password_hash"] = hashed_pwd
    user_dict.pop("password")  # Remove plain password before saving

    result = await db.users.insert_one(user_dict)
    return {"message": "User registered successfully", "user_id": str(result.inserted_id)}

# Authenticate user and return JWT token if valid
async def login_user(user: UserLogin):
    existing_user = await db.users.find_one({"email": user.email})
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not verify_password(user.password, existing_user["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token_data = {
        "user_id": str(existing_user["_id"]),
        "email": existing_user["email"],
        "role": existing_user["role"]
    }

    access_token = create_access_token(token_data)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
