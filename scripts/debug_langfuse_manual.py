import os
from langfuse import Langfuse
import uuid
import time

public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
secret_key = os.getenv("LANGFUSE_SECRET_KEY")
host = os.getenv("LANGFUSE_BASE_URL", "https://cloud.langfuse.com")

client = Langfuse(public_key=public_key, secret_key=secret_key, host=host)

if not client.auth_check():
    print("❌ AUTH FAILED!")
else:
    print("✅ AUTH SUCCESS!")
    
    # In v3.2.1, create an event or start a span directly
    event = client.create_event(
        name="MANUAL_TEST_V3",
        input={"msg": "Manual event test"},
        user_id="son_manual",
        metadata={"sdk_version": "3.2.1"}
    )
    
    # Or start a span
    span = client.start_span(
        name="MANUAL_SPAN_V3",
        input={"action": "test"}
    )
    time.sleep(0.1)
    span.update(output={"result": "success"})
    span.end()
    
    client.flush()
    print("✨ EVENT & SPAN SENT! Check Langfuse now.")
