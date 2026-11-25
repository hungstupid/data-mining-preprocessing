# Phần A · Dữ liệu dạng bảng

## Bài toán và dữ liệu

Tập huấn luyện WiDS Datathon 2024 Challenge #1 có 12.906 dòng, 83 cột, 69 ứng viên số và 12 trường phân loại, mã hoặc mô tả. Nhãn `DiagPeriodL90D` phân biệt nhóm chẩn đoán trong khoảng 90 ngày (1) và nhóm bù (0). `patient_id` chỉ xác định dòng. ZIP3 giữ nguyên dạng chuỗi, dùng để chia nhóm. BMI và điều trị được ghi sau khi phát hiện di căn. Cần xác minh thời điểm có dữ liệu, kỳ tham chiếu và đơn vị trước khi áp dụng như một mô hình dự báo. [Dữ liệu WiDS](https://www.kaggle.com/competitions/widsdatathon2024-challenge1/data) · [Giải thích nhãn trong EDA](01_eda.ipynb)

## Các chương

| Chương | Câu hỏi |
|---|---|
| [01. Phân tích khám phá](01_eda.ipynb) | Các cột có kiểu, phân phối, tương quan và mẫu hình thiếu như thế nào? |
| [02. Điền giá trị thiếu](02_preprocessing.ipynb) | Phương án nào khôi phục tốt nhất cùng tập ô quan sát đã che? |
| [03. Ngoại lai](03_outliers.ipynb) | Những dòng nào được gắn cờ và giả định loại chúng sẽ đổi dữ liệu ra sao? |
| [04. Co giãn đặc trưng](04_scaling.ipynb) | Mỗi phép biến đổi tác động thế nào lên thang đo và hình dạng? |
| [05. Mã hóa biến phân loại](05_encoding.ipynb) | Năm cách mã hóa khác nhau ra sao về kích thước, mức mới và VIF? |
| [06. Lựa chọn đặc trưng và giảm chiều](06_feature_selection.ipynb) | Rút gọn có cải thiện F1 trên cùng năm fold ZIP không? |
| [07. Mất cân bằng lớp](07_class_imbalance.ipynb) | Lấy mẫu lại trong phần huấn luyện thay đổi F1, AUC và Brier thế nào? |

## Giao thức đánh giá

| Tập | Số dòng | Số ZIP | Lớp 0 | Lớp 1 | Dùng để |
|---|---:|---:|---:|---:|---|
| Huấn luyện | 8.173 | 443 | 3.064 | 5.109 | Khớp các phép biến đổi và kiểm định chéo |
| Xác thực cho điền thiếu | 2.081 | 148 | 778 | 1.303 | Chấm khôi phục trên các ô đã che |
| Dự trữ | 2.652 | 148 | 1.004 | 1.648 | Chấm một lần cấu hình đã khóa ở chương 07 |

`GroupShuffleSplit` dùng seed 42 và 43 để tạo ba tập tách ZIP. Hai chương cuối dùng cùng năm `StratifiedGroupKFold` với seed 42 trên 8.173 dòng. Phần giữ lại luôn giữ tỷ lệ lớp gốc. EDA đọc toàn bộ bảng nên tập dự trữ chỉ là đánh giá nội bộ sau EDA.

Mỗi notebook chạy từ đầu với kernel `hcmus-wids`. Chương 01 và 02 tự chuẩn bị đầu vào. Các chương sau dùng `src/tabular_data.py` để tái dựng dữ liệu và phép chia. Chương 03–05 tái dựng khâu điền mô tả chỉ từ tập huấn luyện. Chương 06–07 khớp mọi bước học từ dữ liệu lại trong từng fold. [Phụ lục kết quả và kiểm thử](appendix.md) · [Hướng dẫn chạy](https://github.com/hungstupid/data-mining-preprocessing#ch%E1%BA%A1y-notebook-v%C3%A0-ki%E1%BB%83m-th%E1%BB%AD) · [Đối chiếu tiêu chí](../../RUBRIC_AUDIT.md) · [Phần B](../text/index.md)
