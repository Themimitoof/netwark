from sqlalchemy import Column, Integer, Text, TIMESTAMP, JSON, Enum
from sqlalchemy.sql.functions import now
from sqlalchemy.dialects.postgresql import UUID

from .meta import Base


class Ping(Base):
    id = Column(UUID, primary_key=True)
    dest_ip = Column(Text, nullable=False)
    ping_type = Column(
        Enum('default', 'ip4', 'ip6', name='ping_type'),
        default='default',
        nullable=False,
    )
    count = Column(Integer, default=4, nullable=False)
    created_at = Column(TIMESTAMP, default=now())
