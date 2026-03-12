"""
Drishyamitra backend application package.

Clean Architecture layers live under:
- api/: HTTP layer (Flask blueprints, request/response)
- services/: use-cases + orchestration
- ai/: model-facing logic (DeepFace, embeddings, clustering, indexing)
- models/: ORM models
- schemas/: serialization/validation
- utils/: cross-cutting utilities
- workers/: celery tasks
"""

