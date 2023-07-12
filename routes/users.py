from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from auth.jwt_handler import create_access_token
from models.users import User, TokenResponse
from database.connection import Database
from auth.hash_password import HashPassword
from auth.authenticate import authenticate

user_router = APIRouter(
    tags=["User"],
)

user_database = Database(User)
hash_password = HashPassword()

#회원가입 ("/signup")
@user_router.post("/signup", response_model=TokenResponse)
async def signup(user: User) -> dict:
    user_exist = await User.find_one(User.email == user.email)
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already exists"
        )
    hashed_password = hash_password.create_hash(user.password)
    user.password = hashed_password
    await user_database.save(user)
    access_token = create_access_token(user=user.email)
    return {"access_token": access_token, "token_type": "bearer"}
    #return {"message": "User created successfully"}

#로그인  (/signin)
@user_router.post("/signin", response_model=TokenResponse)
async def signin(data: OAuth2PasswordRequestForm = Depends()) -> dict:
    user_exist = await User.find_one(User.email == data.username)
    if user_exist is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if hash_password.verify_hash(data.password, user_exist.password):
        access_token = create_access_token(data.username)
        return {"access_token": access_token, "token_type": "Bearer"}

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
    )

#모든 사용자 이메일, 패스워드, 태그 출력
@user_router.get("/findall")
async def get_all_users() -> List[dict]:
    users = await User.find_all().to_list() #비동기연산
    return [user.dict() for user in users]

# @user_router.get("/", response_model=List[User])
# async def get_all_users2() -> List[User]:
#     users = await user_database.get_all()
#     return users


@user_router.get("/", response_model=List[User])
async def get_all_users_admin(user: str = Depends(authenticate)) -> List[User]:  # get method 접속 시 토큰을 통해 인증하도록 설정
    if user != "song@test.pri":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin Only. Access denied."
        )

    users = await user_database.get_all()
    return users