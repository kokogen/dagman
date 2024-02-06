import asyncio

from typing import Optional

from sqlalchemy import Integer, and_, cast, func, insert, inspect, or_, select, text
from sqlalchemy.orm import aliased, contains_eager, joinedload, selectinload

from db.models import Base, Dag

from db.sessions import async_session_factory
from db.sessions import async_engine

async def init_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
async def select_dags():
    async with async_session_factory() as session:
        query = (
                select(Dag)
                .options(selectinload(Dag.operations))
            )

        res = await session.execute(query)
        rslt = res.scalars().all()
        return [r for r in rslt]
    
async def select_dag_by_id(id: int) -> Optional[Dag]:
    async with async_session_factory() as session:
        query = (
                select(Dag)
                .options(joinedload(Dag.operations))
                .filter(Dag.id==id)
            )

        res = await session.execute(query)
        rslt = res.scalars().all()
        return [r for r in rslt]
    




