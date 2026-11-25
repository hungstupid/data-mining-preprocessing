# Đối chiếu chi tiết phần B

Bảng này dẫn đến các phép đo văn bản. Trọng số và quy định thư viện nằm trong bảng đối chiếu chung. [Đối chiếu toàn đồ án](../RUBRIC_AUDIT.md) · [Đề đồ án](https://hcmus-cs-ta.github.io/lab-book/data-mining/projects/preprocessing/)

| Yêu cầu | Bằng chứng | Kết quả |
|---|---|---|
| Điều kiện nguồn, độ dài, kiểm định | CSV gốc 50.425 mô tả, bốn lớp. Thống kê độ dài và 12 phép kiểm Mann–Whitney có Holm, lặp trên tập bỏ trùng. [EDA](../book/text/01_eda.ipynb) | PASS |
| Từ phổ biến, TTR và Zipf | Bốn đám mây và bốn bảng 50 token. 81.531 loại trên 5.918.452 lượt. Hệ số góc −1,173, R² 0,9772 trên khoảng hạng công bố. [EDA](../book/text/01_eda.ipynb) | PASS |
| Chuẩn hóa và OOV | So từng bước trên 22.201 dòng huấn luyện. Từ vựng từ 72.746 còn 72.299 loại. OOV đánh giá đo trên cùng đầu vào nhẹ cho từ, câu, ký tự và byte-level BPE. [Chuẩn hóa](../book/text/02_normalization_tokenization.ipynb) | PASS |
| Từ dừng, hình thái | Bỏ 180 loại. MI và Naive Bayes đo trước/sau. Tỷ lệ nén của Porter, Snowball và WordNet danh từ là 20,55%, 20,72% và 7,47%. Có hai chỉ số va chạm và F1 riêng từng fold Logistic Regression. [Từ dừng và hình thái](../book/text/03_stopwords_morphology.ipynb) | PASS |
| BoW, TF-IDF và Word2Vec | Ba dải TF-IDF tích lũy, giới hạn 30.000 cột. Số ứng viên n-gram lần lượt 36.099, 299.680 và 631.052. CBOW 100 chiều học 40.880 loại trên tập huấn luyện. [Biểu diễn, mục 1–2](../book/text/04_representations.ipynb) | PASS |
| Độ thưa, cosine và t-SNE | Sáu kích thước và số phần tử khác 0. Độ thưa 99,63–99,77% ở ma trận thưa. 2.400 cặp cùng lớp và 2.400 cặp khác lớp dùng chung. Chiếu t-SNE cùng 1.200 dòng, tính silhouette ở không gian gốc. [Biểu diễn, mục 4–7](../book/text/04_representations.ipynb) | PASS |
| Sentence Transformer, phân cụm và phân loại | MiniLM 384 chiều, 2.864 mô tả vượt giới hạn 256 token con. Silhouette cosine theo cụm của TF-IDF là 0,011900, MiniLM là 0,104771. ARI lần lượt 0,326454 và 0,727192. F1-macro SVM lần lượt 0,957514 và 0,937824. [Biểu diễn, mục 3, 6 và 8](../book/text/04_representations.ipynb) | PASS |
| Ranh giới học và tái lập | Khóa 11 nhóm chuỗi chuẩn hóa trùng trước khi thử từ dừng hay hình thái. Tạo mới từ vựng, IDF và mô hình trong phần huấn luyện của từng fold. MiniLM công khai đóng băng. Gensim ghim commit sửa số học và có kiểm thử. [Giao thức](../book/text/index.md) · [README](../README.md) | PASS |

Nhóm theo chuỗi giống nhau hạn chế chia trùng trực tiếp. Biến thể sản phẩm và việc khảo sát toàn bộ dữ liệu trong EDA vẫn ảnh hưởng đến tính độc lập. Các điểm CV dùng để so sánh cấu hình trong nguồn này.
