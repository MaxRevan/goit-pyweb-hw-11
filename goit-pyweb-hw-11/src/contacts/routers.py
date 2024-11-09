from fastapi import APIRouter, Query, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from config.db import get_db
from src.contacts.schema import Contact, ContactCreate, ContactResponse, ContactUpdate
from src.contacts.repos import ContactRepository


router = APIRouter()


@router.get("/search", response_model=list[ContactResponse])
async def search_contacts(
    first_name: str = Query(None, alias="first_name"),
    last_name: str = Query(None),
    email: str = Query(None),
    db: AsyncSession = Depends(get_db)
):
    if not first_name and not last_name and not email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="At least one search parameter is required")
    contact_repo = ContactRepository(db)
    contacts = await contact_repo.search_contacts(first_name=first_name, last_name=last_name, email=email)
    return contacts


@router.get("/upcoming_birthdays", response_model=list[ContactResponse])
async def upcoming_birthdays(db: AsyncSession = Depends(get_db)):
    contact_repo = ContactRepository(db)
    contacts = await contact_repo.get_upcoming_birthdays()
    if not contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No contacts with birthdays in the next 7 days")
    return contacts


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(contact: ContactCreate, db: AsyncSession = Depends(get_db)):
    contact_repo = ContactRepository(db)
    return await contact_repo.create_contact(contact)
     

@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact_repo = ContactRepository(db)
    contact = await contact_repo.get_contact(contact_id)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.get("/", response_model=list[ContactResponse])
async def get_all_contacts(db: AsyncSession = Depends(get_db)):
    contact_repo = ContactRepository(db)
    contacts = await contact_repo.get_all_contacts()
    return contacts


@router.put("/{contact_id}", response_model=ContactResponse, status_code=status.HTTP_200_OK)
async def update_contact(contact_id: int, contact_data: ContactUpdate, db: AsyncSession = Depends(get_db)):
    contact_repo = ContactRepository(db)
    contact = await contact_repo.update_contact(contact_id, contact_data)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def get_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact_repo = ContactRepository(db)
    success = await contact_repo.delete_contact(contact_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return {"message": "Contact deleted successfully"}


