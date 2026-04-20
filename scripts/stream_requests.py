import time
import json
import random
import httpx
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"
QUERIES_FILE = Path("data/sample_queries.jsonl")

def stream():
    print(f"🚀 Starting live stream to {BASE_URL} every 2 seconds...")
    print(f"Reading from {QUERIES_FILE}")
    
    if not QUERIES_FILE.exists():
        print(f"❌ Error: {QUERIES_FILE} not found!")
        return

    # Load all queries into memory for fast random access
    with open(QUERIES_FILE, "r") as f:
        queries = [json.loads(line) for line in f if line.strip()]

    client = httpx.Client(timeout=10.0)
    
    try:
        while True:
            payload = random.choice(queries)
            try:
                start_time = time.time()
                response = client.post(f"{BASE_URL}/chat", json=payload)
                duration = (time.time() - start_time) * 1000
                
                status_icon = "✅" if response.status_code == 200 else "❌"
                print(f"[{status_icon}] {response.status_code} | {payload.get('feature', 'unknown')} | {duration:.1f}ms")
                
            except Exception as e:
                print(f"❌ Connection error: {e}")
            
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n👋 Stream stopped.")
    finally:
        client.close()

if __name__ == "__main__":
    stream()
