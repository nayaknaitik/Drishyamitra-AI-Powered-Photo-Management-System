from __future__ import annotations

import base64
import os
from dataclasses import dataclass

from cryptography.fernet import Fernet
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def _derive_fernet_key(secret: str) -> bytes:
    raw = secret.encode("utf-8")
    padded = (raw * (32 // len(raw) + 1))[:32]
    return base64.urlsafe_b64encode(padded)


@dataclass(frozen=True)
class EmbeddingCrypto:
    fernet: Fernet

    @classmethod
    def from_secret(cls, secret: str) -> "EmbeddingCrypto":
        return cls(fernet=Fernet(_derive_fernet_key(secret)))

    def encrypt(self, data: bytes) -> bytes:
        return self.fernet.encrypt(data)

    def decrypt(self, token: bytes) -> bytes:
        return self.fernet.decrypt(token)

