from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from PIL import Image, ExifTags


@dataclass(frozen=True)
class PhotoMetadata:
    taken_at: datetime | None
    exif: dict[str, Any]


def extract_photo_metadata(image_path: str) -> PhotoMetadata:
    """
    Best-effort metadata extraction. EXIF may be missing.
    """
    exif_out: dict[str, Any] = {}
    taken_at: datetime | None = None

    with Image.open(image_path) as img:
        exif = getattr(img, "_getexif", None)
        if not exif:
            return PhotoMetadata(taken_at=None, exif={})
        raw = exif() or {}

        tag_map = {v: k for k, v in ExifTags.TAGS.items()}
        dt_key = tag_map.get("DateTimeOriginal") or tag_map.get("DateTime")

        for tag_id, value in raw.items():
            name = ExifTags.TAGS.get(tag_id, str(tag_id))
            exif_out[name] = value

        if dt_key and dt_key in raw:
            dt_str = str(raw[dt_key])
            for fmt in ("%Y:%m:%d %H:%M:%S", "%Y-%m-%d %H:%M:%S"):
                try:
                    taken_at = datetime.strptime(dt_str, fmt).replace(tzinfo=timezone.utc)
                    break
                except ValueError:
                    continue

    return PhotoMetadata(taken_at=taken_at, exif=exif_out)

