from __future__ import annotations

import numpy as np

from app.ai.face_recognition import cosine_similarity


def test_cosine_similarity_identity():
    a = np.array([1.0, 2.0, 3.0], dtype=np.float32)
    assert abs(cosine_similarity(a, a) - 1.0) < 1e-5

