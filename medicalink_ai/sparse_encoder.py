"""Sparse vectors (BM25-style) qua FastEmbed — dùng cho hybrid search trên Qdrant."""

from __future__ import annotations

import logging
from functools import lru_cache

from typing import Any

from qdrant_client.models import SparseVector

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def _get_sparse_model(model_name: str) -> Any:
    """Khởi tạo và cache model FastEmbed (synchronous)."""
    from fastembed import SparseTextEmbedding

    return SparseTextEmbedding(model_name=model_name)


def text_to_sparse_vector(text: str, model_name: str, max_chars: int = 8000) -> SparseVector:
    """
    Chuyển đổi văn bản thành SparseVector sử dụng FastEmbed.
    Lưu ý: Đây là hàm CPU-bound đồng bộ (synchronous). 
    Cần chạy qua asyncio.to_thread() nếu gọi từ luồng async.
    """
    model = _get_sparse_model(model_name)
    chunk = text.replace("\n", " ").strip()[:max_chars] or " "
    emb = next(model.embed([chunk]))
    obj = emb.as_object()
    idx = obj["indices"]
    val = obj["values"]
    indices = [int(x) for x in idx.tolist()]
    values = [float(x) for x in val.tolist()]
    return SparseVector(indices=indices, values=values)
