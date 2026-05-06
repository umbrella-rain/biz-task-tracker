from sqlalchemy.ext.asyncio import AsyncSession
import models, schemas, select
from uuid import uuid4
from sqlalchemy import select, and_
from sqlalchemy.orm import joinedload

class TaskRepository:

    @staticmethod
    async def create_task(db: AsyncSession, task_data: schemas.TaskSchema, user_id: str):

        new_task = models.Task(

            id = str (uuid4()),
            title = task_data.title,
            description = task_data.description,
            creator_id = user_id,
            status = "new"
        )

        db.add(new_task)
        await db.commit()
        await db.refresh(new_task)
        return new_task

    @staticmethod
    async def get_all_users(db: AsyncSession):
        result = await db.execute(select(models.User))
        return result.scalars().all()


    @staticmethod
    async def update_task (db: AsyncSession, task_id: str, task_data: schemas.TaskSchema, user_id: str):
        stmt = select(models.Task).where(models.Task.id == task_id, models.Task.creator_id == user_id)
        result = await db.execute(stmt)
        task = result.scalars().first()

        if task:
            task.status = "updated"
            task.title = task_data.title
            task.description = task_data.description
            await db.commit()
            await db.refresh(task)
        return task


    @staticmethod
    async def get_task(db: AsyncSession):
        result = await db.execute(select(models.Task))
        return result.scalars().all()

        @staticmethod
        async def search_task(db: AsyncSession, query: str):
            stmt = ((models.Task).options(joinedload(models.Task.creator)).where((models.Task.title.ilike(f"%{query}%"))
                                                                                 |(models.Task.description.ilike(f"%{query}%"))
                )
            )
            result = await db.execute(stmt)
            return result.scalars().all()

        result = await db.execute(stmt)
        return result.scalars().all()