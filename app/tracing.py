from __future__ import annotations

import os
import logging
from langfuse import Langfuse, observe

logger = logging.getLogger("langfuse_tracing")

# Initialize client
langfuse_client = Langfuse()

def tracing_enabled() -> bool:
    return bool(os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"))

def flush_traces() -> None:
    try:
        langfuse_client.flush()
    except Exception as e:
        logger.error(f"Failed to flush traces: {e}")
