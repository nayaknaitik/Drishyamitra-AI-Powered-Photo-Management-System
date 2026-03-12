from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import and_, select

from app.ai.nlp_query_parser import ParsedQuery, parse_query_rule_based
from app.extensions import db
from app.models import Face, Person, Photo, PhotoTag


class SearchService:
    def search(self, *, user_id: int, query_text: str) -> tuple[ParsedQuery, list[Photo]]:
        parsed = parse_query_rule_based(query_text)
        photos = self._search_photos(user_id=user_id, parsed=parsed)
        return parsed, photos

    def _search_photos(self, *, user_id: int, parsed: ParsedQuery) -> list[Photo]:
        q = select(Photo).where(Photo.user_id == user_id)

        if parsed.year:
            start = datetime(parsed.year, 1, 1, tzinfo=timezone.utc)
            end = datetime(parsed.year + 1, 1, 1, tzinfo=timezone.utc)
            q = q.where(and_(Photo.taken_at.is_not(None), Photo.taken_at >= start, Photo.taken_at < end))

        if parsed.person_name:
            person = db.session.execute(
                select(Person).where(Person.user_id == user_id, Person.name.ilike(parsed.person_name))
            ).scalar_one_or_none()
            if person:
                q = q.join(Face, Face.photo_id == Photo.id).where(Face.person_id == person.id)
            else:
                return []

        if parsed.event:
            q = q.join(PhotoTag, PhotoTag.photo_id == Photo.id).where(
                PhotoTag.key == "event", PhotoTag.value.ilike(parsed.event)
            )

        q = q.order_by(Photo.taken_at.desc().nullslast(), Photo.created_at.desc()).limit(200)
        return list(db.session.execute(q).scalars().unique().all())

