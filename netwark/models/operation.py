from sqlalchemy import (
    Column,
    Integer,
    Enum,
    TIMESTAMP,
    ARRAY,
    ForeignKey,
    String
)
from sqlalchemy.orm import relationship, backref, aliased
from sqlalchemy.sql.functions import now

from .meta import Base
from .types import UUID, JSON

OPERATION_FLAGS = ['ping', 'mtr']

operation_status = Enum(
    'waiting',
    'progress',
    'done',
    'error',
    'timeout',
    name='en_operation_status',
)


class Operation(Base):
    __tablename__ = 'operation'
    id = Column(UUID(), primary_key=True)
    type = Column(
        Enum('ping', 'mtr', name='en_operation_type'), nullable=False
    )
    destination = Column(String(), nullable=False)
    payload = Column(JSON())
    queues = Column(String(), default='netwark', nullable=False)
    status = Column(operation_status, nullable=False)
    created_at = Column(TIMESTAMP(False), nullable=False, default=now())
    updated_at = Column(TIMESTAMP(False), nullable=False, default=now())


class OperationResult(Base):
    __tablename__ = 'operation_result'
    id = Column(UUID(), primary_key=True)
    operation_id = Column('operation', UUID(), ForeignKey('operation.id'))
    worker = Column(String(), nullable=False)
    queue = Column(String(), nullable=False)
    status = Column(operation_status, nullable=False)
    payload = Column(JSON(), nullable=False)
    created_at = Column(TIMESTAMP(False), nullable=False, default=now())
    updated_at = Column(TIMESTAMP(False), nullable=False, default=now())

    operation = relationship(Operation, backref=backref('operation'))
