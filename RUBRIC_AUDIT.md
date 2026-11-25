# Đối chiếu tiêu chí và bằng chứng

Đồ án cá nhân của **Nguyễn Đức Hưng, 24127174**. Đã đọc đề chính thức và bảng điểm ngày 25/11/2026. Phạm vi chấm là dữ liệu bảng ở phần (a), văn bản ở phần (b) và chất lượng nguồn, repository, báo cáo. Phiên bản trước hoàn thiện là `0709c5b4503b7aba5159954119ca761ce9521736`. [Đề và rubric HCMUS](https://hcmus-cs-ta.github.io/lab-book/data-mining/projects/preprocessing/)

**PASS** xác nhận có thực nghiệm và bằng chứng trong phạm vi ghi rõ. **PARTIAL** chỉ điều kiện còn cần xác nhận. Tự đánh giá dựa trên nội dung và kết quả. Điểm do giảng viên quyết định.

## Bảng điểm chính thức

| Tiêu chí | Tối đa | Bằng chứng và vị trí | Trạng thái | Tự đánh giá |
|---|---:|---|---|---:|
| (a) EDA với kiểm định phân phối và MCAR | 10 | 69 phép kiểm đúng theo cỡ mẫu, hai ma trận tương quan, 17 cặp mạnh, missingno và bảng tỷ lệ thiếu kèm kiểu. Little trên tuổi–BMI cho χ² 3,506534, df 1, p 0,061127. [EDA bảng](book/tabular/01_eda.ipynb) | PASS | 10 |
| (a) Phát hiện ngoại lai và mã hóa | 10 | Chín cấu hình gồm IQR, Z, Isolation Forest, LOF, DBSCAN, ma trận Jaccard và 621 so sánh KS. Năm bộ mã hóa, Target OOF theo ZIP, 145 dòng VIF và hạng toàn thiết kế. [Ngoại lai](book/tabular/03_outliers.ipynb) · [Mã hóa](book/tabular/05_encoding.ipynb) | PASS | 10 |
| (a) Lựa chọn đặc trưng với F1 qua CV | 10 | ANOVA, Chi-square, MI, RF, GB, RFE, PCA; 22 cấu hình, 110 lần đánh giá, mốc F1-macro 0,452154 và đường F1 theo số cột. Có phổ PCA, chiếu PCA và t-SNE. UMAP có điều kiện, xem bên dưới. [Lựa chọn đặc trưng](book/tabular/06_feature_selection.ipynb) | PASS trong phạm vi đã nêu | 10 |
| (b) Text EDA với Zipf | 10 | Kiểm định từng cặp độ dài từ và ký tự, phân tích bỏ trùng, bốn đám mây từ và bốn bảng 50 token, TTR. Zipf toàn tập có dốc −1,173 và R² 0,9772 trên miền đã chọn. [EDA văn bản](book/text/01_eda.ipynb) | PASS | 10 |
| (b) Chuẩn hóa và so sánh bộ tách qua OOV | 10 | Từng bước có số thay đổi từ vựng và độ dài. Cùng đầu vào nhẹ cho từ/câu/ký tự/BPE với OOV 3,0714%/75,6723%/0,0029%/0%. Có đối chiếu từ dừng, MI, NB và hình thái theo CV. [Chuẩn hóa, tách token](book/text/02_normalization_tokenization.ipynb) · [Từ dừng và hình thái](book/text/03_stopwords_morphology.ipynb) | PASS | 10 |
| (b) Vector hóa, silhouette và Sentence Transformer | 10 | BoW, ba dải TF-IDF, CBOW và MiniLM thật. Báo số chiều, độ thưa, 4.800 cặp cosine, sáu hình t-SNE và silhouette gốc. So sánh K-Means và SVM trên cùng dữ liệu. [Biểu diễn](book/text/04_representations.ipynb) | PASS | 10 |
| Mã sạch, có chú thích và tái sản xuất được | 10 | Pipeline theo fold, gói ghim phiên bản, kiểm tra Gensim, kiểm thử công thức, ranh giới dữ liệu và tái chạy. Danh sách thư viện chung cần xác nhận hai tên cụ thể. [README](README.md) · [Đối chiếu thư viện](#library-policy) | PARTIAL về xác nhận thư viện | 9 |
| Repository cá nhân, cấu trúc book và README | 10 | Danh tính, dữ liệu, phiên bản, cách chạy, dựng sách từ notebook và link Pages. Git chỉ chứa mã, tệp đánh dấu dữ liệu và kết quả được lưu. [README](README.md) · [Jupyter Book](https://hungstupid.github.io/data-mining-preprocessing/) | PASS | 10 |
| Chương báo cáo, phân tích và thảo luận | 20 | 11 chương có mục đích, công thức thích hợp, mã, số liệu và diễn giải. Tổng kết đối chiếu các chỉ số và giới hạn của mỗi quyết định. [Tổng kết](book/ket-luan.md) | PASS | 20 |
| **Tổng điểm tối đa theo đề** | **100** | **Phần (a) 30, phần (b) 30 và chất lượng 40** | | **99** |

## Yêu cầu bắt buộc, nâng cao và điều kiện

| Nội dung | Phân loại trong đề | Bằng chứng và giới hạn |
|---|---|---|
| Chọn đúng dạng dữ liệu và đủ kích thước | Bắt buộc | WiDS 12.906 × 83, có biến số và phân loại, BMI thiếu 69,46%. Văn bản 50.425 dòng và bốn nhãn. [Phần A](book/tabular/index.md) · [Phần B](book/text/index.md) |
| Bảng thiếu kèm kiểu và Little | EDA bắt buộc, bổ sung cách trình bày theo giải đáp giảng viên | Bảng chính có tên, dtype, kiểu ngữ nghĩa, số ô và tỷ lệ thiếu. Phần mở rộng có đủ 81 đặc trưng. Giải đáp về Adult nhắc trình bày tỷ lệ và kiểu; WiDS vẫn chạy Little trên tuổi và BMI vì mức đo cấp cá nhân. Giá trị p > 0,05 chỉ là chưa bác bỏ tham chiếu trên phạm vi đó. [EDA bảng](book/tabular/01_eda.ipynb) |
| Điền thiếu và co giãn | Bắt buộc, Levene là phép kiểm đề cho phép | Trung bình, trung vị, mode, kNN 3/5/10 và MICE trên cùng mặt nạ MCAR 10%. RMSE gộp, Macro NRMSE cùng phân tích biên dữ liệu. Min-Max, Z-score, Robust, phân vị đều và chuẩn, violin, Levene trên BMI quan sát. [Điền thiếu](book/tabular/02_preprocessing.ipynb) · [Co giãn](book/tabular/04_scaling.ipynb) |
| Cách đọc VIF và F1 | VIF bắt buộc; CV F1 được tính điểm trực tiếp | VIF là hệ số phóng đại phương sai. Phạm vi VIF trên mọi cột mã hóa và sáu biến số cố định. Hạng SVD xét thiết kế đầy đủ. CV học từng bước trong phần huấn luyện của từng fold và báo đủ F1. [Mã hóa](book/tabular/05_encoding.ipynb) · [Lựa chọn đặc trưng](book/tabular/06_feature_selection.ipynb) |
| SMOTE, ADASYN và RUS | Nâng cao | Lấy mẫu trong phần huấn luyện, chấm tập giữ tỷ lệ gốc. Có precision, recall, F1-macro, AUC và Brier. Chỉ đánh giá một cấu hình khóa trên tập dự trữ. [Mất cân bằng lớp](book/tabular/07_class_imbalance.ipynb) |
| Từ dừng và hình thái | Bắt buộc | Bỏ 180 loại, MI trung bình 0,00041228 → 0,00039878 nat, NB F1 0,938031 → 0,939891. Va chạm và Logistic Regression trên năm fold cho mốc, Porter, Snowball và WordNet. [Từ dừng và hình thái](book/text/03_stopwords_morphology.ipynb) |
| Sentence Transformer | Nâng cao trong mô tả, có tên trong bảng điểm | MiniLM đóng băng, đối chiếu K-Means và Linear SVM với TF-IDF. Có số liệu về độ dài và giới hạn cắt token. [Đối chiếu chi tiết phần B](docs/TEXT_RUBRIC_AUDIT.md) |
| Phân tích hỗ trợ | Đồ án tự bổ sung | Macro NRMSE, kiểm tra biên MICE, độ nhạy bỏ trùng và Holm, ARI, phân tích dung lượng, kiểm thử trình duyệt. Bằng chứng hỗ trợ đọc và giải thích các phép so sánh chính. |

(library-policy)=
## Quy định thư viện và UMAP

Đề ghi Python và các thư viện NumPy, pandas, Matplotlib, Seaborn, scikit-learn, SciPy, statsmodels, missingno, imbalanced-learn, NLTK hoặc spaCy, công cụ tải dữ liệu và PyTorch/TensorFlow. Tokenizers và Sentence Transformers được chỉ rõ ở các yêu cầu tương ứng. Các gói Jupyter, dựng sách và phụ thuộc gián tiếp dùng để chạy, trình bày hoặc phục vụ các gói đã ghim.

- **UMAP.** Đề yêu cầu khi dữ liệu lớn và chưa đặt ngưỡng. Dữ liệu có 12.906 dòng, hình PCA/t-SNE dùng cùng 2.000 dòng huấn luyện và chạy được trên CPU. Danh sách thư viện chung chưa liệt kê `umap-learn`. Vì vậy đồ án giữ phạm vi trực quan hóa hiện tại. Nếu giảng viên xem WiDS thuộc điều kiện bắt buộc, cần xác nhận thư viện được dùng.
- **Gensim và WordCloud.** Đồ án dùng Gensim để đáp ứng Word2Vec và WordCloud để vẽ đám mây từ. Hai tên này chưa xuất hiện trong danh sách thư viện chung. Cần xác nhận giảng viên chấp nhận chúng cho các kỹ thuật đã nêu. Bản Gensim 4.4.0 vẫn có lỗi số học đã ghi nhận; phiên bản nguồn cố định vượt kiểm thử tương ứng. [PR sửa lỗi Gensim](https://github.com/piskvorky/gensim/pull/3668) · [Điều kiện cài đặt](README.md)

## Quy định nộp bài

| Yêu cầu | Đối chiếu |
|---|---|
| Một Jupyter Book công khai trên GitHub Pages của repo cá nhân | Nội dung sách lấy trực tiếp từ 11 notebook và các trang dẫn đọc trong cùng repo. Nộp một đường dẫn sách trên Moodle. [Sách công khai](https://hungstupid.github.io/data-mining-preprocessing/) |
| Nội dung nguồn, dữ liệu và cấu hình | Có hướng dẫn môi trường, nguồn Kaggle và Zenodo, quyền tải WiDS và checksum hai tệp. Notebook EDA có bước chuẩn bị dữ liệu. Tệp gốc và trọng số lưu cục bộ. [README](README.md) |
| Báo cáo chạy sạch và có biến Python | Các phép tính chính trả kết quả trong notebook, kèm dữ liệu tổng hợp, bảng, hình, diễn giải và cách chạy lại. |
| Ngôn ngữ, danh tính và vấn đáp | Báo cáo tiếng Việt theo yêu cầu hoàn thiện, giữ định danh kỹ thuật và trích dẫn gốc. Nguyễn Đức Hưng và MSSV 24127174 có ở README và trang chủ. Các chương nêu lý do, cách làm và kết quả theo phạm vi vấn đáp ngày 25/11. |
| Liêm chính và AI | Đề cho phép AI hỗ trợ viết mã và phân tích. README ghi phạm vi hỗ trợ trong lần hoàn thiện. Sinh viên cần hiểu và giải thích phần đã thực hiện. |

## Kiểm tra khi hoàn thiện

- Đã cài mới môi trường Python 3.13.3 từ lockfile trên macOS arm64, dựng Gensim từ commit nguồn, chạy kiểm tra phụ thuộc và 48 kiểm thử đơn vị. Kiểm tra Gensim bao gồm trường hợp tích vô hướng −1, CBOW và Skip-gram.
- Đã chạy cả 11 notebook với kernel mới, trên đúng hai CSV theo checksum. Đối chiếu 302 bảng với bản trước hoàn thiện. Giá trị định lượng khớp sau khi bỏ các phép đo thời gian và bộ nhớ phụ thuộc môi trường. Các công thức dạng khối và thiết lập thực nghiệm được giữ. Bảng thiếu có thêm kiểu dữ liệu và phần tóm tắt theo giải đáp của giảng viên.
- Giữ một Jupyter Book từ các notebook có kết quả đã lưu. Bản dựng không cần dữ liệu gốc hoặc trọng số. Các hình có mô tả tiếng Việt và có thể xem cùng bảng, công thức và mã. Nút do MyST cung cấp vẫn dùng nhãn mặc định của theme ở một số vị trí.
