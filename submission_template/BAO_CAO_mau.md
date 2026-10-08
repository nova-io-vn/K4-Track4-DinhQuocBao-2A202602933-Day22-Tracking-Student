# Báo cáo lab: chọn tracker cho 5 video

**Hình thức:** Cá nhân &nbsp;&nbsp; **Họ và tên:** Đinh Quốc Bảo &nbsp;&nbsp; **MSSV:** 2A202602933

Detector cố định: `yolo26n.pt`, ảnh 640 px, Re-ID `osnet_x0_25_msmt17.pt`. Các thành phần cố định này không bị thay đổi trong các lượt chạy.

## 1. Cấu hình đã chọn

| Video | Tracker | conf | iou | Quan sát khi xem video | Đã thử nhưng loại |
|---|---|---:|---:|---|---|
| video_1 (quảng trường, tĩnh, ban ngày) | BoT-SORT | 0.15 | 0.5 | Bám được cả người gần lẫn người nhỏ ở xa; Re-ID hữu ích khi nhiều người cắt qua nhau. Cấu hình này đạt cả ba metric cao nhất trong các lượt đã chấm. | ByteTrack, `conf=0.30`, `iou=0.5`: HOTA và IDF1 thấp hơn; `conf=0.30` cũng bỏ sót thêm người nhỏ. |
| video_2 (phố đêm, tĩnh, rất đông) | BoT-SORT | 0.15 | 0.5 | Ngưỡng thấp giữ thêm nhiều người nhỏ và tối ở xa; các hộp vẫn tập trung vào người trong cảnh đông. | ByteTrack, `conf=0.30`, `iou=0.5`, 150 frame: bỏ sót rõ hơn các người nhỏ ở vùng xa và vùng thiếu sáng. |
| video_3 (camera di động, ảnh nhỏ) | BoT-SORT | 0.15 | 0.5 | Phát hiện được người rất gần, người ở giữa ảnh và một số người nhỏ phía xa dù ảnh chỉ 640×480 và bị nhòe do chuyển động. | ByteTrack, `conf=0.30`, `iou=0.5`, 150 frame: ít hộp hơn ở người nhỏ/xa; chỉ dựa nhiều vào chuyển động nên kém phù hợp khi camera di chuyển. |
| video_4 (trong nhà, camera di chuyển) | BoT-SORT | 0.30 | 0.5 | Giữ ngưỡng cao hơn để hạn chế hộp giả từ kính và phản chiếu; hộp bám tốt các người chính khi camera tiến lên. | ByteTrack, `conf=0.30`, `iou=0.5`, 150 frame: theo được người lớn nhưng ít lợi thế hơn khi người che nhau hoặc kích thước thay đổi theo camera. |
| video_5 (trên xe bus, giao lộ đông) | BoT-SORT | 0.15 | 0.5 | Ngưỡng thấp bắt thêm người nhỏ hai bên đường; Re-ID hỗ trợ khi toàn cảnh dịch chuyển và rung theo xe. | ByteTrack, `conf=0.30`, `iou=0.5`, 150 frame: bỏ sót nhiều người nhỏ và tối ở lề đường hơn cấu hình đã chọn. |

Tất cả file nộp được chạy toàn bộ frame: video_1 đến video_5 lần lượt có 600, 1050, 837, 900 và 750 frame.

## 2. Số liệu video_1

Kết quả TrackEval của cấu hình nộp BoT-SORT, `conf=0.15`, `iou=0.5`:

```text
Metric   HOTA     MOTA     IDF1
video_1  29.343   20.731   29.561
```

Một số số liệu bổ sung: DetA 19.236, AssA 45.113, IDSW 27, CLR_TP 4384, CLR_FN 14197 và CLR_FP 505. Các video_2 đến video_5 không có nhãn trong gói lab nên không điền metric cho chúng.

## 3. Phân tích

### Video 1

BoT-SORT `conf=0.15` đạt HOTA 29.343, MOTA 20.731 và IDF1 29.561, cao hơn BoT-SORT `conf=0.25` (29.096 / 20.139 / 28.644) và hai cấu hình ByteTrack đã chấm. Việc hạ `conf` tăng recall và số true positive, đổi lại có thêm false positive, nhưng tổng thể cả ba metric vẫn tăng. Cảnh có camera tĩnh nhưng nhiều người giao nhau nên đặc trưng ngoại hình giúp duy trì liên kết tốt hơn chỉ dùng chuyển động. Sai số lớn còn lại chủ yếu đến từ detector bỏ sót người nhỏ/che khuất, thể hiện ở số false negative cao.

### Video 2

Cảnh đêm có nhiều người nhỏ và tập trung thành nhóm, vì vậy ByteTrack `conf=0.30` bỏ sót khá nhiều người ở xa. BoT-SORT `conf=0.15` tạo thêm hộp đúng tại các vùng này trong preview. Khi các quỹ đạo đi gần nhau, Re-ID cung cấp thêm thông tin ngoại hình để giảm nguy cơ hộp nhảy sang người bên cạnh. Đổi lại, ngưỡng thấp có thể tạo thêm một số track ngắn nên cần quan sát các vùng biển sáng và vật thể nền.

### Video 3

Camera di chuyển và ảnh có độ phân giải thấp khiến giả định chuyển động nền ổn định không còn đúng. Trong baseline 150 frame, ByteTrack bắt được các người lớn nhưng dễ mất người nhỏ hoặc bị nhòe. BoT-SORT kết hợp chuyển động với ngoại hình nên phù hợp hơn khi toàn bộ khung hình thay đổi. `conf=0.15` được giữ để giảm bỏ sót, dù một số người rất xa vẫn chưa có hộp.

### Video 4 và video 5

Ở video_4, kính và phản chiếu có thể giống người nên dùng `conf=0.30` để ưu tiên hộp chắc chắn; BoT-SORT vẫn bám tốt những người chính khi khoảng cách tới camera thay đổi nhanh. Ở video_5, người thường nhỏ và nằm hai bên đường trong khi camera rung theo xe, nên dùng `conf=0.15` để tăng khả năng phát hiện. Preview cho thấy cấu hình BoT-SORT bắt được nhiều người nhỏ hơn baseline ByteTrack `conf=0.30`, nhưng các đối tượng rất xa vẫn là trường hợp khó.

## 4. Nếu có thêm thời gian

Nhóm sẽ quét `conf` mịn hơn quanh 0.15–0.25 cho từng cảnh và ghi lại chính xác các frame xảy ra đổi ID. Với video_4, nhóm cũng sẽ so sánh thêm `conf=0.25` để tìm điểm cân bằng giữa người nhỏ bị bỏ sót và hộp giả do phản chiếu.
