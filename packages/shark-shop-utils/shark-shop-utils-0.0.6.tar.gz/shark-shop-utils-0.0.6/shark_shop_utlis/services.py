from typing import List, cast
from uuid import UUID

import ormar
from fastapi import HTTPException
from ormar import NoMatch

from shark_shop_utlis.depends import PAGINATION

NOT_FOUND = HTTPException(404, "Item not found")


class BaseService:
    def __init__(self):
        self._table = ormar.Model

    async def get_one(self, server_id: UUID, **kwargs) -> ormar.Model:
        try:
            server = await self._table.objects.filter(id=server_id, **kwargs).first()
        except NoMatch:
            raise NOT_FOUND
        return server

    async def get_all(self, pagination: PAGINATION, **kwargs) -> List[ormar.Model]:
        skip, limit = pagination.get("skip"), pagination.get("limit")
        query = self._table.objects.offset(cast(int, skip))
        if limit:
            query = query.limit(limit)
        if kwargs:
            query = query.filter(**kwargs)
        return await query.all()

    async def create(self, schema=None, **kwargs) -> ormar.Model:
        model_dict = schema.dict(exclude={"id"})
        return await self._table.objects.create(**model_dict, **kwargs)

    async def delete_one(self, server_id: UUID, **kwargs) -> ormar.Model:
        model = await self.get_one(server_id=server_id, **kwargs)
        await model.delete()
        return model

    async def update(self, server_id: UUID, schema=None, **kwargs) -> ormar.Model:
        await self._table.objects.filter(_exclude=False, id=server_id).update(
            **schema.dict(exclude_unset=True), **kwargs
        )
        return await self.get_one(server_id=server_id)

    async def delete_all(self):
        await self._table.objects.delete(each=True)
        return await self.get_all(pagination={"skip": 0, "limit": None})
