# Day 13 Observability Lab Report

> **Instruction**: Fill in all sections below. This report is designed to be parsed by an automated grading assistant. Ensure all tags (e.g., `[GROUP_NAME]`) are preserved.

## 1. Team Metadata
- [GROUP_NAME]: C401-D6
- [REPO_URL]: https://github.com/LeHuyHongNhat/Lab13-Observability
- [MEMBERS]:
  - Member A: Nguyễn Quốc Khánh (khanhnq) | Role: Logging & PII Scrubbing
  - Member B: Nguyễn Tuấn Khải (Khaidz) | Role: Tracing & Tags
  - Member C: Phan Văn Tấn (tan) | Role: SLO & Alerts
  - Member D: Lê Công Thành (thanh) | Role: Load Test & Incident Debugging
  - Member E: Nguyễn Quế Sơn (sonnq) | Role: Dashboard & Evidence Collection
  - Member F: Lê Huy Hồng Nhật (nhat) | Role: Blueprint & Demo Lead

---

## 2. Group Performance (Auto-Verified)
- [VALIDATE_LOGS_FINAL_SCORE]: 100/100
- [TOTAL_TRACES_COUNT]: 10+
- [PII_LEAKS_FOUND]: 0

---

## 3. Technical Evidence (Group)

### 3.1 Logging & Tracing
- [EVIDENCE_CORRELATION_ID_SCREENSHOT]: evidence/06_log_samples.png
- [EVIDENCE_PII_REDACTION_SCREENSHOT]: evidence/04_pii_scrubbing_logs.png
- [EVIDENCE_TRACE_WATERFALL_SCREENSHOT]: evidence/08_trace_waterfall.png
- [TRACE_WATERFALL_EXPLANATION]: The `run` span in the agent shows the full lifecycle of a chat request: RAG document retrieval, LLM prompt construction, fake generation, and quality scoring. The `@observe()` decorator from Langfuse captures input/output, token usage, and latency automatically.

### 3.2 Dashboard & SLOs
- [DASHBOARD_6_PANELS_SCREENSHOT]: evidence/01_grafana_dashboard.png
- [SLO_TABLE]:
| SLI | Target | Window | Current Value |
|---|---:|---|---:|
| Latency P95 | < 3000ms | 28d | ~800ms |
| Error Rate | < 2% | 28d | 0% (normal) |
| Cost Budget | < $2.5/day | 1d | $0.02 |

### 3.3 Alerts & Runbook
- [ALERT_RULES_SCREENSHOT]: evidence/03_prometheus_alerts_list.png
- [SAMPLE_RUNBOOK_LINK]: docs/alerts.md#2-high-error-rate

---

## 4. Incident Response (Group)
- [SCENARIO_NAME]: tool_fail
- [SYMPTOMS_OBSERVED]: All requests returned HTTP 500 (RuntimeError). Error rate spiked to 100%. Alert `HighErrorRate` fired within 1 minute.
- [ROOT_CAUSE_PROVED_BY]: Log lines with `error_type: RuntimeError` and correlation_id tracing showed the incident toggle `tool_fail` was enabled.
- [FIX_ACTION]: Disabled the incident toggle via `python scripts/inject_incident.py --scenario tool_fail --disable`
- [PREVENTIVE_MEASURE]: Added circuit breaker pattern and fallback model routing. Alert rules now trigger before SLO breach.

---

## 5. Individual Contributions & Evidence

### Khánh (Member A)
- [TASKS_COMPLETED]: Structured logging with structlog, PII scrubbing (email, phone, credit card, CCCD, passport), JSONL file output, context enrichment (user_id_hash, session_id, feature, model, env)
- [EVIDENCE_LINK]: Branch `origin/khanhnq` merged into `sonnq`

### Khải (Member B)
- [TASKS_COMPLETED]: Langfuse tracing integration with `@observe()` decorator, trace enrichment with user_id, session_id, tags, token usage tracking
- [EVIDENCE_LINK]: Branch `origin/Khaidz` merged into `sonnq` (plus `app/tracing.py`, `app/agent.py`)

### Tấn (Member C)
- [TASKS_COMPLETED]: Alert rules definition (8 rules in config/alert_rules.yaml), SLO specification (config/slo.yaml), Runbook documentation (docs/alerts.md), Address PII pattern
- [EVIDENCE_LINK]: Branch `origin/tan` merged into `sonnq`

### Thành (Member D)
- [TASKS_COMPLETED]: Load test script (scripts/load_test.py), Incident injection script (scripts/inject_incident.py), Log validation script (scripts/validate_logs.py)
- [EVIDENCE_LINK]: Branch `origin/thanh` merged into `sonnq`

### Nguyễn Quế Sơn (Member E)
- [TASKS_COMPLETED]: Grafana dashboard with 6 panels (Latency, Traffic, Error Rate, Cost, Tokens, Quality), Prometheus metrics integration, Docker Compose orchestration, Evidence collection and final report
- [EVIDENCE_LINK]: config/grafana_dashboard.json, evidence/ directory

### Lê Huy Hồng Nhật (Member F)
- [TASKS_COMPLETED]: Project management, Blueprint documentation lead, Demo scenario preparation, Root Cause Analysis (RCA) reporting
- [EVIDENCE_LINK]: docs/blueprint-template.md, docs/grading-evidence.md

---

## 6. Bonus Items (Optional)
- [BONUS_COST_OPTIMIZATION]: Cost tracking via `request_cost_usd_total` Prometheus counter with threshold alert at $2.5
- [BONUS_AUDIT_LOGS]: JSONL audit logging to `data/audit.jsonl` via `JsonlFileProcessor`
- [BONUS_CUSTOM_METRIC]: `pii_scrub_total` counter tracks number of PII elements redacted in real-time
