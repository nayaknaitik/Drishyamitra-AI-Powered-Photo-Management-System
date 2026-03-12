"""initial schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-03-12
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "photos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("file_path", sa.String(length=1024), nullable=False),
        sa.Column("original_filename", sa.String(length=512), nullable=True),
        sa.Column("mime_type", sa.String(length=128), nullable=True),
        sa.Column("taken_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_photos_user_id", "photos", ["user_id"])

    op.create_table(
        "persons",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("notes", sa.String(length=1024), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_persons_user_id", "persons", ["user_id"])
    op.create_index("ix_persons_name", "persons", ["name"])

    op.create_table(
        "face_embeddings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("model_name", sa.String(length=128), nullable=False),
        sa.Column("detector_backend", sa.String(length=128), nullable=False),
        sa.Column("vector_dim", sa.Integer(), nullable=False),
        sa.Column("embedding_encrypted", sa.LargeBinary(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_face_embeddings_user_id", "face_embeddings", ["user_id"])

    op.create_table(
        "faces",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("photo_id", sa.Integer(), sa.ForeignKey("photos.id", ondelete="CASCADE"), nullable=False),
        sa.Column("person_id", sa.Integer(), sa.ForeignKey("persons.id", ondelete="SET NULL"), nullable=True),
        sa.Column("embedding_id", sa.Integer(), sa.ForeignKey("face_embeddings.id", ondelete="SET NULL"), nullable=True),
        sa.Column("x", sa.Integer(), nullable=False),
        sa.Column("y", sa.Integer(), nullable=False),
        sa.Column("w", sa.Integer(), nullable=False),
        sa.Column("h", sa.Integer(), nullable=False),
        sa.Column("detection_confidence", sa.Float(), nullable=True),
        sa.Column("is_unknown", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_faces_user_id", "faces", ["user_id"])
    op.create_index("ix_faces_photo_id", "faces", ["photo_id"])
    op.create_index("ix_faces_person_id", "faces", ["person_id"])
    op.create_index("ix_faces_embedding_id", "faces", ["embedding_id"])

    op.create_table(
        "photo_tags",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("photo_id", sa.Integer(), sa.ForeignKey("photos.id", ondelete="CASCADE"), nullable=False),
        sa.Column("key", sa.String(length=64), nullable=False),
        sa.Column("value", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_photo_tags_user_id", "photo_tags", ["user_id"])
    op.create_index("ix_photo_tags_photo_id", "photo_tags", ["photo_id"])
    op.create_index("ix_photo_tags_key", "photo_tags", ["key"])
    op.create_index("ix_photo_tags_value", "photo_tags", ["value"])

    op.create_table(
        "delivery_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("channel", sa.String(length=32), nullable=False),
        sa.Column("destination", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("provider_message_id", sa.String(length=255), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_delivery_logs_user_id", "delivery_logs", ["user_id"])

    op.create_table(
        "chat_history",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("role", sa.String(length=16), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_chat_history_user_id", "chat_history", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_chat_history_user_id", table_name="chat_history")
    op.drop_table("chat_history")

    op.drop_index("ix_delivery_logs_user_id", table_name="delivery_logs")
    op.drop_table("delivery_logs")

    op.drop_index("ix_photo_tags_value", table_name="photo_tags")
    op.drop_index("ix_photo_tags_key", table_name="photo_tags")
    op.drop_index("ix_photo_tags_photo_id", table_name="photo_tags")
    op.drop_index("ix_photo_tags_user_id", table_name="photo_tags")
    op.drop_table("photo_tags")

    op.drop_index("ix_faces_embedding_id", table_name="faces")
    op.drop_index("ix_faces_person_id", table_name="faces")
    op.drop_index("ix_faces_photo_id", table_name="faces")
    op.drop_index("ix_faces_user_id", table_name="faces")
    op.drop_table("faces")

    op.drop_index("ix_face_embeddings_user_id", table_name="face_embeddings")
    op.drop_table("face_embeddings")

    op.drop_index("ix_persons_name", table_name="persons")
    op.drop_index("ix_persons_user_id", table_name="persons")
    op.drop_table("persons")

    op.drop_index("ix_photos_user_id", table_name="photos")
    op.drop_table("photos")

    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")

