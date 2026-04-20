from __future__ import annotations

import hashlib
import re

PII_PATTERNS: dict[str, str] = {
    # ── Định danh cá nhân ──────────────────────────────────────────────────────
    "email": r"[\w\.-]+@[\w\.-]+\.\w+",
    "phone_vn": r"(?:\+84|0)[ \.-]?\d{3}[ \.-]?\d{3}[ \.-]?\d{3,4}",           # 090 123 4567, +84.987.654.321
    "cccd": r"\b\d{12}\b",                                                         # Căn cước công dân 12 số
    "passport_vn": r"\b[A-Z]\d{7}\b",                                             # Hộ chiếu: B1234567
    "dob": r"\b(?:0?[1-9]|[12]\d|3[01])[\/\-\.](?:0?[1-9]|1[0-2])[\/\-\.](?:19|20)\d{2}\b",  # DD/MM/YYYY, DD-MM-YYYY
    "license_plate_vn": r"\b\d{2}[A-Z]\d?[-\s]?\d{4,5}\b",                      # 51G-12345, 30A 12345
    "address_vn": r"(?i)\b(?:số nhà|số|ngõ|ngách|hẻm|đường|phố|phường|xã|quận|huyện|thành phố|tỉnh)\s+[\w\s,/\-]+",

    # ── Tài chính ──────────────────────────────────────────────────────────────
    "credit_card": r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b",                 # 4111 1111 1111 1111
    "tax_code_vn": r"\b\d{10}(?:-\d{3})?\b",                                      # Mã số thuế: 10 số hoặc 10-3 số

    # ── Credential / Secret ────────────────────────────────────────────────────
    "api_key_generic": r"\b(?:sk|pk|api|key|token|secret)[-_][A-Za-z0-9_\-]{16,}\b",  # sk-xxxx, api_xxxxxx
    "jwt_token": r"eyJ[A-Za-z0-9_\-]+\.eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+",         # JWT 3 phần
    "url_with_creds": r"https?://[^:@\s]+:[^@\s]+@[^\s]+",                            # https://user:pass@host
    "ssh_private_key": r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",           # Fragment SSH private key
    "kv_password": r"(?i)(?:password|passwd|pwd|secret|api_?key)\s*[=:]\s*\S+",       # password=abc123, secret: xyz

    # ── Network / Infrastructure ───────────────────────────────────────────────
    "ipv4_private": r"\b(?:10|172\.(?:1[6-9]|2\d|3[01])|192\.168)\.\d{1,3}\.\d{1,3}\b",  # IP RFC-1918
}


def scrub_text(text: str) -> str:
    from .metrics import P_PII_SCRUB
    safe = text
    for name, pattern in PII_PATTERNS.items():
        matches = re.findall(pattern, safe)
        if matches:
            P_PII_SCRUB.inc(len(matches))
        safe = re.sub(pattern, f"[REDACTED_{name.upper()}]", safe)
    return safe


def summarize_text(text: str, max_len: int = 80) -> str:
    safe = scrub_text(text).strip().replace("\n", " ")
    return safe[:max_len] + ("..." if len(safe) > max_len else "")


def hash_user_id(user_id: str) -> str:
    return hashlib.sha256(user_id.encode("utf-8")).hexdigest()[:12]
