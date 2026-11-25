# Tổng kết

## Dữ liệu dạng bảng

WiDS có cột thiếu nhiều và các biến cùng mô tả một khu vực. Kiểm định Little trên tuổi và BMI cho χ² = 3,506534 và p = 0,061127, với một bậc tự do. Đây là thông tin về hai mẫu hình quan sát, đủ để mô tả kết quả kiểm định trong phạm vi đã chọn. Khi cần chọn cách điền, dùng phép che ngẫu nhiên trên tập xác thực để có giá trị thật đối chiếu. [EDA WiDS](tabular/01_eda.ipynb)

- **Giá trị thiếu.** kNN10 cho Macro NRMSE 0,676330, thấp nhất khi bảy cấu hình khôi phục cùng 14.181 ô trên 69 đặc trưng. MICE có RMSE gộp thấp hơn nhưng 912 dự đoán của biến tỷ lệ vượt biên qua ba lần lấy mẫu. Tiêu chí chuẩn hóa theo biến và tính hợp lệ của giá trị đều quan trọng khi triển khai. [So sánh cách điền](tabular/02_preprocessing.ipynb)
- **Ngoại lai.** Giữ toàn bộ dòng. Nếu loại theo IQR, mất 319 trong 443 ZIP huấn luyện. Các quy tắc đưa ra những tập cờ khác nhau, nên có thể dùng cờ để kiểm tra từng trường hợp. [So sánh ngoại lai](tabular/03_outliers.ipynb)
- **Co giãn và mã hóa.** Z-score là mốc cho các mô hình nhạy thang đo. Đối chiếu Robust và ánh xạ phân vị khi quan tâm ảnh hưởng của cực trị hoặc hình dạng phân phối. One-Hot giữ khác biệt giữa mức định danh, còn Binary giảm số cột từ 67 xuống 27. Phụ thuộc địa lý vẫn xuất hiện trong VIF. Target Encoding cần tính ngoài fold để tách nhãn của dòng đang mã hóa. [Co giãn](tabular/04_scaling.ipynb) · [Mã hóa](tabular/05_encoding.ipynb)
- **Đặc trưng và tỷ lệ lớp.** Giữ mốc toàn bộ cột trong phép so sánh chọn đặc trưng vì F1-macro 0,452154 vẫn cao nhất trên cùng năm fold. Trong phép so sánh riêng trên biến số, RUS tăng F1-macro từ 0,426654 lên 0,509298. AUC giảm và Brier tăng. Trên 2.652 dòng dự trữ, RUS có F1-macro 0,500629 và AUC 0,529792. [Lựa chọn đặc trưng](tabular/06_feature_selection.ipynb) · [Lấy mẫu lại](tabular/07_class_imbalance.ipynb)

Chia theo ZIP giữ các dòng cùng khu vực về một phía. Các con số trên là thực nghiệm hồi cứu. Dữ liệu thiếu tự nhiên, thời điểm ghi BMI và các dấu hiệu lâm sàng giới hạn khả năng dùng kết quả để dự báo khi tiếp nhận bệnh nhân.

## Dữ liệu văn bản

Chuỗi lặp xuất hiện nhiều trong dữ liệu E-commerce. Quy tắc khử trùng giữ một mô tả theo khóa chuẩn tắc và cho 27.752 dòng đủ điều kiện. Vì thông số và mã sản phẩm có thể chứa số, dạng chuẩn hóa mặc định giữ chúng. Đầu vào kiểm tra tokenization giữ thêm chữ hoa và dấu câu để so sánh cả bộ tách theo câu. [EDA văn bản](text/01_eda.ipynb) · [Chuẩn hóa và tách token](text/02_normalization_tokenization.ipynb)

- **Tách token.** BPE bao phủ tập đánh giá với OOV bằng 0 nhờ bảng byte. Tách theo câu có OOV 75,6723% theo đơn vị toàn câu. OOV và độ dài chuỗi giúp chọn độ mịn phù hợp với mục tiêu sử dụng.
- **Từ dừng và hình thái.** Bỏ từ dừng làm MI trung bình giảm từ 0,00041228 xuống 0,00039878 nat và làm F1-macro Naive Bayes tăng nhẹ. Porter, Snowball và WordNet nén số loại token ở mức khác nhau, kèm nguy cơ gộp khác nghĩa. Điểm Logistic Regression thay đổi nhỏ. [Thực nghiệm từ dừng và hình thái](text/03_stopwords_morphology.ipynb)
- **Biểu diễn.** TF-IDF unigram đạt F1-macro cao nhất (0,957514) với Linear SVM cố định. MiniLM đạt ARI 0,727192, cao hơn 0,326454 của TF-IDF trong phân cụm K-Means. Trung bình Word2Vec có chênh lệch cosine cùng lớp và khác lớp lớn nhất. Mỗi kết quả phù hợp với một câu hỏi về phân loại, cấu trúc cụm hoặc độ tương đồng. [So sánh biểu diễn](text/04_representations.ipynb)

Các cấu hình văn bản dùng chung dữ liệu và fold. Dù đã khử trùng và gom chuỗi giống nhau, các biến thể sản phẩm còn lại có thể làm kết quả nội bộ cao hơn kết quả trên nguồn mới. Với MiniLM, 12,90% mô tả huấn luyện vượt giới hạn 256 token con nên có thể mất nội dung ở cuối.

## Bài học từ hai phần

Chọn thước đo trước khi so sánh. RMSE gộp ưu tiên cột có sai số theo đơn vị lớn, còn Macro NRMSE cân bằng theo thang đo. F1 theo ngưỡng và AUC theo xếp hạng có thể đổi ngược chiều. Silhouette, ARI và F1 phản ánh các mục đích khác nhau. Giữ thiết lập đánh giá chung và học mọi bước trong đúng phần huấn luyện giúp đọc được từng đánh đổi.

Có thể dùng các bảng và hình trong từng chương để giải thích khi vấn đáp vì sao đồ án chọn kNN10, giữ các dòng ngoại lai, dùng Target OOF hoặc ưu tiên TF-IDF ở bài toán phân loại này. [Đối chiếu tiêu chí và bằng chứng](../RUBRIC_AUDIT.md)
