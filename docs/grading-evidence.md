# Evidence Collection Sheet

## Required screenshots

| # | Evidence | File | Status |
|---|---------|------|--------|
| 1 | Langfuse trace list >= 10 traces | `evidence/07_langfuse_trace_list.png` | ⏳ Pending |
| 2 | One full trace waterfall | `evidence/08_trace_waterfall.png` | ⏳ Pending |
| 3 | JSON logs showing correlation_id | `evidence/06_log_samples.png` | ✅ Done |
| 4 | Log line with PII redaction | `evidence/04_pii_scrubbing_logs.png` | ✅ Done |
| 5 | Dashboard with 6 panels | `evidence/01_grafana_dashboard.png` | ✅ Done |
| 6 | Alert rules with runbook link | `evidence/03_prometheus_alerts_list.png` | ✅ Done |

## Optional screenshots

| # | Evidence | File | Status |
|---|---------|------|--------|
| 7 | Incident before/after fix | `evidence/02_alert_firing.png` | ✅ Done |
| 8 | PII patterns integrated | `evidence/05_pii_patterns_integrated.png` | ✅ Done |

## Validation Results

```
--- Lab Verification Results ---
Total log records analyzed: 116
Records with missing required fields: 0
Records with missing enrichment (context): 0
Unique correlation IDs found: 59
Potential PII leaks detected: 0

Estimated Score: 100/100
```

## Evidence Directory Layout

```
evidence/
├── 01_grafana_dashboard.png        # 6-panel dashboard screenshot
├── 02_alert_firing.png             # HighErrorRate alert in FIRING state
├── 03_prometheus_alerts_list.png   # All Prometheus alert rules
├── 04_pii_scrubbing_logs.png       # Log showing [REDACTED_CREDIT_CARD] etc.
├── 05_pii_patterns_integrated.png  # All PII regex patterns
├── 06_log_samples.png              # JSONL logs with correlation_id
├── 07_langfuse_trace_list.png      # (Pending) >= 10 traces on Langfuse Cloud
└── 08_trace_waterfall.png          # (Pending) Single trace waterfall view
```
