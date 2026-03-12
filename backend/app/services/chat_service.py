from __future__ import annotations

from sqlalchemy import select

from app.ai.nlp_query_parser import parse_query_rule_based
from app.extensions import db
from app.models import ChatHistory, Person, Photo
from app.services.delivery_service import DeliveryService
from app.services.groq_service import GroqService
from app.services.search_service import SearchService


class ChatService:
    def __init__(self) -> None:
        self.groq = GroqService()
        self.search = SearchService()
        self.delivery = DeliveryService()

    def handle_message(self, *, user_id: int, message: str) -> dict:
        if not message:
            return {"reply": "Please enter a message.", "intent": "unknown"}

        db.session.add(ChatHistory(user_id=user_id, role="user", content=message))
        db.session.commit()

        groq_intent = self.groq.parse_intent(user_text=message)
        if groq_intent:
            intent = groq_intent.intent
            args = groq_intent.args
        else:
            parsed = parse_query_rule_based(message)
            intent = parsed.intent
            args = {
                "person_name": parsed.person_name,
                "event": parsed.event,
                "year": parsed.year,
            }

        if intent in ["photo_search", "show_recent"]:
            parsed, photos = self.search.search(user_id=user_id, query_text=message)
            payload = {
                "reply": f"Found {len(photos)} photo(s).",
                "intent": parsed.intent,
                "photos": [{"id": p.id} for p in photos[:50]],
            }
        elif intent == "person_search":
            name = str(args.get("person_name") or "").strip()
            person = None
            if name:
                person = (
                    db.session.execute(select(Person).where(Person.user_id == user_id, Person.name.ilike(name)))
                    .scalar_one_or_none()
                )
            payload = {
                "reply": f"Person {'found' if person else 'not found'}: {name}" if name else "Which person?",
                "intent": intent,
                "person": {"id": person.id, "name": person.name} if person else None,
            }
        elif intent in ["send_email", "send_whatsapp"]:
            destination = str(args.get("destination") or args.get("to") or "").strip()
            photo_ids = args.get("photo_ids") or []
            if not isinstance(photo_ids, list):
                photo_ids = []
            photo_ids = [int(x) for x in photo_ids][:50]

            # If user didn't specify photos, fall back to recent
            if not photo_ids:
                recent = list(
                    db.session.execute(
                        select(Photo.id).where(Photo.user_id == user_id).order_by(Photo.created_at.desc()).limit(10)
                    )
                    .scalars()
                    .all()
                )
                photo_ids = recent

            if intent == "send_email":
                job = self.delivery.queue_email(user_id=user_id, to_email=destination, photo_ids=photo_ids)
                payload = {"reply": "Queued email delivery.", "intent": intent, "job": job}
            else:
                job = self.delivery.queue_whatsapp(user_id=user_id, to_phone=destination, photo_ids=photo_ids)
                payload = {"reply": "Queued WhatsApp delivery.", "intent": intent, "job": job}
        else:
            payload = {"reply": "I can search photos or send them via email/WhatsApp.", "intent": intent, "args": args}

        db.session.add(ChatHistory(user_id=user_id, role="assistant", content=payload["reply"]))
        db.session.commit()
        return payload

