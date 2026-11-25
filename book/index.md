# Tiền xử lý dữ liệu

**Nguyễn Đức Hưng · 24127174**

Đồ án cá nhân môn Khai phá dữ liệu và ứng dụng, HCMUS.

Đồ án đo tác động của các lựa chọn tiền xử lý trên dữ liệu sức khỏe và mô tả sản phẩm. Mỗi chương trình bày mục đích, cách tính, bảng và hình từ notebook đã chạy.

| Chọn phần để đọc | Bài toán và dữ liệu |
|---|---|
| [Phần A · Dữ liệu dạng bảng](tabular/index.md) | Khảo sát và chuẩn bị 12.906 hồ sơ WiDS có nhãn về thời gian chẩn đoán. [Nguồn WiDS](https://www.kaggle.com/competitions/widsdatathon2024-challenge1/data) |
| [Phần B · Dữ liệu văn bản](text/index.md) | Chuẩn hóa và biểu diễn 50.425 mô tả sản phẩm thuộc bốn danh mục. [Nguồn E-commerce](https://www.kaggle.com/datasets/saurabhshahane/ecommerce-text-classification) |

## Kết quả chính

- Trên WiDS, kNN10 có Macro NRMSE thấp nhất (0,676330) khi khôi phục cùng 14.181 ô. Tỷ lệ gắn cờ ngoại lai và sự thay đổi thành phần ZIP ủng hộ việc giữ toàn bộ dòng. [Điền giá trị thiếu](tabular/02_preprocessing.ipynb) · [Ngoại lai](tabular/03_outliers.ipynb)
- Với mô tả sản phẩm, TF-IDF unigram đạt F1-macro 0,957514 cao nhất trong các cách biểu diễn được chấm bằng Linear SVM. MiniLM cho các cụm khớp danh mục tốt hơn theo ARI. [Biểu diễn văn bản](text/04_representations.ipynb)

## Cách đọc và tái lập

Hai phần tổng quan dẫn đến từng kỹ thuật. Các kết quả chính nằm ngay trong chương. Có thể mở phần mã và bảng chi tiết để kiểm tra. Trang tổng kết gộp các quyết định và phạm vi sử dụng. [Tổng kết](ket-luan.md) · [Đối chiếu tiêu chí](../RUBRIC_AUDIT.md)

Website công khai hiển thị các kết quả đã lưu. Muốn chạy lại, lấy dữ liệu đúng phiên bản và dùng môi trường ghi trong README. [Repository GitHub](https://github.com/hungstupid/data-mining-preprocessing) · [Hướng dẫn tái lập](https://github.com/hungstupid/data-mining-preprocessing#c%C3%A0i-%C4%91%E1%BA%B7t-%C4%91%E1%BB%83-t%C3%A1i-l%E1%BA%ADp) · [Đề đồ án](https://hcmus-cs-ta.github.io/lab-book/data-mining/projects/preprocessing/)
