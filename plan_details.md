# Kế hoạch & Checklist Chi Tiết Day 13 Observability Lab

Tài liệu này cung cấp **Checklist thực thi cụ thể** cho 6 thành viên. Mỗi task định rõ: **Làm ở đâu? Cách làm đúng? Khi nào xong?**
Timeline giả định Lab diễn ra trong 4 tiếng (Ví dụ: Từ 13:30 - 17:30).

---

## 1. Lê Huy Hồng Nhật - Vai trò: Team Lead, Demo Lead & Blueprint
**Mục tiêu:** Quản trị dự án, gom bằng chứng và đảm bảo app chạy mượt để Live Demo (20đ nhóm + 20đ cá nhân).

- [ ] **Task 1.1: Khởi tạo Repo & Chia Branch**
  - **Ở đâu:** Terminal / GitHub.
  - **Làm thế nào đúng:** Nhận code từ giảng viên, tạo Repo chung, invite 5 người còn lại. Yêu cầu mọi người tạo nhánh riêng (vd: `feature/logging-khanh`) và tạo Pull Request (PR) khi xong.
  - **Khi nào xong:** 30 phút đầu tiên (Giờ thứ 1).
- [ ] **Task 1.2: Soạn lập dàn ý Blueprint**
  - **Ở đâu:** `docs/blueprint-template.md`.
  - **Làm thế nào đúng:** Chia sẵn các heading cho từng thành viên tự vào điền. Nhắc nhở mọi người ghi chú kiến thức học được.
  - **Khi nào xong:** Giờ thứ 2.
- [ ] **Task 1.3: Khớp nối Root Cause Analysis (RCA)**
  - **Ở đâu:** Phối hợp với Thành (Member D), ghi vào `docs/blueprint-template.md`.
  - **Làm thế nào đúng:** Khi Thành gây ra lỗi (Incident), dùng Trace và Log để phân tích lỗi do đâu (vd: do mock_rag.py bị delay). Phải vẽ được flow: Cảnh báo -> Xem bảng Dash -> Lần theo trace -> Ra log gốc.
  - **Khi nào xong:** Giờ thứ 3.
- [ ] **Task 1.4: Chuẩn bị & Chạy Live Demo**
  - **Ở đâu:** Codebase trên máy local của Nhật.
  - **Làm thế nào đúng:** Pull toàn bộ code từ nhánh `main` sau khi merge PRs. Chạy `uvicorn app.main:app` mượt mà, mở sẵn các tab Grafana/Langfuse, tập diễn đạt theo file `docs/mock-debug-qa.md`.
  - **Khi nào xong:** 30 phút cuối cùng.

---

## 2. Nguyễn Quốc Khánh - Vai trò: Logging & PII Scrubbing
**Mục tiêu:** JSON format log, Correlation ID xuyên suốt, Redact PII (Log ẩn thông tin nhạy cảm).

- [ ] **Task 2.1: Implement Correlation ID Middleware**
  - **Ở đâu:** `app/middleware.py`.
  - **Làm thế nào đúng:** Sinh ra một UUID cho mỗi request đến. Gắn nó vào header `x-request-id` của response, đồng thời đưa vào `structlog` context để in ra cùng mọi log.
  - **Khi nào xong:** Giờ thứ 1.
- [ ] **Task 2.2: Redact PII bằng Regex**
  - **Ở đâu:** `app/pii.py` và `app/logging_config.py`.
  - **Làm thế nào đúng:** Bổ sung regex tìm Số điện thoại/Email trong text và thay bằng `[REDACTED]`. Đảm bảo các field JSON cấu hình `structlog` ẩn dữ liệu trước khi in ra stdout. 
  - **Khi nào xong:** Giờ thứ 2.
- [ ] **Task 2.3: Validate format JSON Logs**
  - **Ở đâu:** Terminal, chạy `python scripts/validate_logs.py`.
  - **Làm thế nào đúng:** Output script phải báo xanh và `VALIDATE_LOGS_SCORE >= 80/100`. Nếu lỗi, quay lại `app/main.py` để bổ sung tag user_id, session_id còn thiếu.
  - **Khi nào xong:** Nửa đầu Giờ thứ 3.

---

## 3. Nguyễn Tuấn Khải - Vai trò: Tracing & Tags
**Mục tiêu:** 10+ traces hợp lệ bắn lên Langfuse chứa metadata đầy đủ.

- [ ] **Task 3.1: Đảm bảo langfuse_context hoạt động**
  - **Ở đâu:** `app/tracing.py`.
  - **Làm thế nào đúng:** Đã có code Wrapper v3. Chỉ cần hướng dẫn cả nhóm duplicate `.env.example` thành `.env`, điền `LANGFUSE_PUBLIC_KEY` và `LANGFUSE_SECRET_KEY` lấy từ website Langfuse.
  - **Khi nào xong:** Giờ thứ 1.
- [ ] **Task 3.2: Gắn Decorator @observe**
  - **Ở đâu:** Các hàm core trong `app/agent.py` (vd: `run()`, `retrieve()`) và `app/main.py`.
  - **Làm thế nào đúng:** Import `@observe()` từ `langfuse` (hoặc `app.tracing`). Đảm bảo function chạy xong không crash. Ở những chỗ cần, gọi `langfuse_context.update_current_trace()` để đính `user_id`.
  - **Khi nào xong:** Giờ thứ 2.
- [ ] **Task 3.3: Xác minh Traces lên UI**
  - **Ở đâu:** Giao diện website Langfuse của project.
  - **Làm thế nào đúng:** Chạy app, tạo 10 - 20 requests qua API (hoặc nhờ Thành chạy load test). Mở Langfuse UI kiểm tra phần Traces xem có hiện đủ metadata `doc_count`, `feature` không.
  - **Khi nào xong:** Giờ thứ 3.

---

## 4. Phan Văn Tấn - Vai trò: SLO & Alerts
**Mục tiêu:** Sinh ra ngưỡng cảnh báo hệ thống, bộ hồ sơ xử lý sự cố (Runbook).

- [ ] **Task 4.1: Định hình SLO cho dự án**
  - **Ở đâu:** `config/slo.yaml`.
  - **Làm thế nào đúng:** Viết file yaml rõ ràng: Target 99% requests phản hồi dưới 500ms; Error rate (Code 5xx) phải dưới 1%. 
  - **Khi nào xong:** Giờ thứ 1.
- [ ] **Task 4.2: Thiết lập Alert Rules**
  - **Ở đâu:** `config/alert_rules.yaml`.
  - **Làm thế nào đúng:** Hiện thực hóa ít nhất 3 rule (High Latency, High Error Rate, High Traffic) theo format chuẩn PromQL hoặc dạng mô tả yaml đơn giản. 
  - **Khi nào xong:** Giờ thứ 2.
- [ ] **Task 4.3: Soạn Runbook cho Alerts**
  - **Ở đâu:** `docs/alerts.md`.
  - **Làm thế nào đúng:** Ánh xạ 3 rule trên thành 3 kịch bản xử lý. VD: *Nếu High Latency nhảy đỏ -> Bật Langfuse check trace xem do `mock_rag` hay `mock_llm` -> Nếu do LLM thì tắt tính năng/Restart.*
  - **Khi nào xong:** Giờ thứ 3.

---

## 5. Lê Công Thành - Vai trò: Load Test & Incident Generator
**Mục tiêu:** Stress-test ứng dụng và tạo "hiện trường giả" cho nhóm tập bắt lỗi.

- [ ] **Task 5.1: Chạy mô phỏng tải bình thường**
  - **Ở đâu:** Terminal, chạy lệnh `python scripts/load_test.py --concurrency 5`.
  - **Làm thế nào đúng:** Code kịch bản load_test.py phải gọi được vào endpoint FastAPI của Nhật. Kiểm tra xem app có bị treo khi đồng thời có 5 request không.
  - **Khi nào xong:** Giờ thứ 2 (Ngay khi nhánh core ráp vào).
- [ ] **Task 5.2: Setup các Incident Mode**
  - **Ở đâu:** `app/incidents.py` và `scripts/inject_incident.py`.
  - **Làm thế nào đúng:** Sửa code trong `incidents.py` để khi cờ `rag_slow = True` thì `app/agent.py` bị delay thêm 2-3s (dùng `time.sleep()`). 
  - **Khi nào xong:** Nửa đầu Giờ thứ 3.
- [ ] **Task 5.3: Thực hiện "phá hoại" (Inject Incident)**
  - **Ở đâu:** Terminal, chạy `python scripts/inject_incident.py --scenario rag_slow`.
  - **Làm thế nào đúng:** Báo cho nhóm biết hệ thống đang lỗi. Yêu cầu Tấn kiểm tra Alert xem có bắn không, Nhật dùng Langfuse tìm xem đoạn code nào bị slow (có phải do `time.sleep` mình vừa thả).
  - **Khi nào xong:** Nửa sau Giờ thứ 3.

---

## 6. Nguyễn Quế Sơn - Vai trò: Dashboard & Evidence Collection
**Mục tiêu:** 1 Dashboard đầy đủ 6 panels, mọi kết quả làm việc phải có minh chứng rõ ràng.

- [ ] **Task 6.1: Khai thác Metrics**
  - **Ở đâu:** `app/metrics.py`.
  - **Làm thế nào đúng:** Nắm rõ metric nào đang export (counter error, histogram latency). Nếu thiếu thì thêm biến global theo hướng dẫn của dự án để expose qua `/metrics`.
  - **Khi nào xong:** Giờ thứ 2.
- [ ] **Task 6.2: Xây Dashboard Grafana**
  - **Ở đâu:** Dashboard Tool (Prometheus/Grafana hoặc công cụ theo chuẩn Lab).
  - **Làm thế nào đúng:** Check `docs/dashboard-spec.md`. Làm đủ 6 panels: *Request count, Error rate, Latency p95, Token usage, ...*. Chú ý kẻ vạch SLO (ví dụ đường chỉ đỏ nằm tại mốc 500ms).
  - **Khi nào xong:** Giờ thứ 3.
- [ ] **Task 6.3: Gom Evidence Document**
  - **Ở đâu:** `docs/grading-evidence.md`.
  - **Làm thế nào đúng:** Chụp màn hình Dashboard đẹp nhất. Chụp màn hình 1 trace từ Langfuse. Xin link Pull Request của Khánh, Khải, Tấn dán vào. Nếu có Audit Logs `data/audit.jsonl`, chụp vào mục Bonus.
  - **Khi nào xong:** Giờ thứ 4.
