from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import cv2
import numpy as np
from deepface import DeepFace


@dataclass(frozen=True)
class DetectedFace:
    x: int
    y: int
    w: int
    h: int
    confidence: float | None


def decode_image_bytes(image_bytes: bytes) -> np.ndarray:
    arr = np.frombuffer(image_bytes, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Invalid image bytes")
    return img


def detect_faces(
    img_bgr: np.ndarray,
    *,
    detector_backend: str = "retinaface",
    enforce_detection: bool = False,
) -> list[DetectedFace]:
    """
    Returns face bounding boxes in pixel coordinates.

    DeepFace uses different face object formats depending on backend; we normalize.
    """
    faces: list[dict[str, Any]] = DeepFace.extract_faces(
        img_path=img_bgr,
        detector_backend=detector_backend,
        enforce_detection=enforce_detection,
        align=True,
    )

    out: list[DetectedFace] = []
    for f in faces:
        area = f.get("facial_area") or {}
        out.append(
            DetectedFace(
                x=int(area.get("x", 0)),
                y=int(area.get("y", 0)),
                w=int(area.get("w", 0)),
                h=int(area.get("h", 0)),
                confidence=(float(f.get("confidence")) if f.get("confidence") is not None else None),
            )
        )
    return out

