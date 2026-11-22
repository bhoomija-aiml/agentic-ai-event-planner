
from fastapi import FastAPI, HTTPException
from bson import ObjectId
from database import events_collection, db

app = FastAPI(title="AI Event Planner")


@app.get("/")
def home():
    return {"message": "Event Planner API is running"}


@app.get("/db-check")
def db_check():
    try:
        db.command("ping")
        return {"database": "connected"}
    except Exception:
        return {"database": "disconnected"}


@app.post("/events")
def create_event(event: dict):
    result = events_collection.insert_one(event)

    return {
        "message": "Event created",
        "event_id": str(result.inserted_id)
    }


@app.get("/events")
def get_events():
    events = list(events_collection.find())

    for event in events:
        event["_id"] = str(event["_id"])

    return events


@app.get("/events/{event_id}")
def get_event(event_id: str):
    if not ObjectId.is_valid(event_id):
        raise HTTPException(status_code=400, detail="Invalid event ID")

    event = events_collection.find_one(
        {"_id": ObjectId(event_id)}
    )

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    event["_id"] = str(event["_id"])
    return event


@app.put("/events/{event_id}")
def update_event(event_id: str, data: dict):
    if not ObjectId.is_valid(event_id):
        raise HTTPException(status_code=400, detail="Invalid event ID")

    data.pop("_id", None)

    result = events_collection.update_one(
        {"_id": ObjectId(event_id)},
        {"$set": data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Event not found")

    return {"message": "Event updated"}


@app.delete("/events/{event_id}")
def delete_event(event_id: str):
    if not ObjectId.is_valid(event_id):
        raise HTTPException(status_code=400, detail="Invalid event ID")

    result = events_collection.delete_one(
        {"_id": ObjectId(event_id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Event not found")

    return {"message": "Event deleted"}
