from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String, nullable=False)
    email = Column(String, nullable=False)
    summary = Column(Text, nullable=True)