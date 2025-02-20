from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI()

# Connect to MongoDB
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.duke_db  # Creates/uses a database named 'duke_db'

# Test route to verify server is running
@app.get("/")
async def read_root():
    return {"message": "Duke API is running"}

# Test route to verify MongoDB connection
@app.get("/test-db")
async def test_db():
    try:
        # Try to ping the database
        await client.admin.command('ping')
        return {"message": "Successfully connected to MongoDB"}
    except Exception as e:
        return {"message": f"Error connecting to MongoDB: {str(e)}"}

# Simple model for testing
class Message(BaseModel):
    content: str
    sender: str

# Test route to write to MongoDB
@app.post("/test-message")
async def create_test_message(message: Message):
    try:
        # Insert a document into a 'messages' collection
        result = await db.messages.insert_one(message.dict())
        return {"message": "Test message stored successfully", "id": str(result.inserted_id)}
    except Exception as e:
        return {"message": f"Error storing message: {str(e)}"}

# Test route to read from MongoDB
@app.get("/test-messages")
async def get_test_messages():
    try:
        # Get all messages
        messages = await db.messages.find().to_list(length=10)
        # Convert ObjectId to string for JSON serialization
        for message in messages:
            message["_id"] = str(message["_id"])
        return messages
    except Exception as e:
        return {"message": f"Error retrieving messages: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)