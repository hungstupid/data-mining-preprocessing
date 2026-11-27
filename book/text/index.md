# Phần B · Dữ liệu văn bản

## Bài toán và dữ liệu

E-commerce Text Classification chứa 50.425 bản ghi từ một nền tảng thương mại điện tử ở Ấn Độ. Mỗi bản ghi gồm mô tả (`text`) và danh mục (`label`), thuộc một trong bốn lớp Household, Books, Clothing & Accessories và Electronics. Tệp gốc có một mô tả thiếu và 22.622 dòng dư do trùng chính xác trong phạm vi hợp lệ. [Kaggle](https://www.kaggle.com/datasets/saurabhshahane/ecommerce-text-classification) · [Zenodo, phiên bản 2, CC BY 4.0](https://zenodo.org/records/3355823)

## Các chương

| Chương | Câu hỏi |
|---|---|
| [01. Phân tích khám phá](01_eda.ipynb) | Độ dài, từ thường gặp, TTR và Zipf khác thế nào theo lớp và sau bỏ trùng? |
| [02. Chuẩn hóa và tách token](02_normalization_tokenization.ipynb) | Mỗi phép chuẩn hóa đổi văn bản ra sao? Tách theo từ, câu, ký tự và BPE khác gì về OOV và độ dài? |
| [03. Từ dừng và xử lý hình thái](03_stopwords_morphology.ipynb) | Bỏ từ dừng đổi MI và Naive Bayes thế nào? Các cách đưa từ về gốc ảnh hưởng va chạm và Logistic Regression ra sao? |
| [04. Biểu diễn văn bản](04_representations.ipynb) | BoW, TF-IDF, Word2Vec và MiniLM khác gì về độ thưa, không gian, phân cụm và Linear SVM? |

## Giao thức đánh giá

Sau khi loại mô tả hoặc nhãn không hợp lệ, khóa xung đột và trùng, còn 27.752 mô tả chuẩn tắc duy nhất. Chia phân tầng 80/20 với seed 42, được 22.201 dòng huấn luyện và 5.551 dòng đánh giá. Hai tập tách biệt về mã dòng và khóa chuẩn tắc. Tập đánh giá dùng cho thống kê OOV và độ dài chuỗi của các bộ tách đã cố định. Sau EDA, mọi điểm phân loại trong phần này đến từ CV nội bộ trên phần huấn luyện.

Các chương 03–04 khớp cùng năm fold theo nhóm chuỗi chuẩn hóa. Có 11 nhóm trùng, gồm 12 dòng dư. Từ vựng, IDF và bộ phân lớp học trong phần huấn luyện của từng fold. MiniLM có trọng số đóng băng. Word2Vec khớp trên toàn tập huấn luyện cho các phép đo mô tả. Tính silhouette trong không gian gốc trên tập con chung, còn t-SNE chỉ dùng để vẽ. Biến thể sản phẩm khác chuỗi vẫn có thể xuất hiện ở hai fold.

Mỗi notebook đọc CSV gốc và dùng kernel `hcmus-wids`. Mã trong `src/text_data.py` dựng lại phép chia, còn `src/text_preprocessing.py` định nghĩa các phép chuẩn hóa dùng chung. [Hướng dẫn tải dữ liệu và chạy](https://github.com/hungstupid/data-mining-preprocessing#l%E1%BA%A5y-d%E1%BB%AF-li%E1%BB%87u-g%E1%BB%91c) · [Đối chiếu tiêu chí văn bản](../../RUBRIC_AUDIT.md#van-ban)
