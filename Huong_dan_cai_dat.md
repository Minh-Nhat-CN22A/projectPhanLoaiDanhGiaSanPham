# 📖 HƯỚNG DẪN CÀI ĐẶT VÀ CHẠY DỰ ÁN AI SENTIMENT ANALYSIS

Chào mừng bạn đến với dự án Phân tích Cảm xúc Bình luận (Sentiment Analysis). Dưới đây là các bước chi tiết để khởi chạy dự án trên máy tính của bạn.

## PHẦN 1: CÀI ĐẶT MÔI TRƯỜNG VÀ THƯ VIỆN

**Bước 1:** Mở Terminal (hoặc Command Prompt / PowerShell) tại thư mục chứa dự án này.

**Bước 2:** Cài đặt toàn bộ thư viện cần thiết bằng lệnh an toàn (dùng `python -m pip` để tránh lỗi):

```
python -m pip install -r requirements.txt
```

_(Lưu ý: Quá trình cài đặt có thể mất vài phút tùy thuộc vào tốc độ mạng của bạn. Hãy chờ cho đến khi hiện thông báo "Successfully installed...")_

## PHẦN 2: QUY TRÌNH CHẠY DỰ ÁN TỪ A-Z

Sau khi cài đặt xong thư viện, bạn hãy chạy tuần tự các bước sau để máy tính học và đưa ra giao diện nhé:

### 1. Thu thập dữ liệu (Tùy chọn)

Nếu bạn chưa có file `raw_data.csv` trong thư mục `data/`, hãy chạy lệnh sau để cào dữ liệu từ sàn TMĐT:

- Cào Tiki: `python scrape_tiki.py`

### 2. Gắn nhãn & Tiền xử lý dữ liệu

Tiếp theo, ta cần dọn dẹp dữ liệu thô thành dữ liệu sạch:

- Chạy lệnh tạo nhãn: `python 1_data_labeling.py`
- Chạy lệnh làm sạch từ vựng: `python 2_data_preprocessing.py`

_(Sau bước này, bạn sẽ có file `clean_data.csv` sẵn sàng cho AI)_

### 3. Đánh giá dữ liệu (EDA) - Trực quan hóa

Để xem sơ đồ, biểu đồ phân phối và WordCloud (mây từ vựng):

- Chạy lệnh: `python eda_assessment.py`

_(Máy tính sẽ lưu các hình ảnh biểu đồ vào thư mục `data/` để bạn đưa vào slide báo cáo)_

### 4. Huấn luyện "Bộ não" AI

Mở file `train_model.ipynb` bằng Jupyter Notebook (hoặc VS Code).

- Chạy tuần tự các Cell từ trên xuống dưới.
- Notebook này sẽ sử dụng các thuật toán tự xây dựng (`custom_tfidf.py`, `custom_logistic_regression.py`, `custom_naive_bayes.py`) để huấn luyện.
- **Kết quả:** Sinh ra thư mục `saved_models/` chứa 2 file `.pkl` (là bộ não của AI).

### 5. Khởi chạy Giao diện Web

Khi đã có "Bộ não" (`.pkl`), bước cuối cùng là bật giao diện website lên để sử dụng:

- Chạy lệnh:

```
python -m streamlit run app.py
```

- Trình duyệt sẽ tự động mở lên với địa chỉ `http://localhost:8501`. Bạn có thể gõ thử các bình luận để xem AI phân tích.
