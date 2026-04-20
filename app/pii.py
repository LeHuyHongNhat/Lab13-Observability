from __future__ import annotations

import hashlib
import re

PII_PATTERNS: dict[str, str] = {
    # ── Định danh cá nhân ──────────────────────────────────────────────────────
    "email": r"(?i)[\w\+\.-]+(?:@|\[at\]|\(at\)|\[ at \])[\w\.-]+(?:\.|\(dot\)|\[dot\])\w+",
    "phone_vn": r"(?:\+?84|0|\(0\d{2,3}\))[ \.-]?\d{2,4}[ \.-]?\d{3}[ \.-]?\d{3,4}",
    "cccd": r"\b\d{9}(?:\d{3})?\b",                                                # CMND 9 số hoặc CCCD 12 số
    "passport_vn": r"(?i)\b[A-Z]\d{7}\b",                                         # Hộ chiếu: B1234567, b1234567
    "address_vn": r"(?i)\b(?:số nhà|số|ngõ|ngách|hẻm|đường|phố|phường|xã|quận|huyện|thành phố|tỉnh)\s+[\w\s,/\-]+",
    "student_id": r"(?i)\b(?:19|20|21|22|23|24|25)[a-z]{2,4}\d{4}\b",             # Mã SV: 21CE0001, 23CS0123
    "dob": r"\b(?:(?:0?[1-9]|[12]\d|3[01])[\/\-\.](?:0?[1-9]|1[0-2])[\/\-\.](?:19|20)\d{2}|(?:19|20)\d{2}[\/\-\.](?:0?[1-9]|1[0-2])[\/\-\.](?:0?[1-9]|[12]\d|3[01]))\b",
    "license_plate_vn": r"(?i)\b\d{2}[A-Z]\d?[\-\s\.]?\d{4,5}\b",                 # 51G-123.45


    # ── Tài chính ──────────────────────────────────────────────────────────────
    "tax_code_vn": r"\b\d{10}(?:-\d{3})?\b",                                      # Mã số thuế: 10 số hoặc 10-3 số
    "credit_card": r"(?<!\d)(?:\d[ -]*?){13,19}(?!\d)",                           # Hỗ trợ 13-19 số, dời xuống sau tax_code để ưu tiên

    # ── Credential / Secret ────────────────────────────────────────────────────
    "api_key_generic": r"(?i)\b(?:sk|pk|api|key|token|secret)[-_][a-z0-9_\-]{16,}\b|\bAKIA[0-9A-Z]{16}\b",
    "jwt_token": r"eyJ[A-Za-z0-9_\-]+\.eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+",         # JWT 3 phần
    "url_with_creds": r"(?i)[a-z0-9\.\-\+]+://[^:@\s]+:[^@\s]+@[^\s]+",              # mongodb://, postgresql://, https://
    "ssh_private_key": r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",           # Fragment SSH private key
    "kv_password": r"(?i)(?:password|passwd|pwd|secret|api_?key|pin(?:\s+code)?|passcode)(?:\s+is\s+|\s*[=:]\s*)\S+",
    "otp_code": r"(?i)\b(?:otp|2fa|code|mã\s?otp|mã\s?xác\s?nhận)(?:\s+is\s+|\s*[:=]\s*|\s+)\b\d{4,8}\b",

    # ── Network / Infrastructure ───────────────────────────────────────────────
    "mac_address": r"(?i)\b(?:[0-9a-f]{2}[:-]){5}[0-9a-f]{2}\b",                  # Địa chỉ MAC Address
    "ipv4_private": r"\b(?:10|172\.(?:1[6-9]|2\d|3[01])|192\.168)\.\d{1,3}\.\d{1,3}\b",  # IP RFC-1918
    "ipv6_private": r"(?i)\b(?:fe80|fc[0-9a-f]{2}|fd[0-9a-f]{2}):[0-9a-f:]+\b",

    # ── Fallback Catch-All cho dải số học (Tài khoản ngân hàng / PIN dài) ───
    "bank_account_or_id": r"\b\d{6,}\b",                                          # Dãy từ 6 số trở lên (STK ngân hàng, mã số lạ...)

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
