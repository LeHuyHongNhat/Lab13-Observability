from __future__ import annotations

from collections import Counter as PyCounter
from statistics import mean
from prometheus_client import Counter, Histogram, Gauge, Summary

# Original state for snapshot() compatibility
REQUEST_LATENCIES: list[int] = []
REQUEST_COSTS: list[float] = []
REQUEST_TOKENS_IN: list[int] = []
REQUEST_TOKENS_OUT: list[int] = []
ERRORS: PyCounter[str] = PyCounter()
TRAFFIC: int = 0
QUALITY_SCORES: list[float] = []

# Prometheus Metrics
P_TRAFFIC = Counter('request_total', 'Total number of requests')
P_LATENCY = Histogram('request_latency_ms', 'Request latency in ms', buckets=[100, 500, 1000, 2000, 3000, 5000, 10000])
P_COST = Counter('request_cost_usd_total', 'Total cost in USD')
P_TOKENS_IN = Counter('request_tokens_in_total', 'Total tokens in')
P_TOKENS_OUT = Counter('request_tokens_out_total', 'Total tokens out')
P_ERRORS = Counter('request_errors_total', 'Total number of errors', ['error_type'])
P_QUALITY = Summary('request_quality_score', 'Summary of quality scores')


def record_request(latency_ms: int, cost_usd: float, tokens_in: int, tokens_out: int, quality_score: float) -> None:
    global TRAFFIC
    TRAFFIC += 1
    REQUEST_LATENCIES.append(latency_ms)
    REQUEST_COSTS.append(cost_usd)
    REQUEST_TOKENS_IN.append(tokens_in)
    REQUEST_TOKENS_OUT.append(tokens_out)
    QUALITY_SCORES.append(quality_score)
    
    # Update Prometheus metrics
    P_TRAFFIC.inc()
    P_LATENCY.observe(latency_ms)
    P_COST.inc(cost_usd)
    P_TOKENS_IN.inc(tokens_in)
    P_TOKENS_OUT.inc(tokens_out)
    P_QUALITY.observe(quality_score)


def record_error(error_type: str) -> None:
    ERRORS[error_type] += 1
    # Update Prometheus metrics
    P_ERRORS.labels(error_type=error_type).inc()



def percentile(values: list[int], p: int) -> float:
    if not values:
        return 0.0
    items = sorted(values)
    idx = max(0, min(len(items) - 1, round((p / 100) * len(items) + 0.5) - 1))
    return float(items[idx])



def snapshot() -> dict:
    return {
        "traffic": TRAFFIC,
        "latency_p50": percentile(REQUEST_LATENCIES, 50),
        "latency_p95": percentile(REQUEST_LATENCIES, 95),
        "latency_p99": percentile(REQUEST_LATENCIES, 99),
        "avg_cost_usd": round(mean(REQUEST_COSTS), 4) if REQUEST_COSTS else 0.0,
        "total_cost_usd": round(sum(REQUEST_COSTS), 4),
        "tokens_in_total": sum(REQUEST_TOKENS_IN),
        "tokens_out_total": sum(REQUEST_TOKENS_OUT),
        "error_breakdown": dict(ERRORS),
        "quality_avg": round(mean(QUALITY_SCORES), 4) if QUALITY_SCORES else 0.0,
    }
