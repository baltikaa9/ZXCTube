from typing import Type, TypeVar, Generic, overload
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from db import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        """
            CRUD object with default methods to Create, Read, Update, Delete (CRUD).

            **Parameters**

            * `model`: A SQLAlchemy model class
            * `schema`: A Pydantic model (schema) class
        """
        self.model = model
        self.session = session

    async def create(self, obj_schema: CreateSchemaType) -> ModelType:
        obj_data = obj_schema.model_dump()
        obj = self.model(**obj_data)
        self.session.add(obj)
        await self.session.commit()
        return obj

    async def get(self, primary_key: int | UUID) -> ModelType | None:
        obj = await self.session.get(self.model, primary_key)
        return obj

    async def update(self):
        raise NotImplementedError

    async def delete(self, primary_key: int | UUID) -> ModelType | None:
        obj = await self.get(primary_key)
        if not obj:
            return None
        await self.session.delete(obj)
        await self.session.commit()
        return obj
