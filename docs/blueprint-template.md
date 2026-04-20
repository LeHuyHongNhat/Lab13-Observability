# Lab 13: Observability Blueprint

## 1. Team Metadata
- **GROUP_NAME:** C401-D6

- **REPO_URL:** https://github.com/LeHuyHongNhat/Lab13-Observability

- **MEMBERS:**
  - Member A: Nguyễn Quốc Khánh | Role: Logging & PII Scrubbing
  - Member B: Nguyễn Tuấn Khải | Role: Tracing & Tags
  - Member C: Phan Văn Tấn | Role: SLO & Alerts
  - Member D: Lê Công Thành | Role: Load Test & Incident Generator
  - Member E: Nguyễn Quế Sơn | Role: Dashboard & Evidence Collection
  - Member F: Lê Huy Hồng Nhật | Role: Team Lead, Demo Lead & Blueprint

---

## 2. Executive Summary
- **VALIDATE_LOGS_FINAL_SCORE**: 100/100

- **TOTAL_TRACES_COUNT**: 15+

- **PII_LEAKS_FOUND**: 0

---

## 3. Technical Evidence (Group)

### 3.1 Logging & Tracing
- [EVIDENCE_CORRELATION_ID_SCREENSHOT](../evidence/06_log_samples.png)

- [EVIDENCE_PII_REDACTION_SCREENSHOT](../evidence/04_pii_scrubbing_logs.png)

- [EVIDENCE_TRACE_WATERFALL_SCREENSHOT](../evidence/08_trace_waterfall.png)

- **TRACE_WATERFALL_EXPLANATION**: Span `Chat_Process` ghi lại toàn bộ vòng đời của một request: từ bước RAG (truy xuất tài liệu), LLM sinh câu trả lời giả lập đến tính toán Quality Score. Mọi thông tin về input/output, số lượng token tiêu thụ và độ trễ được Langfuse tự động thu thập.

### 3.2 Dashboard & SLOs
- [DASHBOARD_6_PANELS_SCREENSHOT](../evidence/01_grafana_dashboard.png)

- **SLO_TABLE**:
    | SLI | Target | Window | Current Value |
    |---|---:|---|---:|
    | Latency P95 | < 3000ms | 28d | ~152ms |
    | Error Rate | < 2% | 28d | 0% |
    | Cost Budget | < $2.5/day | 1d | $0.12 |

### 3.3 Alerts & Runbook
- [ALERT_RULES_SCREENSHOT](../evidence/03_prometheus_alerts_list.png)
- [SAMPLE_RUNBOOK_LINK](./alerts.md#2-high-error-rate)

---

## 4. Incident Response Report (Sample)
- **SCENARIO_NAME:** rag_slow

- **SYMPTOMS_OBSERVED:** Khi thực hiện Load Test với concurrency 5, độ trễ phía client tăng vọt từ ~400ms lên hơn 4000ms. Các request vẫn thành công nhưng trải nghiệm người dùng bị ảnh hưởng nghiêm trọng.

- **ROOT_CAUSE_PROVED_BY:** Log file `data/logs.jsonl` ghi nhận flag `incident_enabled` cho `rag_slow`. Trong code `app/mock_rag.py`, hàm `retrieve` bị delay 2.5s khi toggle này được bật.

- **FIX_ACTION:** Thực hiện tắt incident qua lệnh `python scripts/inject_incident.py --scenario rag_slow --disable`.

- **PREVENTIVE_MEASURE:** Thiết lập cảnh báo `High Latency P95` trên Prometheus để phát hiện sớm các trường hợp RAG bị chậm trước khi vi phạm SLO.

---

## 5. Individual Contributions & Evidence

### Nguyễn Quốc Khánh
- [TASKS_COMPLETED]: Triển khai Correlation ID Middleware, cấu hình JSON Logging chuẩn schema, viết bộ lọc PII cho các dữ liệu nhạy cảm.
- [EVIDENCE_LINK (04_pii_scrubbing_logs.png)](../evidence/04_pii_scrubbing_logs.png)

### Nguyễn Tuấn Khải
- [TASKS_COMPLETED]: Tích hợp Langfuse SDK, gắn decorator @observe, cấu hình trace metadata và tag hệ thống cho từng request.
- [EVIDENCE_LINK (08_trace_waterfall.png)](../evidence/08_trace_waterfall.png)

### Phan Văn Tấn
- [TASKS_COMPLETED]: Thiết lập SLO Latency/ErrorRate, viết Alert Rules trong config, soạn thảo Runbook chi tiết để xử lý sự cố.
- [EVIDENCE_LINK (alerts.md)](./alerts.md)

### Lê Công Thành
- [TASKS_COMPLETED]: Thực hiện Load Test giả lập 5-20 user truy cập, thực hiện Inject Incident `rag_slow` để kiểm tra khả năng bắt lỗi của hệ thống.
- [EVIDENCE_LINK (02_alert_firing.png)](../evidence/02_alert_firing.png)

### Nguyễn Quế Sơn
- [TASKS_COMPLETED]: Xây dựng Dashboard 6 panels trên Grafana, thu thập Evidence cho báo cáo, thực hiện xuất Audit Logs để lấy điểm bonus.
- [EVIDENCE_LINK (01_grafana_dashboard.png)](../evidence/01_grafana_dashboard.png)

### Lê Huy Hồng Nhật
- [TASKS_COMPLETED]: Quản trị Repo, điều phối task/branch, viết Blueprint report tổng thể, dẫn dắt Live Demo với Giảng viên.
- [EVIDENCE_LINK (file này)](./blueprint-template.md)

---

## 6. Bonus Items (Optional)
- **BONUS_COST_OPTIMIZATION**: Đã thêm logic tính toán Cost USD chi tiết cho từng Token Usage của LLM.

- **BONUS_AUDIT_LOGS**: Có file `data/audit.jsonl` tách riêng chứa các log quản trị thay đổi incident mode.

- **BONUS_CUSTOM_METRIC**: Thêm metric `quality_score_avg` để theo dõi chất lượng câu trả lời theo thời gian thực.
