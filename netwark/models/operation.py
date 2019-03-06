from sqlalchemy import Column, Integer, Text, TIMESTAMP, JSON, Enum
from sqlalchemy.sql.functions import now
from sqlalchemy.dialects.postgresql import UUID

from .meta import Base


class Operation(Base):
    __tablename__ = 'operation'
    id = Column(UUID(), primary_key=True)
    destination = Column(Text, nullable=False)
    type = Column(
        Enum('ping', 'mtr', 'whois', 'dig', name='operation_type_enm'),
        nullable=False,
    )
    options = Column(JSON())
    created_at = Column(TIMESTAMP, default=now())
