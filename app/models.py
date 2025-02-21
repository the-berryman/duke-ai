# app/models.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

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
    status: str
    current_turn: str
    created_at: datetime