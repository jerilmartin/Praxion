"""
Generic async repository (data-access layer).

Every service uses a Repository subclass instead of writing raw SQLAlchemy
queries directly in endpoints or agents. Keeps things DRY and testable.

Usage:
    class InfrastructureRepository(BaseRepository[InfrastructureResource]):
        model = InfrastructureResource

    repo = InfrastructureRepository(db)
    resources = await repo.list(skip=0, limit=50)
"""
from __future__ import annotations
from typing import Generic, TypeVar, Type, Optional, Any

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base

ModelT = TypeVar("ModelT", bound=Base)


class BaseRepository(Generic[ModelT]):
    """CRUD operations for a single SQLAlchemy model."""

    model: Type[ModelT]

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, id: str) -> Optional[ModelT]:
        """Return a single record by primary key, or None."""
        result = await self.db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def get_or_404(self, id: str) -> ModelT:
        """Return a record or raise NotFoundError."""
        from app.core.exceptions import NotFoundError
        obj = await self.get(id)
        if obj is None:
            raise NotFoundError(f"{self.model.__name__} '{id}' not found")
        return obj

    async def list(
        self,
        skip: int = 0,
        limit: int = 50,
        filters: Optional[list] = None,
    ) -> tuple[list[ModelT], int]:
        """
        Return (items, total_count) with optional SQLAlchemy filter clauses.

        Example:
            items, total = await repo.list(filters=[Model.status == "active"])
        """
        query = select(self.model)
        count_query = select(func.count()).select_from(self.model)
        if filters:
            for f in filters:
                query = query.where(f)
                count_query = count_query.where(f)

        total_result = await self.db.execute(count_query)
        total = total_result.scalar_one()

        result = await self.db.execute(query.offset(skip).limit(limit))
        items = list(result.scalars().all())
        return items, total

    async def create(self, obj: ModelT) -> ModelT:
        """Persist a new record and return it with DB-generated fields populated."""
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def update(self, obj: ModelT, data: dict[str, Any]) -> ModelT:
        """Apply a dict of field updates to an existing record."""
        for key, value in data.items():
            setattr(obj, key, value)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, obj: ModelT) -> None:
        """Hard-delete a record."""
        await self.db.delete(obj)
        await self.db.commit()
