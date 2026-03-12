from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class StoragePaths:
    upload_root: str

    def user_dir(self, user_id: int) -> str:
        return os.path.join(self.upload_root, str(user_id))

    def photo_path(self, user_id: int, photo_id: int, ext: str = ".jpg") -> str:
        return os.path.join(self.user_dir(user_id), f"{photo_id}{ext}")


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

