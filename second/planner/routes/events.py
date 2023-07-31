from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, Body, HTTPException, status

from planner.database.connection import Database
from planner.models.events import Event, EventUpdate

event_router = APIRouter(tags=["Events"], prefix="/event")

event_database = Database(Event)


@event_router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    events = await event_database.get_all()
    return events


@event_router.get("/{userid}", response_model=Event)
async def retrieve_event(userid: PydanticObjectId) -> Event:
    event = await event_database.get(userid)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied Id does not exist",
        )
    return event


@event_router.post("/new")
async def create_event(body: Event = Body(...)) -> dict:
    await event_database.save(body)
    return {"message": "Event created Successfully"}


@event_router.put("/{id}", response_model=Event)
async def update_event(userid: PydanticObjectId, body: EventUpdate) -> Event:
    updated_event = await event_database.update(userid, body)
    if not updated_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist",
        )
    return updated_event


@event_router.delete("/{userid}")
async def delete_event(userid: PydanticObjectId) -> dict:
    event = await event_database.delete(userid)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist",
        )

    return {"message": "Event deleted successfully"}
