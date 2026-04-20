import json
import time
import httpx

BASE_URL = "http://127.0.0.1:8000"

def log_step(message):
    print(f"\n[{time.strftime('%H:%M:%S')}] 🚀 {message}")
    print("-" * 50)

def send_chat(client, feature, message):
    payload = {
        "user_id": "tester_01",
        "session_id": "e2e_session",
        "feature": feature,
        "message": message
    }
    try:
        r = client.post(f"{BASE_URL}/chat", json=payload, timeout=15.0)
        print(f"  → [{r.status_code}] {payload['feature']}: {r.json().get('correlation_id', 'Error')}")
    except Exception as e:
        print(f"  → Server sập hoặc Timeout: {e}")

def toggle_incident(client, name, enable=True):
    action = "enable" if enable else "disable"
    try:
        r = client.post(f"{BASE_URL}/incidents/{name}/{action}")
        print(f"  → Incident '{name}' - {action.upper()}: {r.status_code}")
    except Exception:
        print(f"  → Lỗi khi chỉnh dửa Incident {name}")

def main():
    print("=" * 60)
    print("🎬 BẮT ĐẦU KỊCH BẢN TEST TOÀN DIỆN (E2E OBSERVABILITY)")
    print("=" * 60)
    
    with httpx.Client() as client:
        # 1. Traffic Bình Thường
        log_step("PHASE 1: HỆ THỐNG YÊN BÌNH (Chạy mượt mà)")
        for _ in range(3):
            send_chat(client, "qa", "Xin chào, hệ thống bạn dạo này thế nào?")
            time.sleep(1)

        # 2. Xảy ra sự cố Đứt kết nối nội bộ
        log_step("PHASE 2: SỰ CỐ ĐỨT CÁP - LỖI HÀNG LOẠT (Test Error Rate & Alerts)")
        toggle_incident(client, "tool_fail", enable=True)
        for _ in range(3):
            send_chat(client, "coding", "Code cho tôi một website!")
        toggle_incident(client, "tool_fail", enable=False) # Tắt đi để test phase sau

        # 3. Sự cố RAG Slow (Tăng Latency)
        log_step("PHASE 3: SERVER BỊ QUÁ TẢI (Test Latency P95 & P99 vọt lên)")
        toggle_incident(client, "rag_slow", enable=True)
        send_chat(client, "qa", "Hãy tìm kiếm trong database 10 tỷ dòng.")
        send_chat(client, "policy_check", "Tìm luật lao động năm 2024.")
        toggle_incident(client, "rag_slow", enable=False)

        # 4. Tấn công PII tinh vi lồng sâu (Nested Payload Leak)
        log_step("PHASE 4: HACKER CHÈN PII VÀO PAYLOAD (Test Security Scrubbing)")
        tricky_payload = "Mật khẩu của tôi là [email protected] và CCCD: 001099123456"
        send_chat(client, "it_support", f"Khách hàng báo cáo: {tricky_payload}")

        log_step("✅ KỊCH BẢN HOÀN TẤT!")
        print("Bây giờ hãy mở Grafana lên, bạn sẽ thấy:")
        print("  1. Đồ thị Error Rate nhô lên một đỉnh đỏ lòm ở Phase 2.")
        print("  2. Đồ thị Latency P95 chọc trời lủng mây ở Phase 3.")
        print("  3. File data/logs.jsonl của Phase 4 không hề bị lọt email CCCD ra ngoài.")

if __name__ == "__main__":
    main()
