from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class ManagerBase:
    def __init__(self, model):
        self.model = model

    async def get_multi(self, session: AsyncSession):
        objects = await session.execute(
            select(self.model)
        )
        return objects.scalars().all()

    async def create(
            self,
            obj,
            session: AsyncSession,
            user: Optional[User] = None
    ):
        obj_dict = obj.dict()
        if user:
            obj_dict['user_id'] = user.id
        obj_model = self.model(**obj_dict)
        session.add(obj_model)
        await session.commit()
        await session.refresh(obj_model)
        return obj_model
