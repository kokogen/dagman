import asyncio

from typing import Optional

from sqlalchemy import Integer, and_, cast, func, insert, inspect, or_, select, text
from sqlalchemy.orm import aliased, contains_eager, joinedload, selectinload

from db.models import Base, Dag, DagOperation, Node, Edge

from db.sessions import async_session_factory

async def init_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
class RepoDag:
  
    @staticmethod
    async def select_dags():
        async with async_session_factory() as session:
            query = (
                    select(Dag)
                    .options(selectinload(Dag.operations).options(selectinload(DagOperation.node)))
                )

            res = await session.execute(query)
            rslt = res.scalars().all()
            return [r for r in rslt]
       
    @staticmethod 
    async def select_dag_by_id(id: int) -> Optional[Dag]:
        async with async_session_factory() as session:
            query = (
                    select(Dag)
                    .options(joinedload(Dag.operations))
                    .filter(Dag.id==id)
                )

            res = await session.execute(query)
            return res.scalars().first()
            
    
    @staticmethod    
    async def add_dag(dag: Dag) -> Dag:
        async with async_session_factory() as session:
            session.add(dag)
            await session.flush()
            await session.commit()
            return dag
    
    @staticmethod    
    async def del_dag(dag: Dag):
        async with async_session_factory() as session:
            await session.delete(dag)
            await session.commit()

    @staticmethod
    async def del_dags_all():
        lst = await RepoDag.select_dags()
        async with async_session_factory() as session:
            for d in lst: 
                operations = d.operations
                
                for o in operations:
                    node = o.node
                    await session.delete(o)
                    await session.delete(n)
                    
                await session.delete(d)
                
            await session.commit()
            
            
class RepoNode:
    
    @staticmethod
    async def select_node_by_id(id: int) -> Optional[Node]:
        async with async_session_factory() as session:
            query = (
                    select(Node)
                    .options(selectinload(Node.operation).options(selectinload(DagOperation.dag)))
                    .options(selectinload(Node.dataversion))
                    .options(selectinload(Node.left_edges))
                    .options(selectinload(Node.right_edges))
                    .filter(Node.id==id)
                )

            res = await session.execute(query)
            return res.scalars().first()
            # rslt = res.scalars().all()
            # return [r for r in rslt]    


