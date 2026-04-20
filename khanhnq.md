# Hướng dẫn chi tiết cho Nguyễn Quốc Khánh (Member A — Logging & PII)

## Tổng quan vai trò

Bạn chịu trách nhiệm cho **3 trụ cột cốt lõi** của hệ thống Observability mà toàn bộ nhóm phụ thuộc vào:
1. **Correlation ID** — Gán mã định danh duy nhất cho mỗi request để truy vết xuyên suốt hệ thống.
2. **Log Enrichment** — Gắn ngữ cảnh nghiệp vụ (user, session, feature...) vào mọi dòng log.
3. **PII Scrubbing** — Đảm bảo thông tin nhạy cảm (email, SĐT, thẻ tín dụng) KHÔNG BAO GIỜ lọt ra file log.

> **Tại sao phần việc của bạn quan trọng nhất?** Vì script chấm điểm `validate_logs.py` kiểm tra chính xác 4 tiêu chí, trong đó **3 tiêu chí do bạn phụ trách** (schema, correlation ID, enrichment, PII). Nếu bạn không hoàn thành, nhóm mất tối đa **80/100 điểm validation**.

---

## TASK 1: Implement Correlation ID Middleware

### File: `app/middleware.py`

### Hiện trạng (Code gốc)
```python
class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # TODO: Clear contextvars to avoid leakage between requests
        # clear_contextvars()

        # TODO: Extract x-request-id from headers or generate a new one
        # Use format: req-<8-char-hex>
        correlation_id = "MISSING"
        
        # TODO: Bind the correlation_id to structlog contextvars
        # bind_contextvars(correlation_id=correlation_id)
        
        request.state.correlation_id = correlation_id
        
        start = time.perf_counter()
        response = await call_next(request)
        
        # TODO: Add the correlation_id and processing time to response headers
        # response.headers["x-request-id"] = correlation_id
        # response.headers["x-response-time-ms"] = ...
        
        return response
```

### Bạn cần làm gì (từng bước)

**Bước 1 — Clear context:** Mỗi request mới đều phải "xóa sạch" context của request cũ, không để dữ liệu bị rò rỉ chéo giữa các request:
```python
clear_contextvars()
```

**Bước 2 — Tạo hoặc lấy Correlation ID:**  
- Nếu client gửi kèm header `x-request-id` thì **dùng lại** giá trị đó (vì microservice upstream có thể đã gán).
- Nếu KHÔNG có, tự sinh ID mới theo format `req-<8 ký tự hex>`.
```python
correlation_id = request.headers.get(
    "x-request-id",
    f"req-{uuid.uuid4().hex[:8]}"
)
```

**Bước 3 — Bind vào structlog context:** Từ đây, BẤT KỲ dòng log nào được ghi trong suốt vòng đời request này đều tự động mang theo `correlation_id`:
```python
bind_contextvars(correlation_id=correlation_id)
```

**Bước 4 — Gắn vào Response Headers:** Trả `correlation_id` và thời gian xử lý về cho client, giúp frontend hoặc tester biết request nào tương ứng trace nào:
```python
response.headers["x-request-id"] = correlation_id
response.headers["x-response-time-ms"] = str(int((time.perf_counter() - start) * 1000))
```

### ⚠️ Lưu ý quan trọng

| # | Lưu ý | Giải thích |
|---|-------|-----------|
| 1 | `clear_contextvars()` **phải nằm đầu tiên** | Nếu không có bước này, request B có thể "thừa hưởng" user_id, session_id của request A trước đó (context leakage). Đây là bug rất khó debug trong production. |
| 2 | Format ID phải là `req-xxxxxxxx` | Script `validate_logs.py` kiểm tra `correlation_id != "MISSING"`. Tuy không bắt buộc prefix `req-`, nhưng format này giúp dễ dàng grep log và phân biệt ID do hệ thống tự sinh vs. ID client gửi lên. |
| 3 | Phải lấy `uuid.uuid4().hex[:8]` thay vì `str(uuid.uuid4())` | `.hex` cho ra chuỗi hex thuần tuý không có dấu `-`, lấy 8 ký tự đầu tiên cho gọn. |

---

## TASK 2: Enrich Logs với Request Context

### File: `app/main.py` — Hàm `chat()`

### Hiện trạng (Code gốc)
```python
@app.post("/chat", response_model=ChatResponse)
async def chat(request: Request, body: ChatRequest) -> ChatResponse:
    # TODO: Enrich logs with request context (user_id_hash, session_id, feature, model, env)
    # bind_contextvars(...)
```

### Bạn cần làm gì

Gọi `bind_contextvars()` để gắn các field nghiệp vụ vào structlog. Những field này sẽ tự động xuất hiện trong MỌI dòng log phát sinh trong scope của request đó:

```python
bind_contextvars(
    user_id_hash=hash_user_id(body.user_id),
    session_id=body.session_id,
    feature=body.feature,
    model=agent.model,
    env=os.getenv("APP_ENV", "dev"),
)
```

### ⚠️ Lưu ý quan trọng

| # | Lưu ý | Giải thích |
|---|-------|-----------|
| 1 | Dùng `hash_user_id()` — KHÔNG BAO GIỜ log `user_id` raw | Hàm `hash_user_id()` (đã có trong `pii.py`) dùng SHA-256 để băm, trả về 12 ký tự hex. Đây là yêu cầu bảo mật bắt buộc — nếu ghi thẳng `body.user_id` vào log, bạn sẽ bị trừ điểm PII. |
| 2 | Phải bind **trước** khi gọi `log.info("request_received", ...)` | Vì `bind_contextvars` ảnh hưởng đến MỌI log sau nó trong cùng request. Nếu bind sau, dòng `request_received` sẽ thiếu `user_id_hash`, `session_id`, v.v. |
| 3 | Tên field phải khớp chính xác với Schema | `logging_schema.json` và `validate_logs.py` yêu cầu đúng tên: `user_id_hash`, `session_id`, `feature`, `model`. Viết sai tên (VD: `userId` thay vì `user_id_hash`) sẽ bị trừ 20 điểm. |
| 4 | `import os` đã có sẵn ở đầu file | Không cần import thêm. `hash_user_id` cũng đã được import sẵn. |

### Đối chiếu với Schema (logging_schema.json)

Script `validate_logs.py` kiểm tra rằng mỗi log record có `service == "api"` phải chứa ĐẦY ĐỦ 4 field enrichment:
```python
ENRICHMENT_FIELDS = {"user_id_hash", "session_id", "feature", "model"}
```
Nếu thiếu bất kỳ field nào → `[FAILED] Log enrichment` → **-20 điểm**.

---

## TASK 3: Kích hoạt PII Scrubbing Processor

### File: `app/logging_config.py`

### Hiện trạng (Code gốc)
```python
structlog.configure(
    processors=[
        merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True, key="ts"),
        # TODO: Register your PII scrubbing processor here
        # scrub_event,
        ...
    ],
)
```

### Bạn cần làm gì

Bỏ comment dòng `scrub_event` để kích hoạt processor lọc PII:
```python
structlog.configure(
    processors=[
        merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True, key="ts"),
        scrub_event,       # <-- BỎ COMMENT DÒNG NÀY
        structlog.processors.StackInfoRenderer(),
        ...
    ],
)
```

### ⚠️ Lưu ý quan trọng

| # | Lưu ý | Giải thích |
|---|-------|-----------|
| 1 | `scrub_event` phải nằm **SAU** `TimeStamper` và **TRƯỚC** `JsonlFileProcessor` | Thứ tự pipeline processor là: tạo timestamp → lọc PII → ghi ra file. Nếu đặt SAU `JsonlFileProcessor`, PII sẽ đã bị ghi vào `logs.jsonl` trước khi bị lọc → fail. |
| 2 | Hàm `scrub_event` đã được viết sẵn — hiểu cách nó hoạt động | Nó quét 2 vị trí: (a) mọi value kiểu `str` trong dict `payload`, (b) field `event` nếu là string. Mỗi value được đưa qua `scrub_text()` trong `pii.py`. |

---

## TASK 4: Kiểm tra và bổ sung PII Patterns (Tuỳ chọn nâng cao)

### File: `app/pii.py`

### Hiện trạng (Code gốc)
```python
PII_PATTERNS: dict[str, str] = {
    "email": r"[\w\.-]+@[\w\.-]+\.\w+",
    "phone_vn": r"(?:\+84|0)[ \.-]?\d{3}[ \.-]?\d{3}[ \.-]?\d{3,4}",
    "cccd": r"\b\d{12}\b",
    "credit_card": r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b",
    # TODO: Add more patterns (e.g., Passport, Vietnamese address keywords)
}
```

### Giải thích từng Regex đã có

| Pattern | Regex | Match ví dụ | Thay bằng |
|---------|-------|-------------|-----------|
| `email` | `[\w\.-]+@[\w\.-]+\.\w+` | `student@vinuni.edu.vn` | `[REDACTED_EMAIL]` |
| `phone_vn` | `(?:\+84\|0)[ \.-]?\d{3}[ \.-]?\d{3}[ \.-]?\d{3,4}` | `0987654321`, `+84 987 654 321` | `[REDACTED_PHONE_VN]` |
| `cccd` | `\b\d{12}\b` | `012345678901` (số CCCD 12 chữ số) | `[REDACTED_CCCD]` |
| `credit_card` | `\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b` | `4111 1111 1111 1111`, `4111-1111-1111-1111` | `[REDACTED_CREDIT_CARD]` |

### Bạn có thể bổ sung thêm (điểm Bonus)
```python
# Ví dụ: Passport Việt Nam (1 chữ + 7 số)
"passport_vn": r"\b[A-Z]\d{7}\b",
```

### ⚠️ Lưu ý quan trọng

| # | Lưu ý | Giải thích |
|---|-------|-----------|
| 1 | Script chấm điểm kiểm tra PII bằng cách tìm ký tự `@` và chuỗi `4111` | Xem dòng 47-48 trong `validate_logs.py`: `if "@" in raw or "4111" in raw`. Bạn PHẢI đảm bảo mọi email (chứa `@`) và thẻ tín dụng test (`4111...`) đều bị redact **TRƯỚC KHI** ghi vào `logs.jsonl`. |
| 2 | Regex `cccd` có thể gây **false positive** | Pattern `\b\d{12}\b` sẽ match bất kỳ chuỗi 12 chữ số nào. Trong bài lab này không gây vấn đề, nhưng cần biết để giải thích với giảng viên khi bị hỏi. |
| 3 | Hàm `summarize_text()` đã gọi `scrub_text()` bên trong | Nghĩa là bất kỳ dòng nào dùng `summarize_text()` để tạo preview (ví dụ `message_preview`) đều đã tự động lọc PII. Đây là **defense-in-depth**: lọc 2 lần (1 lần qua `summarize_text`, 1 lần qua `scrub_event` processor). |

---

## TỔNG KẾT: Checklist các dòng code cần sửa

| # | File | Dòng | Hành động |
|---|------|------|-----------|
| 1 | `app/middleware.py:14` | `# clear_contextvars()` | Bỏ comment |
| 2 | `app/middleware.py:18` | `correlation_id = "MISSING"` | Thay bằng logic lấy từ header hoặc sinh mới |
| 3 | `app/middleware.py:21` | `# bind_contextvars(...)` | Bỏ comment |
| 4 | `app/middleware.py:29-30` | `# response.headers[...]` | Bỏ comment + tính thời gian xử lý |
| 5 | `app/main.py:47-48` | `# bind_contextvars(...)` | Thêm code bind 5 field enrichment |
| 6 | `app/logging_config.py:46` | `# scrub_event,` | Bỏ comment |
| 7 | `app/pii.py:11` | `# TODO: Add more patterns` | (Tuỳ chọn) Thêm regex mới |

**Tổng cộng: 6 thay đổi bắt buộc + 1 tuỳ chọn.**

---

## Kịch bản Test End-to-End

### Bước 1: Cài đặt môi trường
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### Bước 2: Xoá log cũ (nếu có) và khởi động app
```bash
rm -f data/logs.jsonl
uvicorn app.main:app --reload --port 8000
```

### Bước 3: Gửi request test chứa PII
Mở terminal mới, chạy:
```bash
# Request chứa email (phải bị redact)
curl -s -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id":"u01","session_id":"s01","feature":"qa","message":"My email is student@vinuni.edu.vn"}'

# Request chứa thẻ tín dụng (phải bị redact)
curl -s -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id":"u02","session_id":"s02","feature":"qa","message":"Card 4111 1111 1111 1111"}'

# Request chứa SĐT (phải bị redact)
curl -s -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id":"u03","session_id":"s03","feature":"summary","message":"Call me at 0987654321"}'

# Request bình thường, KHÔNG chứa PII
curl -s -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id":"u04","session_id":"s04","feature":"qa","message":"How do I debug tail latency?"}'

# Request với custom x-request-id (test khả năng giữ ID từ client)
curl -s -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -H "x-request-id: req-mycustom" \
  -d '{"user_id":"u05","session_id":"s05","feature":"qa","message":"What is monitoring?"}'
```

### Bước 4: Kiểm tra log bằng tay
```bash
# Xem 3 dòng log đầu tiên (format đẹp)
head -3 data/logs.jsonl | python -m json.tool
```

**Checklist kiểm tra thủ công** — mỗi dòng log phải thoả mãn:

- [ ] Có field `ts` (timestamp ISO format, VD: `2026-04-20T08:00:00Z`)
- [ ] Có field `level` (`info`, `warning`, `error`)
- [ ] Có field `event` (`request_received`, `response_sent`, ...)
- [ ] Có field `correlation_id` ≠ `"MISSING"` (VD: `req-a1b2c3d4`)
- [ ] Có field `service` = `"api"`
- [ ] Có field `user_id_hash` (12 ký tự hex, VD: `"e3b0c44298fc"`)
- [ ] Có field `session_id` (VD: `"s01"`)
- [ ] Có field `feature` (VD: `"qa"`)
- [ ] Có field `model` (VD: `"claude-sonnet-4-5"`)
- [ ] **KHÔNG** chứa ký tự `@` ở bất kỳ đâu
- [ ] **KHÔNG** chứa chuỗi `4111` ở bất kỳ đâu
- [ ] **KHÔNG** chứa chuỗi `0987654321` (raw phone)
- [ ] Nếu có PII, đã bị thay bằng `[REDACTED_EMAIL]`, `[REDACTED_PHONE_VN]`, `[REDACTED_CREDIT_CARD]`

### Bước 5: Chạy script chấm điểm tự động
```bash
python scripts/validate_logs.py
```

**Output mong đợi khi đạt 100/100:**
```
--- Lab Verification Results ---
Total log records analyzed: XX
Records with missing required fields: 0
Records with missing enrichment (context): 0
Unique correlation IDs found: X (>= 2)
Potential PII leaks detected: 0

--- Grading Scorecard (Estimates) ---
+ [PASSED] Basic JSON schema
+ [PASSED] Correlation ID propagation
+ [PASSED] Log enrichment
+ [PASSED] PII scrubbing

Estimated Score: 100/100
```

### Bước 6: Kiểm tra Response Header
```bash
curl -s -D - -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id":"u01","session_id":"s01","feature":"qa","message":"test"}' \
  -o /dev/null
```

**Kiểm tra output có chứa:**
```
x-request-id: req-xxxxxxxx
x-response-time-ms: <số ms>
```

---

## Các câu hỏi giảng viên có thể hỏi bạn (Chuẩn bị trả lời)

### Q1: "Tại sao phải `clear_contextvars()` ở đầu mỗi request?"
> **A:** Vì structlog dùng `contextvars` (biến gắn liền với thread/coroutine). Trong môi trường async, nếu không clear, context của request cũ có thể bị "rò rỉ" sang request mới chạy trên cùng coroutine, dẫn đến log ghi sai `user_id` hoặc `session_id`.

### Q2: "Regex email `[\w\.-]+@[\w\.-]+\.\w+` có nhược điểm gì?"
> **A:** Pattern này đơn giản, có thể match các string không phải email hợp lệ (ví dụ `a@b.c`). Tuy nhiên, trong ngữ cảnh PII scrubbing, **over-matching (false positive) tốt hơn under-matching** — ta ưu tiên che hết còn hơn để lọt. Trong production dùng RFC 5322 pattern sẽ chính xác hơn nhưng phức tạp hơn nhiều.

### Q3: "Giải thích flow dữ liệu từ lúc user gửi request đến lúc log ghi xuống file?"
> **A:**
> 1. Request đến → `CorrelationIdMiddleware.dispatch()` chạy → clear context → sinh/lấy correlation_id → bind vào contextvars.
> 2. Vào hàm `chat()` → bind thêm user_id_hash, session_id, feature, model, env.
> 3. Gọi `log.info("request_received", ...)` → structlog pipeline chạy:
>    - `merge_contextvars` → nhập tất cả biến đã bind vào event_dict
>    - `add_log_level` → thêm field `level`
>    - `TimeStamper` → thêm field `ts`
>    - **`scrub_event`** → quét `payload` và `event`, thay PII bằng `[REDACTED_*]`
>    - `JsonlFileProcessor` → ghi 1 dòng JSON vào `data/logs.jsonl`
>    - `JSONRenderer` → in ra console

### Q4: "Tại sao hash user_id thay vì mã hoá hai chiều (encrypt)?"
> **A:** Hash một chiều (SHA-256) đảm bảo không thể khôi phục `user_id` gốc từ log. Mục đích là để truy vết request theo user mà không lộ danh tính. Encrypt hai chiều vẫn có rủi ro nếu key bị lộ. Trong Observability, ta chỉ cần **group** log theo user chứ không cần biết user thật là ai.
