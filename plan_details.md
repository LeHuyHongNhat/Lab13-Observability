# Kế hoạch & Checklist Chi Tiết Day 13 Observability Lab

Tài liệu này cung cấp **Checklist thực thi cụ thể** cho 6 thành viên. Mỗi task định rõ: **Làm ở đâu? Cách làm đúng? Khi nào xong?**
Timeline giả định Lab diễn ra trong 4 tiếng (Ví dụ: Từ 13:30 - 17:30).

---

## 🧭 Ma trận Phụ thuộc & Luồng phối hợp (Critical Path)

Để dự án trơn tru, các thành viên cần chú ý các "nút thắt" sau:

1.  **Nhật (Team Lead)**: Phải xong **Task 1.1** (Repo) trong 15p đầu để 5 người còn lại có chỗ push code.
2.  **Khánh (Logging)** & **Khải (Tracing)**: Phải xong tính năng cốt lõi (Giờ 1 & 2) thì **Thành (Load Test)** mới có dữ liệu để bắn.
3.  **Thành (Load Test)**: Phải chạy Load Test (Giờ 2) thì **Sơn (Dashboard)** mới thấy biểu đồ nhảy số để chụp ảnh làm bằng chứng.
4.  **Thành (Incident)**: Phải Inject lỗi (Giờ 3) thì **Tấn (Alerts)** mới kiểm tra được chuông có reo hay không và **Nhật (Blueprint)** mới có nội dung viết phần RCA.
5.  **Sơn (Evidence)**: Gom ảnh từ tất cả mọi người (Giờ 4) để hoàn thiện báo cáo.

---

## 1. Lê Huy Hồng Nhật - Vai trò: Team Lead, Demo Lead & Blueprint
**Mục tiêu:** Quản trị dự án, gom bằng chứng và đảm bảo app chạy mượt để Live Demo (20đ nhóm + 20đ cá nhân).

- [ ] **Task 1.1: Khởi tạo Repo & Chia Branch**
  - **Phụ thuộc:** *Tiên phong - Làm đầu tiên.*
  - **Ở đâu:** Terminal / GitHub.
  - **Làm thế nào đúng:** Nhận code từ giảng viên, tạo Repo chung, invite 5 người còn lại.
  - **Khi nào xong:** 30 phút đầu tiên (Giờ thứ 1).
- [ ] **Task 1.2: Soạn lập dàn ý Blueprint**
  - **Phụ thuộc:** Không.
  - **Ở đâu:** `docs/blueprint-template.md`.
  - **Khi nào xong:** Giờ thứ 2.
- [ ] **Task 1.3: Khớp nối Root Cause Analysis (RCA)**
  - **Phụ thuộc:** **Thành (Task 5.3)** - Cần Thành inject lỗi xong mới có cái để phân tích.
  - **Ở đâu:** Phối hợp với Thành (Member D), ghi vào `docs/blueprint-template.md`.
  - **Khi nào xong:** Giờ thứ 3.
- [ ] **Task 1.4: Chuẩn bị & Chạy Live Demo**
  - **Phụ thuộc:** **Cả đội** - Cần mọi người merge PR để có bản code cuối cùng.
  - **Khi nào xong:** 30 phút cuối cùng.

---

## 2. Nguyễn Quốc Khánh - Vai trò: Logging & PII Scrubbing
**Mục tiêu:** JSON format log, Correlation ID xuyên suốt, Redact PII.

- [ ] **Task 2.1: Implement Correlation ID Middleware**
  - **Phụ thuộc:** **Nhật (Task 1.1)** - Cần Repo để tạo branch.
  - **Ở đâu:** `app/middleware.py`.
  - **Khi nào xong:** Giờ thứ 1.
- [ ] **Task 2.2: Redact PII bằng Regex**
  - **Phụ thuộc:** Xong Middleware.
  - **Ở đâu:** `app/pii.py`.
  - **Khi nào xong:** Giờ thứ 2.
- [ ] **Task 2.3: Validate format JSON Logs**
  - **Phụ thuộc:** Xong code PII.
  - **Khi nào xong:** Nửa đầu Giờ thứ 3.

---

## 3. Nguyễn Tuấn Khải - Vai trò: Tracing & Tags
**Mục tiêu:** 10+ traces hợp lệ bắn lên Langfuse.

- [ ] **Task 3.1: Đảm bảo langfuse_context hoạt động**
  - **Phụ thuộc:** **Nhật (Task 1.1)**.
  - **Ở đâu:** `app/tracing.py`.
  - **Khi nào xong:** Giờ thứ 1.
- [ ] **Task 3.2: Gắn Decorator @observe**
  - **Phụ thuộc:** Xong Task 3.1.
  - **Khi nào xong:** Giờ thứ 2.
- [ ] **Task 3.3: Xác minh Traces lên UI**
  - **Phụ thuộc:** **Thành (Task 5.1)** - Thành chạy Load Test thì Khải mới có nhiều Traces đẹp để kiểm tra.
  - **Khi nào xong:** Giờ thứ 3.

---

## 4. Phan Văn Tấn - Vai trò: SLO & Alerts
**Mục tiêu:** Ngưỡng cảnh báo và Runbook.

- [ ] **Task 4.1: Định hình SLO cho dự án**
  - **Phụ thuộc:** Nhật (Task 1.1).
  - **Khi nào xong:** Giờ thứ 1.
- [ ] **Task 4.2: Thiết lập Alert Rules**
  - **Phụ thuộc:** Xong SLO.
  - **Khi nào xong:** Giờ thứ 2.
- [ ] **Task 4.3: Soạn Runbook cho Alerts**
  - **Phụ thuộc:** **Thành (Task 5.3)** - Test alert xem có trigger như kịch bản không.
  - **Khi nào xong:** Giờ thứ 3.

---

## 5. Lê Công Thành - Vai trò: Load Test & Incident Generator
**Mục tiêu:** Stress-test và tạo lỗi giả định.

- [ ] **Task 5.1: Chạy mô phỏng tải bình thường**
  - **Phụ thuộc:** **Khánh (Task 2.1)** & **Khải (Task 3.2)** - App phải có log/trace mới bõ công test.
  - **Khi nào xong:** Giờ thứ 2.
- [ ] **Task 5.2: Setup các Incident Mode**
  - **Phụ thuộc:** Không.
  - **Khi nào xong:** Giờ thứ 3.
- [ ] **Task 5.3: Thực hiện "phá hoại" (Inject Incident)**
  - **Phụ thuộc:** Nhật thông báo bắt đầu phase "Diễn tập sự cố".
  - **Khi nào xong:** Nửa sau Giờ thứ 3.

---

## 6. Nguyễn Quế Sơn - Vai trò: Dashboard & Evidence Collection
**Mục tiêu:** Dashboard 6 panels và Evidence.

- [ ] **Task 6.1: Khai thác Metrics**
  - **Phụ thuộc:** Khánh (Xong middleware/app structure).
  - **Khi nào xong:** Giờ thứ 2.
- [ ] **Task 6.2: Xây Dashboard Grafana**
  - **Phụ thuộc:** **Thành (Task 5.1)** - Cần Thành bắn tải thì biểu đồ Dashboard mới có sóng để chụp ảnh.
  - **Khi nào xong:** Giờ thứ 3.
- [ ] **Task 6.3: Gom Evidence Document**
  - **Phụ thuộc:** **Tất cả mọi người** - Chỉ gom được khi các bạn đã làm xong việc kỹ thuật.
  - **Khi nào xong:** Giờ thứ 4.
