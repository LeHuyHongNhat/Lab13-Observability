from __future__ import annotations

import os
from typing import Any
import logging

logger = logging.getLogger("langfuse_tracing")

_client = None

try:
    from langfuse import observe, get_client

    # Langfuse v3.2.1 uses LANGFUSE_BASE_URL, not LANGFUSE_HOST
    # Set it from LANGFUSE_HOST if not already set
    if os.getenv("LANGFUSE_HOST") and not os.getenv("LANGFUSE_BASE_URL"):
        os.environ["LANGFUSE_BASE_URL"] = os.getenv("LANGFUSE_HOST")

    _client = get_client()
    logger.info("Langfuse client initialized successfully")

    class _LangfuseContext:
        """Adapter for langfuse v3.2.1 which has no langfuse_context module."""

        def update_current_trace(self, **kwargs: Any) -> None:
            try:
                _client.update_current_trace(**kwargs)
            except Exception:
                pass

        def update_current_observation(self, **kwargs: Any) -> None:
            try:
                _client.update_current_observation(**kwargs)
            except Exception:
                pass

    langfuse_context = _LangfuseContext()

except Exception as exc:
    logger.warning(f"Langfuse not available, tracing disabled: {exc}")

    def observe(*args: Any, **kwargs: Any):
        def decorator(func):
            return func
        return decorator

    class _DummyContext:
        def update_current_trace(self, **kwargs: Any) -> None:
            pass
        def update_current_observation(self, **kwargs: Any) -> None:
            pass

    langfuse_context = _DummyContext()


def tracing_enabled() -> bool:
    return _client is not None


def flush_traces() -> None:
    if _client is not None:
        try:
            _client.flush()
        except Exception:
            pass
