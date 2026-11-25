# Phụ lục · Kết quả hỗ trợ và kiểm thử

## Điền giá trị thiếu trên sáu đặc trưng

Chương 02 giữ so sánh ban đầu trên sáu đặc trưng và thực nghiệm chính trên 69 đặc trưng. Hai ma trận đầu vào và hai tập ô bị che khác nhau. Sai số gộp giữa hai bảng chịu ảnh hưởng đồng thời từ phạm vi đặc trưng và cách chọn ô che. Dưới đây là kết quả đã lưu từ notebook.

```{embed} #stage02-cell-19
:remove-input: true
:remove-output: false
```

## Chạy kiểm thử

Chạy từ thư mục repo với môi trường đã cài:

```bash
.venv/bin/python -m unittest discover -s tests -v
```

Các kiểm thử dùng mẫu nhỏ để kiểm tra Little, chia tập và bảo toàn giá trị quan sát, che ô và RMSE, ngưỡng ngoại lai, Jaccard và KS, Levene, mã nhị phân, VIF, Target OOF, lựa chọn đặc trưng trong fold và lấy mẫu đúng phạm vi. Khi cần, test nạp định nghĩa hàm của notebook để kiểm tra chính mã thực nghiệm.

## Kết quả đầy đủ trong các chương

Các bảng mở rộng lưu 69 phép kiểm phân phối, ma trận tương quan và cỡ mẫu theo cặp, 17 cặp tương quan mạnh, sai số điền theo đặc trưng, 621 phép so sánh KS, 414 thống kê co giãn, 145 dòng VIF, 110 kết quả lựa chọn đặc trưng và 20 kết quả lấy mẫu lại. [Tổng quan phần A](index.md) · [Đối chiếu tiêu chí](../../RUBRIC_AUDIT.md)
