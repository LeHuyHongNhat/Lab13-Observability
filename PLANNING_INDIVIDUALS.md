# Kế hoạch triển khai Day 13 Observability Lab

Dựa trên yêu cầu của `README.md` và `day13-rubric-for-instructor.md`, lab có mục tiêu xây dựng một FastAPI agent với đầy đủ structured logging, tracing, dashboard, và alerting. Bài lab dùng mô hình điểm **60/40** (60 điểm nhóm, 40 điểm cá nhân). Nhóm có 6 thành viên, tương ứng phân chia thành 6 vai trò đảm bảo công việc đồng đều, phát huy tối đa khả năng để dễ dàng lấy trọn vẹn điểm cá nhân và điểm nhóm.

## Phân công vai trò & Kế hoạch chi tiết

### 1. Lê Huy Hồng Nhật (Tôi) - Vai trò: Member F (Blueprint, Demo Lead & Tiên phong dự án)
- **Nhiệm vụ chính:** Quản lý chung, viết báo cáo tổng kết (Blueprint), đảm bảo tiến độ và dẫn dắt phần Live Demo.
- **Chi tiết công việc:**
  - Xử lý và hoàn thiện file `docs/blueprint-template.md` (tổng hợp phần báo cáo của tất cả thành viên).
  - Phối hợp với Thành (Incident) để giải thích Root Cause Analysis (RCA) trong báo cáo.
  - Đảm bảo app khởi chạy mượt mà, chuẩn bị kịch bản thuyết trình cho Live Demo (mục tiêu đạt tối đa 20đ Demo).
  - Trình bày tổng quan hệ thống, workflow của middleware và logging pipeline trước giảng viên.
  - Hỗ trợ các thành viên khác gỡ lỗi chéo nếu hệ thống không đạt được `VALIDATE_LOGS_SCORE`.
- **KPI Cá nhân:** File báo cáo Blueprint hoàn chỉnh, demo không dính lỗi runtime, nắm rõ toàn bộ kiến trúc để thay mặt nhóm trả lời những câu hỏi tổng quan của giảng viên.

### 2. Nguyễn Quốc Khánh - Vai trò: Member A (Logging & PII Scrubbing)
- **Nhiệm vụ chính:** Đảm bảo JSON logs schema chuẩn xác, implement correlation ID và cơ chế làm sạch dữ liệu nhạy cảm (PII).
- **Chi tiết công việc:**
  - `app/middleware.py`: Cấu hình để mọi request đi qua đều được gán `x-request-id` hợp lệ liên tục.
  - `app/main.py`: Bind các metadata quan trọng như user, session, feature context vào trong log struct.
  - `app/logging_config.py` & `app/pii.py`: Viết và cấu hình PII scrubber bằng Regex (ẩn thông tin cá nhân khách hàng).
  - Thường xuyên chạy `python scripts/validate_logs.py` để giữ mức điểm Validation Score >= 80/100.
- **KPI Cá nhân:** Dữ liệu PII bị redact 100%, logs tuân thủ nghiêm ngặt logging_schema.json, sẵn sàng giải thích Logic Regex với giảng viên.

### 3. Nguyễn Tuấn Khải - Vai trò: Member B (Tracing & Tags)
- **Nhiệm vụ chính:** Tích hợp Langfuse để lưu vết (trace) mọi request vào hệ thống.
- **Chi tiết công việc:**
  - `app/tracing.py`: Cấu hình Langfuse helpers và authentication.
  - Khai báo decorator `@observe()` tại các function xử lý chính trong `app/agent.py` và `app/main.py`.
  - Thực hiện gửi request test bằng kịch bản cho sẵn và chốt lại **ít nhất 10 traces** hiển thị rõ ràng trên bảng điều khiển Langfuse.
- **KPI Cá nhân:** Đạt điều kiện ti quyết "10 traces live", hiểu rõ khái niệm span, trace, và cách gắn tag cho mỗi step xử lý.

### 4. Phan Văn Tấn - Vai trò: Member C (SLO & Alerts)
- **Nhiệm vụ chính:** Định nghĩa tài liệu SLO và thiết lập quy tắc Alerting khi hệ thống gặp rủi ro.
- **Chi tiết công việc:**
  - `config/slo.yaml`: Xác định SLO tối thiểu cho độ trễ (Latency) và Tỷ lệ lỗi (Error Rate).
  - `config/alert_rules.yaml`: Khởi tạo tối thiểu 3 bộ cảnh báo (vd: Latency vượt mức thời gian cấu hình, Traffic giảm đột ngột, Lỗi 5xx tăng cao).
  - Cập nhật file `docs/alerts.md`: Soạn thảo Runbook chứa cẩm nang xử lý nếu từng luật cảnh báo ở trên bị trigger.
- **KPI Cá nhân:** Có sẵn ít nhất 3 alerts đã map với runbook hợp lý. Bảo vệ được với giảng viên về cách tính độ đo P95 và khái niệm SLO error budget.

### 5. Lê Công Thành - Vai trò: Member D (Load Test & Incident Debugging)
- **Nhiệm vụ chính:** Tạo gánh nặng tải, mô phỏng lỗi (incident) để thử thách công việc của C và lấy dữ liệu RCA.
- **Chi tiết công việc:**
  - `scripts/load_test.py`: Thực thi kịch bản tạo vô số request đồng thời bằng parameter `--concurrency 5`.
  - `scripts/inject_incident.py`: Kích hoạt một lỗi ngầm (như `--scenario rag_slow`) sinh ra các dòng log bị chậm hoặc thất bại.
  - `app/incidents.py`: Rà soát code toggle cho failed mode để đảm bảo lab vận hành như thực tế.
  - Ghi chép cách debug bắt đầu từ Metrics trượt dốc -> Check Traces chậm -> Xem Logs báo lỗi -> Đưa cho Nhật nộp chấm 10đ Incident.
- **KPI Cá nhân:** Phục vụ đủ lượng request traffic lớn cho team, phân tích trúng root cause của kịch bản inject. Điểm Nhóm 10đ Debugging.

### 6. Nguyễn Quế Sơn - Vai trò: Member E (Dashboard & Evidence Collection)
- **Nhiệm vụ chính:** Trình bày số liệu qua Dashboard cho mãn nhãn, thu thập chứng cứ (Evidence) vào doc.
- **Chi tiết công việc:**
  - Giao tiếp với `app/metrics.py` xuất số liệu cần thiết.
  - Thiết kế Dashboard 6-panel theo danh sách tại `docs/dashboard-spec.md` (Chú ý gán đúng label trục X/Y, đường kẻ Threshold/SLO line).
  - Đóng góp vào `docs/grading-evidence.md`: Thêm mã PR/Commit, ảnh chụp Grafana/Langfuse cho từng gạch đầu dòng chấm điểm.
  - Cày phần Bonus: Làm Dashboard UI xuất sắc hoặc thu thập cả file Audit log `data/audit.jsonl` tách biệt (+ Bonus points).
- **KPI Cá nhân:** Có đầy đủ 6 panels hoàn mỹ trên Dashboard, minh chứng PDF/ảnh sắc nét cho mọi tính năng của cả team. Lấy thêm điểm Bonus.

---

## Timeline & Lộ trình thực hiện lý tưởng (4 Tiếng)

1. **Giai đoạn 1 (Setup & Phân tách việc - Tiếng 1)**
   - Nhật: Tạo remote repo, cài đặt project và chia task/branch. Phân mảng Git để mọi người dễ bề Commit kiếm điểm (B2: Evidence of Work).
   - Khánh & Tấn: Tiến hành thiết lập cơ bản về format logging JSON, Middleware và nháp rule Alerts.

2. **Giai đoạn 2 (Tính năng cốt lõi - Tiếng 2)**
   - Khánh: Deploy PII Regex rồi test script `validate_logs.py`. 
   - Khải: Gắn Langfuse cho middleware và các class gọi ngoại vi.
   - Thành: Init Load Test nhẹ để kéo dữ liệu về cho Khải kiểm tra span.

3. **Giai đoạn 3 (Giám sát & Sự cố - Tiếng 3)**
   - Thành: Bật incident mode (thả lỗi vào code).
   - Sơn: Trực quan hóa log lỗi, pull metrics qua Dashboard. Vẽ threshold đứt khúc. 
   - Nhật & Thành: Xúm lại debug tìm theo dấu trace để xác định lỗi chậm ở RAG.

4. **Giai đoạn 4 (Tài liệu hóa & Tổng duyệt - Tiếng 4)**
   - Nhóm: Submit hết code qua Pull Request, Approve chéo nhau.
   - Sơn & Nhật: Update file `evidence` và `blueprint`. 
   - Cả team: Diễn tập quá trình live_demo, thử hỏi xoáy các câu hỏi tại `docs/mock-debug-qa.md` để tự tin trình bày.
