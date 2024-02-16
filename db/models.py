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
    DAG_OP = 'DAG_OP'
    DAG_EDV = 'EDV'
    
class Base(DeclarativeBase):
    __table_args__ = {"schema": "dagman"}
    
    repr_cols_num = 3
    repr_cols = tuple()
    
    def __repr__(self):
        """Relationships не используются в repr(), т.к. могут вести к неожиданным подгрузкам"""
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"

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
    left_edges: Mapped[List['Edge']] = relationship(lazy=True, foreign_keys="Edge.left_id")
    right_edges: Mapped[List['Edge']] = relationship(lazy=True, foreign_keys="Edge.right_id")
    
class DagOperation(Base):
    __tablename__ = 'dag_operation'
    node_id: Mapped[int] = mapped_column(ForeignKey('dagman.node.id'), primary_key=True)
    dag_id: Mapped[int] = mapped_column(ForeignKey('dagman.dag.id'))
    step: Mapped[int] = mapped_column(nullable=False)
    dag: Mapped['Dag'] = relationship(back_populates='operations', lazy=True)
    node: Mapped['Node'] = relationship(back_populates='operation', lazy=True)
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
    left_node: Mapped['Node'] = relationship("Node", lazy=True, foreign_keys=[left_id])
    right_node: Mapped['Node'] = relationship("Node", lazy=True, foreign_keys=[right_id])
    # left_node: Mapped['Node'] = relationship(back_populates='left_edges', lazy=True, foreign_keys=[left_id])
    # right_node: Mapped['Node'] = relationship(back_populates='right_edges', lazy=True, foreign_keys=[right_id])