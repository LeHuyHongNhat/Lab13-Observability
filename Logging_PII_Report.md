# Logging & PII Implementation Report

**Status:** ✅ Completed & Verified (100/100)
**Responsible:** Nguyễn Quốc Khánh (Member A)

## 📌 1. Mục tiêu (Objectives)
Thiết lập hệ thống **Structured Logging** tiêu chuẩn công nghiệp cho AI Agent, đảm bảo khả năng truy vết (Traceability) và bảo mật dữ liệu nhạy cảm (PII Redaction) tuyệt đối.

---

## 🚀 2. Các thành phần đã triển khai (Key Achievements)

### 🧩 A. Correlation ID Middleware (`app/middleware.py`)
- **Cơ chế**: Tự động gán/truyền mã `correlation_id` (format `req-xxxxxxxx`) cho mỗi request.
- **Lợi ích**: Liên kết mọi log phát sinh trong cùng một luồng xử lý từ lúc vào đến lúc ra.
- **Headers**: Trả về `x-request-id` và `x-response-time-ms` cho client để tiện đối soát.

### 📊 B. Log Enrichment (`app/main.py`)
Mọi log record hiện nay đều mang theo ngữ cảnh nghiệp vụ đầy đủ:
- `user_id_hash`: Định danh người dùng (đã hash SHA-256).
- `session_id`: ID phiên làm việc.
- `feature`: Tính năng đang sử dụng (qa, summary...).
- `model`: Model AI xử lý.
- `env`: Môi trường triển khai (dev/prod).

### 🛡️ C. Đa tầng Bảo mật & PII Scrubbing (`app/pii.py` & `app/logging_config.py`)
Hệ thống không chỉ dựa vào Regex mà được thiết kế theo chuẩn **Defense-in-Depth** (Phòng thủ đa lớp):
1. **Lớp 1 (Data Truncation):** Hàm `summarize_text()` chặn đứng rò rỉ văn bản dài bằng cách chỉ giữ lại tối đa 80 ký tự đầu tiên để làm `message_preview`/`answer_preview`. Mọi bí mật nằm phía sau đều bị loại bỏ tự động.
2. **Lớp 2 (One-Way Hashing):** Các định danh cốt lõi như `user_id` đều bị mã hóa một chiều qua SHA-256 ngay lập tức.
3. **Lớp 3 (Advanced Regex Redaction):** Càn quét toàn bộ cấu trúc log ở Root level để ngăn chặn *Data Structure Evasion*, đồng thời mở rộng quy mô lọc lên **18 loại dữ liệu**:
   - **Thông tin cá nhân**: Email (cả dạng thủ thuật thay @ bằng `[at]`), SĐT VN (quốc tế & ngoặc đơn), CCCD (bao gồm loại CMND 9 số cũ), Hộ chiếu (case-insensitive), Ngày sinh (đảo ngược ISO-8601), Biển số xe, Mã Sinh Viên (vd: `21CE0123`).
   - **Tài chính/Bảo mật**: Thẻ tín dụng (13-19 số liền khối / AMEX 15 số), Mã số thuế, Mã OTP / 2FA.
   - **Hệ thống/Network**: JWT, API Keys (kể cả AWS `AKIA...`), Credential URLs (bao hàm DB strings `postgresql://`), Mật khẩu tự nhiên (`my pin code is...`), IPv4/IPv6, MAC Addresses.

---

## ✅ 3. Kết quả kiểm chứng (Verification)

### 📈 Điểm Validation
Đã chạy script `scripts/validate_logs.py` và đạt kết quả tuyệt đối:
- **Score:** `100/100` 💯
- **PII Leaks:** `0` detected.
- **Unique IDs:** Verified.

### 📝 Ví dụ Log thực tế (Sau khi Redacted)
```json
{
  "service": "api",
  "event": "request_received",
  "correlation_id": "req-3c3f3a76",
  "payload": {
    "message_preview": "My email is [REDACTED_EMAIL] and my card is [REDACTED_CREDIT_CARD]"
  },
  "user_id_hash": "2055254ee30a",
  "ts": "2026-04-20T14:40:00Z"
}
```

---

## ⚡ 4. Những lưu ý cho Team
- **Member B (Tracing)**: Có thể sử dụng `correlation_id` này để làm tag chính trong Langfuse nhằm khớp log Backend với Traces.
- **Member D (Incident)**: Khi debug incident, hãy lọc (grep) theo `correlation_id` để thấy toàn bộ lịch sử của request bị lỗi.
- **Common Rule**: KHÔNG BAO GIỜ log trực tiếp `body.user_id` hay thông tin thô, hãy luôn dùng `hash_user_id()` và `summarize_text()`.

---
*Báo cáo được khởi tạo tự động bởi hệ thống hỗ trợ phát triển.*
