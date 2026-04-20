from __future__ import annotations

import os
from typing import Any

try:
    # 1. Try v2 style (langfuse.decorators)
    from langfuse.decorators import observe, langfuse_context
except (ImportError, ModuleNotFoundError):
    try:
        # 2. Try v3+ style (top-level import)
        from langfuse import observe, get_client

        class LangfuseContextWrapper:
            def update_current_trace(self, **kwargs: Any) -> None:
                client = get_client()
                if client:
                    client.update_current_trace(**kwargs)

            def update_current_observation(self, **kwargs: Any) -> None:
                client = get_client()
                if client:
                    client.update_current_span(**kwargs)

        langfuse_context = LangfuseContextWrapper()
    except ImportError:
        # 3. Fallback to dummy mocks
        def observe(*args: Any, **kwargs: Any):
            def decorator(func):
                return func
            return decorator

        class _DummyContext:
            def update_current_trace(self, **kwargs: Any) -> None:
                return None
            def update_current_observation(self, **kwargs: Any) -> None:
                return None

        langfuse_context = _DummyContext()




def tracing_enabled() -> bool:
    return bool(os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"))
