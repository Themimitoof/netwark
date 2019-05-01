from sqlalchemy import Column, Integer, Text
from sqlalchemy.sql.functions import now

from .meta import Base


class OuiVendor(Base):
    __tablename__ = 'oui_vendor'
    id = None
    assignment = Column(Text, primary_key=True)
    orgname = Column(Text, nullable=False)
    orgaddr = Column(Text, nullable=True)

    def to_dict(self):
        return {
            'assignment': self.assignment,
            'orgname': self.orgname,
            'orgaddr': self.orgaddr
        }
