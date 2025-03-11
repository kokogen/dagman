import asyncio

from typing import Optional

from sqlalchemy import Integer, and_, cast, func, insert, inspect, or_, select, text
from sqlalchemy.orm import aliased, contains_eager, joinedload, selectinload

from db.models import Base, Dag, DagOperation, Node, Edge

from db.sessions import async_session_factory, async_engine

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
                    await session.delete(node)
                    
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
            
    @staticmethod
    async def select_nodes() -> list[Node]:
        async with async_session_factory() as session:
            query = (
                    select(Node)
                    .options(selectinload(Node.operation).options(selectinload(DagOperation.dag)))
                    .options(selectinload(Node.dataversion))
                    .options(selectinload(Node.left_edges))
                    .options(selectinload(Node.right_edges))
            )
            
            res = await session.execute(query)
            return [r for r in res.scalars().all()]

    @staticmethod
    async def add_node(node: Node) -> Node:
        async with async_session_factory() as session:
            session.add(node)
            await session.flush()
            await session.commit()
            return node

    @staticmethod
    async def update_node(node: Node) -> Node:
        async with async_session_factory() as session:
            await session.merge(node)
            await session.commit()
            return node

    @staticmethod
    async def delete_node(node: Node):
        async with async_session_factory() as session:
            await session.delete(node)
            await session.commit()

    @staticmethod
    async def delete_node_by_id(node_id: int):
        node = await RepoNode.select_node_by_id(node_id)
        if node:
            await RepoNode.delete_node(node)

    @staticmethod
    async def delete_node_with_edges(node: Node):
        async with async_session_factory() as session:
            async with session.begin():
                # Удаляем все рёбра, где узел является левым или правым концом
                for edge in node.left_edges:
                    await session.delete(edge)
                
                for edge in node.right_edges:
                    await session.delete(edge)
                
                # Удаляем сам узел
                await session.delete(node)

class RepoEdge:
    @staticmethod
    async def select_edges() -> list[Edge]:
        async with async_session_factory() as session:
            query = (
                select(Edge)
                .options(selectinload(Edge.left_node))
                .options(selectinload(Edge.right_node))
            )
            res = await session.execute(query)
            return [r for r in res.scalars().all()]
            
    @staticmethod
    async def select_edge_by_nodes(left_id: int, right_id: int) -> Optional[Edge]:
        async with async_session_factory() as session:
            query = (
                select(Edge)
                .options(selectinload(Edge.left_node))
                .options(selectinload(Edge.right_node))
                .filter(and_(Edge.left_id == left_id, Edge.right_id == right_id))
            )
            res = await session.execute(query)
            return res.scalars().first()
            
    @staticmethod
    async def add_edge(edge: Edge) -> Edge:
        async with async_session_factory() as session:
            session.add(edge)
            await session.flush()
            await session.commit()
            return edge
            
    @staticmethod
    async def delete_edge(left_id: int, right_id: int):
        async with async_session_factory() as session:
            query = (
                select(Edge)
                .filter(and_(Edge.left_id == left_id, Edge.right_id == right_id))
            )
            res = await session.execute(query)
            edge = res.scalars().first()
            if edge:
                await session.delete(edge)
                await session.commit()


