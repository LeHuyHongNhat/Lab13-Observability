# Mock Debug Q&A (Oral/Written Debugging Questions)

Đây là tài liệu tập hợp các câu hỏi phỏng vấn hoặc tình huống gỡ lỗi (debugging) để chuẩn bị cho buổi bảo vệ Lab 13.

## 1. Truy vết phân tán (Distributed Tracing)

**Q: Làm thế nào bạn xác định được đoạn code nào đang làm chậm toàn bộ quy trình RAG?**
*   **A**: Bằng cách sử dụng **Langfuse**, nhóm theo dõi luồng Waterfall của Trace ID. Khi có sự cố `rag_slow`, span tương ứng với bước truy xuất (`retrieve`) sẽ có thanh đo độ dài bất thường (ví dụ: mất tới 2.5s thay vì 100ms). Nhờ vậy, thay vì đoán mò, nhóm biết chính xác hàm nào đang gây ra độ trễ.

**Q: Khi xảy ra lỗi 500 ở Client, bạn làm sao để tìm ra nguyên nhân tận gốc ở Backend?**
*   **A**: Tại Client, nhóm trích xuất `x-request-id` (Correlation ID) từ Response Header. Trong hệ thống Log (Grafana Loki), nhóm dùng Correlation ID này để filter. Nó sẽ hiển thị toàn bộ vòng đời của request: từ lúc nhận, thực thi LLM, cho đến dòng báo lỗi Exception cụ thể cùng Stack Trace liên quan.

## 2. Bảo mật PII & Dữ liệu nhạy cảm

**Q: Có rủi ro nào khi lọc PII bằng Regex truyền thống không? Và bạn giải quyết thế nào?**
*   **A**: Regex truyền thống thường chỉ "cào" trên bề mặt chuỗi văn bản (flat string) và sẽ dễ dàng bỏ qua các cụm PII nằm sâu bên trong JSON lồng nhau (Nested JSON). Để khắc phục, nhóm thiết kế thuật toán `scrub_recursive` kết hợp với Regex để bóc tách và làm sạch mọi tầng sâu của dict/list, đảm bảo an toàn tuyệt đối.

**Q: Làm sao bạn phân biệt được một Exception bình thường với việc vượt ngưỡng Budget (Cost Limit)?**
*   **A**: Trong file `agent.py`, nhóm lập cơ chế kiểm tra (Guardrails) ngay sau khi nhận được thông số Token Usage từ LLM (mock_llm). Hàm `_estimate_cost` sẽ tính toán tiền tệ; nếu vượt quá giới hạn thiết lập (`MAX_REQUEST_COST = 0.01`), hệ thống ném ra `ValueError("Request cost exceeds limit")` đi kèm `error_type=ValueError`. Ta có thể thấy biểu đồ phân loại Error trên Grafana chỉ rõ các lỗi này.

## 3. Hệ thống Cảnh báo (Alerting & Metrics)

**Q: Tại sao phải sử dụng Percentile (P95, P99) thay vì Average (Trung bình) cho Latency?**
*   **A**: Trung bình dễ bị đánh lừa bởi một lượng lớn các request cực nhanh. Một vài request cực chậm (có thể gây ra trải nghiệm tệ cho nhóm KH VIP) sẽ bị "hòa tan" trong Average. Bằng cách dùng P95 hoặc P99, nhóm tự động bắt được những độ trễ "đột biến" (đuôi dài) để tạo ra các cảnh báo (Alert) chính xác nhất qua Prometheus.

**Q: Giả sử đêm nay đồ thị Error Rate tự nhiên tăng vọt lên 5%. Nhóm bạn sẽ phản ứng như thế nào?**
*   **A**: 
    1. Đầu tiên, nhóm nhận được cảnh báo qua Alertmanager.
    2. Nhóm mở Grafana Dashboard, nhìn vào biểu đồ quạt *"Error Breakdown by Type"* để xem lỗi thuộc nhóm nào (Network, Auth, hay LLM RateLimit). 
    3. Nhóm quay lại Tab Explore, lấy khoảng thời gian bị lỗi và lọc log bằng `error_type` để đọc chính xác thông điệp lỗi. 
    4. Cuối cùng, nhóm áp dụng Playbook tương ứng từ `docs/alerts.md` để giải quyết.
