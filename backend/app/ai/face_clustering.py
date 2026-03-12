from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.cluster import DBSCAN


@dataclass(frozen=True)
class ClusterResult:
    labels: list[int]  # -1 indicates noise
    n_clusters: int


def cluster_embeddings(
    embeddings: list[np.ndarray],
    *,
    eps: float = 0.35,
    min_samples: int = 3,
) -> ClusterResult:
    if not embeddings:
        return ClusterResult(labels=[], n_clusters=0)

    X = np.stack([e.astype(np.float32) for e in embeddings], axis=0)
    # cosine distance: 1 - cosine similarity
    clustering = DBSCAN(eps=eps, min_samples=min_samples, metric="cosine").fit(X)
    labels = clustering.labels_.tolist()
    n_clusters = len({l for l in labels if l != -1})
    return ClusterResult(labels=labels, n_clusters=n_clusters)

