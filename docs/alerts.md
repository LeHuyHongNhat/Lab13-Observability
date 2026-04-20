# Alert Rules and Runbooks

## 1. High latency P95
- Severity: P2
- Trigger: `latency_p95_ms > 5000 for 30m`
- Impact: tail latency breaches SLO
- First checks:
  1. Open top slow traces in the last 1h
  2. Compare RAG span vs LLM span
  3. Check if incident toggle `rag_slow` is enabled
- Mitigation:
  - truncate long queries
  - fallback retrieval source
  - lower prompt size

## 2. High error rate
- Severity: P1
- Trigger: `error_rate_pct > 5 for 5m`
- Impact: users receive failed responses
- First checks:
  1. Group logs by `error_type`
  2. Inspect failed traces
  3. Determine whether failures are LLM, tool, or schema related
- Mitigation:
  - rollback latest change
  - disable failing tool
  - retry with fallback model

## 3. Cost budget spike
- Severity: P2
- Trigger: `hourly_cost_usd > 2x_baseline for 15m`
- Impact: burn rate exceeds budget
- First checks:
  1. Split traces by feature and model
  2. Compare tokens_in/tokens_out
  3. Check if `cost_spike` incident was enabled
- Mitigation:
  - shorten prompts
  - route easy requests to cheaper model
  - apply prompt cache

## 4. Sudden traffic drop
- Severity: P1
- Trigger: `request_rate_rps < 0.5x_baseline for 10m`
- Impact: users cannot access the system, or routing is broken
- First checks:
  1. Check ingress controller / API Gateway metrics for connection drops
  2. Check DNS routing configuration and health checks
  3. Verify if upstream dependencies or load balancers are down
- Mitigation:
  - Fix DNS records
  - Restart ingress controllers / API Gateway
  - Rollback recent infrastructure changes

## 5. PII redaction spike
- Severity: P2
- Trigger: `pii_scrub_count > 50 for 15m`
- Impact: potential data exfiltration or malicious probing
- First checks:
  1. Filter logs for `[REDACTED_` to see the nature of the data (e.g., credit cards, passports)
  2. Check if the spike comes from a single IP or user ID
  3. Verify if this is a legitimate new use case or an attack
- Mitigation:
  - Temporarily block the offending IP/user
  - Alert the security team for deeper audit
  - Add stricter input validation rules

## 6. Context window limit
- Severity: P3
- Trigger: `tokens_in_per_request > 100000 for 10m`
- Impact: LLM API may reject requests with 400 Bad Request (context length exceeded)
- First checks:
  1. Check traces on Langfuse to see which feature/user is sending massive prompts
  2. Review the document retrieval (RAG) span to see if too many docs are injected
- Mitigation:
  - Trim chat history length
  - Reduce the number of chunks returned by the RAG system
  - Route heavy requests to a model with a larger context window

## 7. Schema validation spike
- Severity: P2
- Trigger: `http_status_422_rate > 5 for 10m`
- Impact: clients are failing to communicate with the API
- First checks:
  1. Filter logs for `status_code=422` or `error_type=ValidationError` to identify the failing fields
  2. Check with Frontend/Mobile teams for recent releases that might have broken the payload structure
  3. Look for abnormal traffic patterns indicating a fuzzer or bot
- Mitigation:
  - If a bad client release: request immediate rollback from the client team
  - If malicious: block the offending IP addresses
 
 ## 8. High LLM token usage
- Severity: P2
- Trigger: `total_tokens_out_per_hour > 200000 for 1h`
- Impact: potential cost overruns due to unexpectedly verbose model outputs
- First checks:
  1. Check which features or user segments are generating the most tokens
  2. Review the RAG retrieval depth and number of documents processed
  3. Verify if there are long conversations or complex queries being processed
- Mitigation:
  - Reduce the verbosity of the AI's responses through prompt engineering
  - Implement token limits per request
  - Use summary or compression techniques for long conversations
  - Optimize the RAG system to return fewer, more relevant documents
