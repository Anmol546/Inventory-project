from pydantic import BaseModel, Field
from typing import Optional

class TicketBase(BaseModel):
    title: str
    subject: str
    description: str
    status: str
    email: str

class TicketCreate(TicketBase):
    pass

class TicketCreateSimple(BaseModel):
    customer_name: str = Field(..., min_length=1, description="Name of the customer")
    email: str = Field(..., description="Contact email")
    subject: str = Field(..., min_length=1, description="Subject of the ticket")
    description: str = Field(..., min_length=1, description="Detailed description of the issue")
    status: Optional[str] = Field("open", description="Ticket status")

    class Config:
        extra = "ignore"

class TicketResponse(TicketBase):
    id: int

    class Config:
        from_attributes = True

class TicketStatusUpdate(BaseModel):
    status: str