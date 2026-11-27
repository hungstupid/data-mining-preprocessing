# Tiền xử lý dữ liệu

**Nguyễn Đức Hưng · 24127174**

Đồ án cá nhân môn Khai phá dữ liệu và ứng dụng, HCMUS.

Đồ án khảo sát cách xử lý giá trị thiếu, ngoại lai, thang đo và đặc trưng trên WiDS, đồng thời so sánh chuẩn hóa, tách token và biểu diễn mô tả sản phẩm trên E-commerce. Có thể đọc toàn bộ bảng và hình ngay trên sách công khai. [Jupyter Book](https://hungstupid.github.io/data-mining-preprocessing/) · [Đề và rubric](https://hcmus-cs-ta.github.io/lab-book/data-mining/projects/preprocessing/) · [Bảng đối chiếu](RUBRIC_AUDIT.md)

| Phần | Dữ liệu | Kết quả chính |
|---|---|---|
| A. Dữ liệu bảng | 12.906 dòng, 83 cột. [WiDS Datathon 2024 Challenge #1](https://www.kaggle.com/competitions/widsdatathon2024-challenge1/data) | kNN10 có Macro NRMSE 0,676330 trên cùng 14.181 ô che. Giữ toàn bộ dòng sau so sánh ngoại lai. |
| B. Văn bản | 50.425 mô tả, bốn nhãn gốc. [E-commerce Text Classification](https://www.kaggle.com/datasets/saurabhshahane/ecommerce-text-classification) | TF-IDF unigram đạt F1-macro 0,957556 với Linear SVM. Cụm MiniLM khớp danh mục tốt hơn theo ARI. |

Bắt đầu ở [tổng quan phần A](book/tabular/index.md) hoặc [tổng quan phần B](book/text/index.md). [Tổng kết](book/ket-luan.md) nêu quyết định, bằng chứng và giới hạn của từng phần.

## Cài đặt để tái lập

Dùng Python **3.13.3**, Git, trình biên dịch C và Node.js **24.x**. Lockfile đã được kiểm tra trên macOS arm64. Với macOS, trình biên dịch có trong Xcode Command Line Tools. Với Linux, cần compiler và header Python để dựng Gensim từ nguồn.

```bash
git clone https://github.com/hungstupid/data-mining-preprocessing.git
cd data-mining-preprocessing
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-lock.txt
python -m pip check
python -m ipykernel install --sys-prefix --name hcmus-wids --display-name "Python (HCMUS WiDS .venv)"
```

`requirements.txt` ghi các phụ thuộc trực tiếp. `requirements-lock.txt` ghim cả các phiên bản phụ thuộc. Gensim dùng đúng commit `ecf22c266f3b8930610114c149d8991ed14e2a16` để sửa trường hợp tích vô hướng −1 bị trả thành 0 ở bản 4.4.0. Ô Word2Vec kiểm tra bản cài và kết quả số trước khi huấn luyện. Commit sửa còn nằm trong PR upstream. [Lỗi #3665](https://github.com/piskvorky/gensim/issues/3665) · [Bản sửa #3668](https://github.com/piskvorky/gensim/pull/3668)

## Lấy dữ liệu gốc

### WiDS Datathon 2024 Challenge #1

Xác thực Kaggle ngoài repo, chấp nhận điều khoản cuộc thi và đặt tệp `training.csv` ở `data/raw/training.csv`. Lệnh kiểm tra đọc đúng tệp này theo mặc định và in SHA-256. [Điều khoản WiDS](https://www.kaggle.com/competitions/widsdatathon2024-challenge1/rules) · [Xác thực Kaggle](https://github.com/Kaggle/kaggle-cli/blob/main/docs/README.md#authentication)

```bash
kaggle competitions download widsdatathon2024-challenge1 -p data/raw
python -m zipfile -e data/raw/widsdatathon2024-challenge1.zip data/raw
python src/validate_dataset.py
```

SHA-256 của tệp đã dùng là `e9947ecfe1cdacafbf9cbcdc0abd024396f617c701b056fa54e5881f1bb9bbe9`. Notebook EDA có tùy chọn `DOWNLOAD_IF_MISSING` để chuẩn bị khi chưa có tệp. Kiểm tra cấu trúc và các điều kiện về kiểu biến, tỷ lệ thiếu nằm trong chương EDA. Quyền tải do Kaggle quản lý. Dữ liệu thô và thông tin xác thực được giữ ngoài Git.

### E-commerce Text Classification

Đặt tệp CSV gốc không có hàng tiêu đề tại `data/raw/ecommerce/ecommerceDataset.csv`. Notebook EDA có thể tải qua Kaggle nếu chưa có tệp và dùng lại ZIP đã tải. Bản Zenodo CC BY 4.0 được đối chiếu trùng từng byte với bản Kaggle. Có thể tải trực tiếp từ nguồn này. [Kaggle](https://www.kaggle.com/datasets/saurabhshahane/ecommerce-text-classification) · [Zenodo, DOI 10.5281/zenodo.3355823](https://zenodo.org/records/3355823)

```bash
mkdir -p data/raw/ecommerce
if [ ! -f data/raw/ecommerce/ecommerceDataset.csv ]; then
  curl -fL https://zenodo.org/records/3355823/files/ecommerceDataset.csv \
    -o data/raw/ecommerce/ecommerceDataset.csv
fi
shasum -a 256 data/raw/ecommerce/ecommerceDataset.csv
```

Chỉ tải khi chưa có tệp gốc. SHA-256 đã xác minh là `1d44be1780bc9558f40ab4cee5b32051ddfe90647cd525b9652b47cdb233593f`. MD5 theo Zenodo là `6f2cfdb475096244916aeed6f776c1a6`. Notebook giữ văn bản tiếng Anh và nhãn nguồn, nhận trường CSV rỗng là thiếu và giữ nguyên chuỗi như `NA`.

## Chạy notebook và kiểm thử

Mở Jupyter Lab từ thư mục repo, chọn kernel `hcmus-wids` và dùng **Restart Kernel and Run All** cho từng chương. Mỗi chương tự đọc dữ liệu nguồn. Một lượt chạy toàn bộ có thể mất hơn 10 phút trên CPU, phần biểu diễn MiniLM chiếm nhiều thời gian nhất.

```bash
for notebook in book/tabular/0[1-7]_*.ipynb book/text/0[1-4]_*.ipynb; do
  python -m nbconvert --to notebook --execute --inplace \
    --ExecutePreprocessor.kernel_name=hcmus-wids \
    --ExecutePreprocessor.timeout=1200 "$notebook" || exit 1
done
python -m unittest discover -s tests -v
```

Kiểm thử đơn vị dùng dữ liệu nhỏ có đáp án biết trước, kiểm tra công thức, ranh giới dữ liệu, rò rỉ và Gensim. Chạy đầy đủ cần hai CSV gốc. Các notebook tách token và hình thái dùng tài nguyên NLTK `punkt_tab`, `stopwords`, `wordnet`. Notebook tải từng tài nguyên khi thiếu. Có thể tải trước bằng lệnh sau.

```bash
python -m nltk.downloader -d .cache/nltk_data punkt_tab stopwords wordnet
```

Chương biểu diễn dùng `sentence-transformers/all-MiniLM-L6-v2` trên CPU, ghim revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`. Trọng số công khai tải lần đầu và lưu trong `.cache/huggingface/`. Việc chạy lại tính lại vector từ trọng số đó. [Thẻ mô hình](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)

## Dựng và đọc sách

Lệnh dựng dùng đầu ra đã lưu trong notebook, chạy được với môi trường chỉ có Jupyter Book 2.1.7 và Node.js 24.x, không cần quyền tải dữ liệu. Lượt đầu cần mạng để lấy theme. Lệnh xem trực tiếp chạy từ thư mục repo.

```bash
jupyter book start
```

Dựng bản tĩnh cho GitHub Pages bằng:

```bash
export BASE_URL=/data-mining-preprocessing
jupyter book build --html
python scripts/localize_book.py
```

Kết quả ở `_build/html/`. Script đặt ngôn ngữ trang tiếng Việt và chuyển hai đường dẫn phụ lục cũ tới phần tương ứng. GitHub Actions dùng cùng lệnh khi xuất bản từ `main`. Giữ đầu ra đã chạy trong notebook để các hình và bảng xuất hiện trong bản tĩnh.

| Vị trí | Nội dung |
|---|---|
| `book/tabular/`, `book/text/` | 11 notebook, kết quả đã lưu và hướng dẫn đọc |
| `myst.yml` | Tên sách, mục lục và cấu hình dựng |
| `src/` | Xử lý dữ liệu dùng chung, phép kiểm, biểu diễn và nhãn trình bày |
| `tests/` | Kiểm tra công thức, dữ liệu và các ranh giới huấn luyện |
| `data/raw/` | Nơi đặt dữ liệu tải từ nguồn, Git chỉ lưu tệp đánh dấu thư mục |
| `RUBRIC_AUDIT.md` | Vị trí bằng chứng theo đề bài |

## Phạm vi kết quả và công cụ

Đồ án đánh giá nội bộ sau khi EDA đã khảo sát toàn bộ hai tập nguồn. Chia nhóm ZIP hạn chế chia sẻ bối cảnh địa lý giữa các fold WiDS. Nhóm theo văn bản chuẩn hóa hạn chế trùng chuỗi trong CV văn bản. Biến thể sản phẩm, thời điểm có sẵn của biến lâm sàng và tính đại diện cho nguồn khác vẫn cần xác minh.

AI hỗ trợ rà soát, tinh gọn mã, biên tập báo cáo và kiểm thử. Notebook và mã nguồn lưu cách tính cùng kết quả để kiểm tra và chạy lại. [Quy định triển khai và nộp bài](https://hcmus-cs-ta.github.io/lab-book/data-mining/projects/preprocessing/)
