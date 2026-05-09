from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from sqlalchemy.orm import joinedload
from uuid import uuid4
import models, schemas


class TaskRepository:

    @staticmethod
    async def create_task(db: AsyncSession, task_data: schemas.TaskSchema, user_id: str):
        new_task = models.Task(
            id=str(uuid4()),
            title=task_data.title,
            description=task_data.description,
            creator_id=user_id,
            status=task_data.status or "new"
        )

        db.add(new_task)
        await db.commit()
        await db.refresh(new_task)


        stmt = select(models.Task).options(joinedload(models.Task.creator)).where(models.Task.id == new_task.id)
        result = await db.execute(stmt)
        return result.scalars().first()

    @staticmethod
    async def get_all_tasks(db: AsyncSession):
        stmt = select(models.Task).options(joinedload(models.Task.creator))
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def get_task_by_id(db: AsyncSession, task_id: str):
        stmt = select(models.Task).options(joinedload(models.Task.creator)).where(models.Task.id == task_id)
        result = await db.execute(stmt)
        return result.scalars().first()

    @staticmethod
    async def search_task(db: AsyncSession, query: str):
        stmt = select(models.Task).options(joinedload(models.Task.creator)).where(
            or_(
                models.Task.title.ilike(f"%{query}%"),
                models.Task.description.ilike(f"%{query}%")
            )
        )
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def update_task(db: AsyncSession, task_id: str, task_data: schemas.TaskUpdate):
        task = await TaskRepository.get_task_by_id(db, task_id)

        if task:
            update_data = task_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(task, key, value)

            await db.commit()
            await db.refresh(task)

            return await TaskRepository.get_task_by_id(db, task_id)
        return None

    @staticmethod
    async def delete_task(db: AsyncSession, task_id: str):
        task = await TaskRepository.get_task_by_id(db, task_id)
        if task:
            await db.delete(task)
            await db.commit()
            return True
        return False