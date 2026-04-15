from sqlalchemy.ext.asyncio import AsyncSession
import models, schemas, select
from uuid import uuid4

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