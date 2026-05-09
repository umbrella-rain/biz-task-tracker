from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from contextlib import asynccontextmanager
from uuid import uuid4
from fastapi.security import OAuth2PasswordBearer
from security import decode_access_token


from database import engine, get_db, Base
from schemas import UserSchema, TaskSchema, TaskRead, UserUpdate, TaskUpdate, UserLogin, Token
from models import User
from repository import TaskRepository
from security import get_password_hash, verify_password, create_access_token, decode_access_token



@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    user_id = decode_access_token(token)

    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=401, detail="Пользователь не найден")
    return user


@app.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_credentials.email))
    user = result.scalars().first()

    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    token_data = {"sub": user.id}
    access_token = create_access_token(data=token_data)

    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/tasks", response_model=list[TaskRead])
async def get_my_tasks(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    stmt = select(Task).where(Task.creator_id == current_user.id)
    result = await db.execute(stmt)
    return result.scalars().all()




@app.post("/users", response_model=UserSchema)
async def create_user(user: UserSchema, db: AsyncSession = Depends(get_db)):
    db_user = User(
        id=str(uuid4()),
        **user.model_dump()
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@app.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()

@app.get("/users/search")
async def search_user(query: str, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(or_(User.email == query, User.phone_number == query))
    result = await db.execute(stmt)
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=UserSchema)
async def update_user_by_id(user_id: str, user_data: UserUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalars().first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)

    await db.commit()
    await db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}")
async def delete_user_by_id(user_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user_in_db = result.scalars().first()

    if not user_in_db:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user_in_db)
    await db.commit()
    return {"message": f"User with id {user_id} has been deleted"}


@app.post("/tasks", response_model=TaskRead)
async def create_task(task: TaskSchema, client_id: str, db: AsyncSession = Depends(get_db)):
    return await TaskRepository.create_task(db, task, client_id)

@app.get("/tasks", response_model=list[TaskRead])
async def get_all_tasks(db: AsyncSession = Depends(get_db)):
    return await TaskRepository.get_all_tasks(db)

@app.get("/tasks/search", response_model=list[TaskRead])
async def search_tasks_route(query: str, db: AsyncSession = Depends(get_db)):
    return await TaskRepository.search_task(db, query)

@app.get("/tasks/{task_id}", response_model=TaskRead)
async def search_tasks_by_id(task_id: str, db: AsyncSession = Depends(get_db)):
    task_in_db = await TaskRepository.get_task_by_id(db, task_id)
    if not task_in_db:
        raise HTTPException(status_code=404, detail="Task not found")
    return task_in_db

@app.put("/tasks/{task_id}", response_model=TaskRead)
async def update_tasks_by_id(task_id: str, task_data: TaskUpdate, db: AsyncSession = Depends(get_db)):
    task_in_db = await TaskRepository.update_task(db, task_id, task_data)
    if not task_in_db:
        raise HTTPException(status_code=404, detail="Task not found")
    return task_in_db

@app.delete("/tasks/{task_id}")
async def delete_task_by_id(task_id: str, db: AsyncSession = Depends(get_db)):
    success = await TaskRepository.delete_task(db, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": f"Task with id {task_id} has been deleted"}