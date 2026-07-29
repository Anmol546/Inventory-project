from sqlalchemy.orm import Session
from app import models, schemas

def create_ticket(db: Session, ticket: schemas.TicketCreateSimple) -> schemas.TicketResponse:
    db_ticket = models.Ticket(
        title=ticket.customer_name[:50] if len(ticket.customer_name) > 50 else ticket.customer_name,
        subject=ticket.subject,
        description=ticket.description,
        status=ticket.status or "open",
        email=ticket.email,
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def get_ticket(db: Session, ticket_id: int = None, status: str = None, email: str = None):
    query = db.query(models.Ticket)
    if ticket_id is not None:
        return query.filter(models.Ticket.id == ticket_id).first()
    if status is not None:
        query = query.filter(models.Ticket.status == status)
    if email is not None:
        query = query.filter(models.Ticket.email == email)
    return query.all()

def save_summary(db: Session, ticket_id: int, summary: str):
    db_ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if db_ticket is None:
        return None
    db_ticket.summary = summary
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def update_ticket_status(db: Session, ticket_id: int, status: str):
    db_ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if db_ticket is None:
        return None
    db_ticket.status = status
    db.commit()
    db.refresh(db_ticket)
    return db_ticket