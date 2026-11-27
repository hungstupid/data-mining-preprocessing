# Đối chiếu với đề bài

Đồ án chọn dữ liệu bảng ở phần (a) và văn bản ở phần (b). Mỗi hàng dẫn đến chương có phương pháp, mã và kết quả tương ứng. [Đề và rubric HCMUS](https://hcmus-cs-ta.github.io/lab-book/data-mining/projects/preprocessing/)

## Dữ liệu bảng

| Yêu cầu | Vị trí kiểm tra |
|---|---|
| Điều kiện dữ liệu và EDA | [Phân tích khám phá](book/tabular/01_eda.ipynb). Kiểm định phân phối cho 69 biến số, Pearson và Spearman, bảng và ma trận giá trị thiếu. Kiểm định Little xét tuổi và BMI với tham chiếu Gaussian. Cơ chế thiếu của toàn bảng chưa xác định. |
| Điền giá trị thiếu | [Điền khuyết](book/tabular/02_preprocessing.ipynb). So sánh trung bình, trung vị, mode, kNN 3/5/10 và MICE bằng RMSE trên cùng mặt nạ ngẫu nhiên. Bảng sáu biến là đối chiếu riêng. |
| Ngoại lai | [Ngoại lai](book/tabular/03_outliers.ipynb). IQR, Z-score, Isolation Forest, LOF, DBSCAN, tỷ lệ gắn cờ, Jaccard và KS trước/sau khi giả định loại điểm. |
| Co giãn và mã hóa | [Co giãn](book/tabular/04_scaling.ipynb) có Min-Max, Z-score, Robust, Quantile và violin, kèm Levene cho BMI. [Mã hóa](book/tabular/05_encoding.ipynb) có One-Hot, Ordinal, Target Encoding ngoài fold theo ZIP, Binary, Frequency và VIF. |
| Chọn đặc trưng và giảm chiều | [Lựa chọn đặc trưng](book/tabular/06_feature_selection.ipynb). ANOVA, Chi-square, MI, Random Forest, Gradient Boosting, RFE và PCA. Xem bảng F1 theo năm fold và các hình PCA, t-SNE. |
| Mất cân bằng lớp · nâng cao | [Mất cân bằng lớp](book/tabular/07_class_imbalance.ipynb). SMOTE, ADASYN và RUS chỉ lấy mẫu trong phần huấn luyện. Có Precision, Recall, F1-macro và AUC trên các phần giữ lại. |

(van-ban)=
## Văn bản

| Yêu cầu | Vị trí kiểm tra |
|---|---|
| Điều kiện dữ liệu và EDA | [Phân tích khám phá](book/text/01_eda.ipynb). Độ dài theo lớp, Mann–Whitney U, word cloud, top-50, TTR và Zipf. |
| Chuẩn hóa và tách token | [Chuẩn hóa và tách token](book/text/02_normalization_tokenization.ipynb). Tác động của từng bước lên từ vựng và độ dài. So sánh từ, câu, ký tự và BPE qua OOV, kích thước từ vựng và độ dài chuỗi. |
| Từ dừng và hình thái | [Từ dừng và hình thái](book/text/03_stopwords_morphology.ipynb). MI và Naive Bayes trước/sau bỏ từ dừng. Porter, Snowball và WordNet được so sánh bằng tỷ lệ va chạm và F1-macro Logistic Regression qua năm fold. |
| Vector hóa | [Biểu diễn văn bản](book/text/04_representations.ipynb). BoW, TF-IDF với các dải n-gram và Word2Vec học trên tập huấn luyện. Xem số chiều, độ thưa, cosine, t-SNE và silhouette. |
| Sentence Transformer · nâng cao | Cùng chương biểu diễn, các mục MiniLM, K-Means và Linear SVM so sánh embedding đóng băng với TF-IDF. |

## Mã nguồn và báo cáo

[README](README.md) ghi danh tính, nguồn dữ liệu, cách cài đặt và lệnh dựng sách. [`src/`](https://github.com/hungstupid/data-mining-preprocessing/tree/main/src) chứa các hàm dùng chung và [`tests/`](https://github.com/hungstupid/data-mining-preprocessing/tree/main/tests) kiểm tra công thức, phép chia và ranh giới huấn luyện. [Tổng kết](book/ket-luan.md) trình bày các quyết định dựa trên thực nghiệm và giới hạn áp dụng.

(library-policy)=
## Phạm vi công cụ

Đề yêu cầu UMAP khi dữ liệu lớn nhưng chưa quy định ngưỡng. Phần Tabular khớp PCA trên 8.173 dòng huấn luyện và dùng 2.000 dòng để vẽ hình PCA và chạy t-SNE. Gensim và WordCloud phục vụ Word2Vec và đám mây từ. Hai tên này chưa được nêu trong danh sách thư viện chung của đề. [Đề và yêu cầu kỹ thuật](https://hcmus-cs-ta.github.io/lab-book/data-mining/projects/preprocessing/) · [Thiết lập Gensim](README.md)
