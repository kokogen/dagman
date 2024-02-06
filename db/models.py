import asyncio
from enum import Enum
from typing import List
from typing import Generator
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY

class NodeType(str, Enum):
    DAG_OP = 'DAG_OPERATION'
    DAG_EDV = 'ENTITY_DATAVERSION'
    
class Base(DeclarativeBase):
    __table_args__ = {"schema": "dagman"}

class Dag(Base):
    __tablename__ = 'dag'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    params: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=False)
    operations: Mapped[List['DagOperation']] = relationship(back_populates='dag')
    
class Node(Base):
    __tablename__ = 'node'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    node_type: Mapped['NodeType'] = mapped_column(String(10), nullable=False)   
    operation: Mapped[Optional['DagOperation']] = relationship(back_populates='node')
    dataversion: Mapped[Optional['DataVersion']] = relationship(back_populates='node')
    left_edges: Mapped[List['Edge']] = relationship(back_populates='left_node', lazy=True)
    right_edges: Mapped[List['Edge']] = relationship(back_populates='right_node', lazy=True)
    
class DagOperation(Base):
    __tablename__ = 'dag_operation'
    node_id: Mapped[int] = mapped_column(ForeignKey('dagman.node.id'), primary_key=True)
    dag_id: Mapped[int] = mapped_column(ForeignKey('dagman.dag.id'))
    step: Mapped[int] = mapped_column(nullable=False)
    dag: Mapped['Dag'] = relationship(back_populates='operations')
    node: Mapped['Node'] = relationship(back_populates='operation')
    params: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=False)
    
class DataVersion(Base):
    __tablename__ = 'dataversion'
    node_id: Mapped[int] = mapped_column(ForeignKey('dagman.node.id'), primary_key=True)    
    entity_name: Mapped[str] = mapped_column(nullable=False)
    node: Mapped['Node'] = relationship(back_populates='dataversion')
    
class Edge(Base):
    __tablename__ = 'edge'
    left_id: Mapped[int] = mapped_column(ForeignKey('dagman.node.id'), primary_key=True)
    right_id: Mapped[int] = mapped_column(ForeignKey('dagman.node.id'), primary_key=True)
    shift: Mapped[int] = mapped_column(nullable=False, default=0)
    left_node: Mapped['Node'] = relationship(back_populates='left_edges', lazy=True)
    right_node: Mapped['Node'] = relationship(back_populates='right_edges', lazy=True)