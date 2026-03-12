from __future__ import annotations

from app.ai.nlp_query_parser import parse_query_rule_based


def test_parse_last_year():
    q = parse_query_rule_based("Show photos of Mom from last year")
    assert q.intent == "photo_search"
    assert q.year is not None


def test_parse_send_whatsapp():
    q = parse_query_rule_based("Send John's photos to WhatsApp")
    assert q.intent == "send_whatsapp"

