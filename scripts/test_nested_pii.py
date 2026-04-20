import json
from pathlib import Path

from app.logging_config import configure_logging, get_logger

configure_logging()
log = get_logger()

def run_tests():
    print("--- CHẠY TEST CASE MÔ PHỎNG LỖ HỔNG NESTED JSON ---")
    
    # Test 1: Mảng (List) chứa dict lồng nhau
    test_1_payload = {
        "event_type": "transaction_failed",
        "chat_history": [
            {"role": "user", "content": "Ngân hàng của tôi là 1234567890 hãy kiểm tra rút tiền."},
            {"role": "agent", "content": "Đang kiểm tra giao dịch."}
        ]
    }
    log.error("nested_list_leak_test", payload=test_1_payload)

    # Test 2: Dict lồng Dict lồng Dict
    test_2_payload = {
        "user_context": {
            "profile": {
                "personal_email": "[email protected]",
                "contact_info": {
                    "home_phone": "0987654321",
                    "id_card": "079099123456"
                }
            }
        }
    }
    log.warning("nested_dict_leak_test", payload=test_2_payload)

    # Test 3: Mixed (Có cả string, list, int, và dict đan xen)
    test_3_payload = {
        "metadata": {
            "attempts": 5,
            "success": False,
            "configs": ["sk-1234567890abcdef1234567890abcdef", {"server_ip": "192.168.1.100"}],
            "note": "Secret password is my_secret_pwd_123"
        }
    }
    log.info("mixed_nested_leak_test", payload=test_3_payload)
    
    print("\nĐã ghi logs ra data/logs.jsonl.")
    print("Hãy kiểm tra file logs.jsonl xem dữ liệu nhảy cảm có bị lọt ra ngoài không nhé!")

if __name__ == "__main__":
    run_tests()
