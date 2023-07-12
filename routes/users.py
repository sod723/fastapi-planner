from typing import List
from fastapi import APIRouter, HTTPException, status
from models.users import User, UserSignIn
from database.connection import Database
from auth.hash_password import HashPassword

user_router = APIRouter(
    tags=["User"],
)

user_database = Database(User)
hash_password = HashPassword()

#회원가입 ("/signup")
@user_router.post("/signup")
async def signup(user: User) -> dict:
    user_exist = await User.find_one(User.email == user.email)
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already exists"
        )
    hashed_password = hash_password.create_hash(user.password)
    user.password = hashed_password
    await user_database.save(user)
    return {"message": "User created successfully"}

#로그인  (/signin)
@user_router.post("/signin")
async def signin(data: UserSignIn) -> dict:
    user_exist = await User.find_one(User.email == data.email)
    if user_exist is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if user_exist.password != data.password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
        )
    return {"message": "User logged in successfully"}

#모든 사용자 이메일, 패스워드, 태그 출력
@user_router.get("/findall")
async def get_all_users() -> List[dict]:
    users = await User.find_all().to_list() #비동기연산
    return [user.dict() for user in users]

@user_router.get("/", response_model=List[User])
async def get_all_users2() -> List[User]:
    users = await user_database.get_all()
    return users