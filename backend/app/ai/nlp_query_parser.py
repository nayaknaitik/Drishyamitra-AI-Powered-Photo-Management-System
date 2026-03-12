from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class ParsedQuery:
    intent: str
    person_name: str | None = None
    event: str | None = None
    year: int | None = None
    raw: str = ""


def parse_query_rule_based(text: str) -> ParsedQuery:
    """
    Lightweight fallback parser (used when Groq is not configured).
    """
    q = text.strip()
    lowered = q.lower()

    if any(k in lowered for k in ["send", "whatsapp", "email"]):
        if "whatsapp" in lowered:
            return ParsedQuery(intent="send_whatsapp", raw=q)
        if "email" in lowered or "mail" in lowered:
            return ParsedQuery(intent="send_email", raw=q)
        return ParsedQuery(intent="delivery", raw=q)

    if any(k in lowered for k in ["show", "find", "photos", "pictures", "images"]):
        # extract year
        year = None
        m = re.search(r"\b(20\d{2}|19\d{2})\b", lowered)
        if m:
            year = int(m.group(1))
        elif "last year" in lowered:
            year = datetime.now(timezone.utc).year - 1

        # naive "of X" person name
        person_name = None
        m = re.search(r"\b(of|with)\s+([a-zA-Z][a-zA-Z\s]{1,40})\b", q)
        if m:
            person_name = m.group(2).strip()

        event = None
        m = re.search(r"\bat\s+([a-zA-Z][a-zA-Z\s]{1,40})\b", q)
        if m:
            event = m.group(1).strip()

        return ParsedQuery(intent="photo_search", person_name=person_name, event=event, year=year, raw=q)

    return ParsedQuery(intent="unknown", raw=q)

