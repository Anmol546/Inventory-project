from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db, Base, engine
from app import crud, schemas, models
from app.ai_service import generate_summary


Base.metadata.create_all(bind=engine)
app = FastAPI(title="Ticket Management API")

@app.get("/")
def home():
    return {"message": "Welcome to the Ticket Management API"}
@app.post("/tickets/", response_model=schemas.TicketResponse)
def create_ticket(ticket: schemas.TicketCreateSimple, db: Session = Depends(get_db)):
    return crud.create_ticket(db=db, ticket=ticket)

@app.get("/tickets/", response_model=list[schemas.TicketResponse])
def get_tickets(status: str = None, email: str = None, db: Session = Depends(get_db)):
    return crud.get_ticket(db=db, status=status, email=email)
@app.get("/tickets/{ticket_id}", response_model=schemas.TicketResponse)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = crud.get_ticket(db=db, ticket_id=ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket
@app.put("/tickets/{ticket_id}/status", response_model=schemas.TicketResponse)
def update_status(ticket_id: int, status_update: schemas.TicketStatusUpdate, db: Session = Depends(get_db)):
    ticket = crud.update_ticket_status(db=db, ticket_id=ticket_id, status=status_update.status)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@app.post("/tickets/{ticket_id}/summary")
def summarize_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = crud.get_ticket(db=db, ticket_id=ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    text = f"Subject: {ticket.subject}\nDescription: {ticket.description}"
    summary = generate_summary(text)
    crud.save_summary(db=db, ticket_id=ticket_id, summary=summary)
    return {"ticket_id": ticket_id, "summary": summary}