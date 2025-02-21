from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid

app = FastAPI(title="Duke API")

# MongoDB connection
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.duke_db


# Pydantic models for data validation
class SessionCreate(BaseModel):
    creator_name: str
    partner_name: str


class Message(BaseModel):
    content: str
    sender_name: str


class Session(BaseModel):
    id: str
    invite_code: str
    creator_name: str
    partner_name: str
    status: str  # "waiting", "active", "completed"
    current_turn: str
    created_at: datetime


# Session routes
@app.post("/sessions/create")
async def create_session(session_data: SessionCreate):
    """Create a new mediation session and generate invite code"""
    session = {
        "id": str(uuid.uuid4()),
        "invite_code": str(uuid.uuid4())[:8],  # First 8 chars of UUID
        "creator_name": session_data.creator_name,
        "partner_name": session_data.partner_name,
        "status": "waiting",  # Waiting for partner to join
        "current_turn": session_data.creator_name,  # Creator goes first
        "created_at": datetime.utcnow()
    }

    await db.sessions.insert_one(session)
    return {
        "session_id": session["id"],
        "invite_code": session["invite_code"],
        "message": "Session created! Share the invite code with your partner."
    }


@app.post("/sessions/join/{invite_code}")
async def join_session(invite_code: str, participant_name: str):
    """Join an existing session using invite code"""
    session = await db.sessions.find_one({"invite_code": invite_code})

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session["status"] != "waiting":
        raise HTTPException(status_code=400, detail="Session already started")

    if participant_name not in [session["creator_name"], session["partner_name"]]:
        raise HTTPException(status_code=400, detail="Name doesn't match session participants")

    # Update session status to active
    await db.sessions.update_one(
        {"invite_code": invite_code},
        {"$set": {"status": "active"}}
    )

    return {
        "session_id": session["id"],
        "message": "Successfully joined session"
    }


@app.post("/sessions/{session_id}/message")
async def send_message(session_id: str, message: Message):
    """Send a message in the session (if it's your turn)"""
    session = await db.sessions.find_one({"id": session_id})

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session["status"] != "active":
        raise HTTPException(status_code=400, detail="Session is not active")

    if session["current_turn"] != message.sender_name:
        raise HTTPException(status_code=400, detail="Not your turn to speak")

    # Store the message
    msg = {
        "session_id": session_id,
        "content": message.content,
        "sender_name": message.sender_name,
        "timestamp": datetime.utcnow()
    }
    await db.messages.insert_one(msg)

    # Update turn to other participant
    next_turn = (
        session["partner_name"]
        if message.sender_name == session["creator_name"]
        else session["creator_name"]
    )

    await db.sessions.update_one(
        {"id": session_id},
        {"$set": {"current_turn": next_turn}}
    )

    return {
        "message": "Message sent",
        "next_turn": next_turn
    }


@app.get("/sessions/{session_id}")
async def get_session_status(session_id: str):
    """Get current session status and recent messages"""
    session = await db.sessions.find_one({"id": session_id})

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Get recent messages
    messages = await db.messages.find(
        {"session_id": session_id}
    ).sort("timestamp", -1).limit(10).to_list(None)

    # Convert ObjectId to string for JSON serialization
    for msg in messages:
        msg["_id"] = str(msg["_id"])

    return {
        "session": {
            "id": session["id"],
            "status": session["status"],
            "current_turn": session["current_turn"],
            "creator_name": session["creator_name"],
            "partner_name": session["partner_name"]
        },
        "recent_messages": messages
    }


# Keep our test endpoint for MongoDB connection verification
@app.get("/test-db")
async def test_db():
    try:
        await client.admin.command('ping')
        return {"message": "Successfully connected to MongoDB"}
    except Exception as e:
        return {"message": f"Error connecting to MongoDB: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)