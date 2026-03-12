from __future__ import annotations

from sqlalchemy import select

from app.extensions import db
from app.models import Face, Person
from app.utils.errors import NotFoundError


class FaceService:
    def label_face(self, *, user_id: int, face_id: int, person_name: str | None, person_id: int | None) -> Face:
        face = db.session.execute(select(Face).where(Face.id == face_id, Face.user_id == user_id)).scalar_one_or_none()
        if not face:
            raise NotFoundError("Face not found")

        person: Person | None = None
        if person_id is not None:
            person = db.session.execute(
                select(Person).where(Person.id == person_id, Person.user_id == user_id)
            ).scalar_one_or_none()
            if not person:
                raise NotFoundError("Person not found")
        elif person_name:
            name = person_name.strip()
            person = db.session.execute(
                select(Person).where(Person.user_id == user_id, Person.name.ilike(name))
            ).scalar_one_or_none()
            if not person:
                person = Person(user_id=user_id, name=name)
                db.session.add(person)
                db.session.flush()

        if not person:
            raise NotFoundError("Person required")

        face.person_id = person.id
        face.is_unknown = False
        db.session.commit()
        return face

    def list_persons(self, *, user_id: int) -> list[Person]:
        q = select(Person).where(Person.user_id == user_id).order_by(Person.name.asc())
        return list(db.session.execute(q).scalars().all())

