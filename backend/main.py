from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from contextlib import asynccontextmanager
from uuid import uuid4


from database import engine, get_db, Base
from schemas import UserSchema, TaskSchema, TaskRead, UserUpdate
from models import User, Task
from repository import TaskRepository


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)



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
async def update_user(user_id: str, user_data: UserUpdate, db: AsyncSession = Depends(get_db)):
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
async def delete_user(user_id: str, db: AsyncSession = Depends(get_db)):
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
async def get_task(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task))
    return result.scalars().all()
