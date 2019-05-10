import uuid

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
    'pending',
    'progress',
    'done',
    'error',
    'timeout',
    name='en_operation_status',
)


def gen_uuid():
    """
    Generates an string UUID4
    """
    return str(uuid.uuid4())


class Operation(Base):
    __tablename__ = 'operation'
    id = Column(UUID(), default=gen_uuid, primary_key=True)
    type = Column(
        Enum('ping', 'mtr', name='en_operation_type'), nullable=False
    )
    target = Column(String(), nullable=False)
    options = Column(String(), nullable=True)
    queues = Column(String(), default='netwark', nullable=False)
    status = Column(operation_status, nullable=False)
    created_at = Column(TIMESTAMP(False), nullable=False, default=now())
    updated_at = Column(TIMESTAMP(False), nullable=False, default=now())

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'status': self.status,
            'target': self.target,
            'options': self.options,
            'queues': self.queues.split(','),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S.%f'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S.%f'),
        }


class OperationResult(Base):
    __tablename__ = 'operation_result'
    id = Column(UUID(), default=gen_uuid, primary_key=True)
    operation_id = Column('operation', UUID(), ForeignKey('operation.id'))
    worker = Column(String(), nullable=False)
    queue = Column(String(), nullable=False)
    status = Column(operation_status, nullable=False)
    payload = Column(JSON(), nullable=False)
    created_at = Column(TIMESTAMP(False), nullable=False, default=now())
    updated_at = Column(TIMESTAMP(False), nullable=False, default=now())

    operation = relationship(Operation, backref=backref('operation'))
