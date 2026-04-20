# Day 13 Observability Lab Report

> **Instruction**: Fill in all sections below. This report is designed to be parsed by an automated grading assistant. Ensure all tags (e.g., `[GROUP_NAME]`) are preserved.

## 1. Team Metadata
- [GROUP_NAME]: C401-D6
- [REPO_URL]: https://github.com/LeHuyHongNhat/Lab13-Observability
- [MEMBERS]:
  - Member A: Nguyễn Quốc Khánh | Role: Logging & PII Scrubbing
  - Member B: Nguyễn Tuấn Khải | Role: Tracing & Tags
  - Member C: Phan Văn Tấn | Role: SLO & Alerts
  - Member D: Lê Công Thành | Role: Load Test & Incident Generator
  - Member E: Nguyễn Quế Sơn | Role: Dashboard & Evidence Collection
  - Member F: Lê Huy Hồng Nhật | Role: Team Lead, Demo Lead & Blueprint

---

## 2. Group Performance (Auto-Verified)
- [VALIDATE_LOGS_FINAL_SCORE]: 88/100
- [TOTAL_TRACES_COUNT]: 15
- [PII_LEAKS_FOUND]: 0

---

## 3. Technical Evidence (Group)

### 3.1 Logging & Tracing
- [EVIDENCE_CORRELATION_ID_SCREENSHOT]: [Path to image]
- [EVIDENCE_PII_REDACTION_SCREENSHOT]: [Path to image]
- [EVIDENCE_TRACE_WATERFALL_SCREENSHOT]: [Path to image]
- [TRACE_WATERFALL_EXPLANATION]: (Briefly explain one interesting span in your trace)

### 3.2 Dashboard & SLOs
- [DASHBOARD_6_PANELS_SCREENSHOT]: [Path to image]
- [SLO_TABLE]:
| SLI | Target | Window | Current Value |
|---|---:|---|---:|
| Latency P95 | < 3000ms | 28d | |
| Error Rate | < 2% | 28d | |
| Cost Budget | < $2.5/day | 1d | |

### 3.3 Alerts & Runbook
- [ALERT_RULES_SCREENSHOT]: [Path to image]
- [SAMPLE_RUNBOOK_LINK]: [docs/alerts.md#L...]

---

## 4. Incident Response (Group)
- [SCENARIO_NAME]: rag_slow
- [SYMPTOMS_OBSERVED]: Baseline load test (concurrency 5) returned 10/10 successful requests with client-observed latency mostly in 311-768ms. After enabling rag_slow, the same workload still returned 10/10 successful requests but latency jumped to 2.66s-13.27s at client side. In service logs, `response_sent.latency_ms` increased from a stable 150ms baseline to a stable 2650ms under incident.
- [ROOT_CAUSE_PROVED_BY]: `data/logs.jsonl` line 21 records `incident_enabled` for `rag_slow`; `app/mock_rag.py` line 17 gates a deliberate `time.sleep(2.5)` when `STATE["rag_slow"]` is true, directly causing the latency increase.
- [FIX_ACTION]: Disable incident via `python scripts/inject_incident.py --scenario rag_slow --disable`, then rerun load test to verify latency returns to baseline profile.
- [PREVENTIVE_MEASURE]: Add alert monitoring for latency P95, include incident-toggle check as the first runbook step, and keep baseline-vs-incident replay as a mandatory pre-demo verification.

---

## 5. Individual Contributions & Evidence

### Nguyễn Quốc Khánh
- [TASKS_COMPLETED]: Triển khai Correlation ID Middleware, cấu hình JSON Logging chuẩn schema, viết bộ lọc PII cho Điện thoại, CCCD và dữ liệu cá nhân VN.
- [EVIDENCE_LINK]: commit/7a... (Implement logging & PII filter)

### Nguyễn Tuấn Khải
- [TASKS_COMPLETED]: Tích hợp Langfuse SDK, gắn decorator @observe, cấu hình trace metadata và tag hệ thống cho từng request.
- [EVIDENCE_LINK]: commit/b8... (Setup Langfuse tracing)

### Phan Văn Tấn
- [TASKS_COMPLETED]: Thiết lập SLO Latency/ErrorRate, viết Alert Rules trong config, soạn thảo Runbook chi tiết để xử lý sự cố.
- [EVIDENCE_LINK]: commit/92... (Add SLO & Alert configs)

### Lê Công Thành
- [TASKS_COMPLETED]: Thực hiện Load Test giả lập 5-20 user truy cập, thực hiện Inject Incident `rag_slow` để kiểm tra khả năng bắt lỗi của hệ thống.
- [EVIDENCE_LINK]: commit/f2... (Load scripts & Incident injection)

### Nguyễn Quế Sơn
- [TASKS_COMPLETED]: Xây dựng Dashboard 6 panels trên Grafana, thu thập Evidence cho báo cáo, thực hiện xuất Audit Logs để lấy điểm bonus.
- [EVIDENCE_LINK]: commit/e5... (Dashboard & Evidence doc)

### Lê Huy Hồng Nhật
- [TASKS_COMPLETED]: Quản trị Repo, điều phối task/branch, viết Blueprint report tổng thể, dẫn dắt Live Demo với Giảng viên.
- [EVIDENCE_LINK]: commit/d9... (Project management & final merge)

---

## 6. Bonus Items (Optional)
- [BONUS_COST_OPTIMIZATION]: Đã thêm logic tính toán Cost USD chi tiết cho từng Token Usage của LLM.
- [BONUS_AUDIT_LOGS]: Có file `data/audit.jsonl` tách riêng chứa các log quản trị thay đổi incident mode.
- [BONUS_CUSTOM_METRIC]: Thêm metric `quality_score_avg` để theo dõi chất lượng câu trả lời theo thời gian thực.
