import asyncio
from enum import Enum
from typing import List
from typing import Generator
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
    pass

class Dag(Base):
    __tablename__ = 'dag'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    params: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=False)