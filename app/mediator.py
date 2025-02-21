# app/mediator.py
from abc import ABC, abstractmethod
import requests
from typing import List, Dict


class AIMediatorBase(ABC):
    """Base class for AI mediators"""

    @abstractmethod
    async def generate_response(self, message: str, context: Dict) -> str:
        pass


class OllamaMediatorModel(AIMediatorBase):
    def __init__(self, model_name: str = "duke", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url

    async def generate_response(self, message: str, context: Dict) -> str:
        prompt = self._create_prompt(message, context)

        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model_name,
                "prompt": prompt,
                "stream": False
            }
        )
        # debugging 500 error when mediator response is expected
        print("Debug - Full response:", response.json())  # See what we're actually getting
        return response.json()["response"]

    def _create_prompt(self, message: str, context: Dict) -> str:
        recent_messages = context.get("recent_messages", [])
        messages_text = "\n".join([
            f"{msg['sender_name']}: {msg['content']}"
            for msg in recent_messages[-3:]
        ])

        return f"""Previous messages:
{messages_text}

Current message from {context['current_speaker']}: {message}

As a relationship mediator, provide a response that acknowledges their perspective and guides the conversation constructively."""


class AIMediator:
    def __init__(self, model: AIMediatorBase):
        self.model = model

    async def mediate(self, session_id: str, message: Dict, db) -> str:
        context = await self._get_context(session_id, db)

        response = await self.model.generate_response(
            message["content"],
            {
                "session_id": session_id,
                "current_speaker": message["sender_name"],
                "recent_messages": context["recent_messages"]
            }
        )

        return response

    async def _get_context(self, session_id: str, db) -> Dict:
        messages = await db.messages.find(
            {"session_id": session_id}
        ).sort("timestamp", -1).limit(5).to_list(None)

        session = await db.sessions.find_one({"id": session_id})

        return {
            "session": session,
            "recent_messages": list(reversed(messages))
        }