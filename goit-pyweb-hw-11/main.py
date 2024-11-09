from fastapi import FastAPI, Query, Path
from src.contacts.routers import router as contacts_router


app = FastAPI()

app.include_router(contacts_router, prefix="/contacts", tags=["contacts"])

# @app.get("/")
# async def ping():
#     return {"message": "pong"}

# @app.get("/contact/all")
# async def get_contact(skip: int = None, limit: int = Query(default=10, le=100, ge=10)):
#     return {"contacts": f"all contacts, skip -{skip}, limit - {limit}"}


# @app.post("/contact")
# async def create_contact(contact: Contact) -> ContactResponse:
#      return ContactResponse(first_name=contact.first_name, last_name=contact.last_name)
     

# @app.get("/contact/{contact_id}")
# async def get_contact(contact_id: int = Path(description="The ID of the contact to get", gt=0, le=10)):
#     return {"contact_id": contact_id}
