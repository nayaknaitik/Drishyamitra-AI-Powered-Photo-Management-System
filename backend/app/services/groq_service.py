from __future__ import annotations

import json
from dataclasses import dataclass

import requests

from config import settings


@dataclass(frozen=True)
class GroqIntent:
    intent: str
    args: dict


class GroqService:
    """
    Minimal Groq OpenAI-compatible client (no extra SDK dependency).
    """

    def parse_intent(self, *, user_text: str) -> GroqIntent | None:
        if not settings.groq_api_key:
            return None

        system = (
            "You are Drishyamitra, an assistant for an AI photo manager. "
            "Extract the user's intent and arguments. "
            "Return ONLY valid JSON with keys: intent, args. "
            "Supported intents: photo_search, person_search, send_email, send_whatsapp, list_events, show_recent. "
            "Args can include: person_name, year, event, photo_ids, destination."
        )
        body = {
            "model": settings.groq_model,
            "temperature": 0.1,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user_text},
            ],
        }

        resp = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {settings.groq_api_key}", "Content-Type": "application/json"},
            data=json.dumps(body),
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        content = data["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        return GroqIntent(intent=str(parsed.get("intent", "unknown")), args=dict(parsed.get("args") or {}))

