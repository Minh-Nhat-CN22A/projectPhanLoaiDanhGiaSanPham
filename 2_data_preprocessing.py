import pandas as pd
import os
from utils import clean_text  # Gọi hàm làm sạch mà bạn vừa viết

def preprocess_data(input_file, output_file):
    print(f"[*] Đang đọc dữ liệu từ: {input_file}")
    
    if os.path.exists(input_file) == False:
        print(f"[Lỗi] Không tìm thấy file {input_file}. Hãy chạy file 1_data_labeling.py trước!")
        return
        
    df = pd.read_csv(input_file)
    print(f"[*] Tổng số dòng dữ liệu cần làm sạch: {len(df)}")
    print("[*] Đang tiến hành làm sạch, chuẩn hóa và tách từ (NLP). Vui lòng đợi...")
    
    # Dùng hàm apply để cho toàn bộ cột Review chạy qua hàm clean_text
    df['Cleaned_Review'] = df['Review'].apply(clean_text)
    
    # Sau khi lọc stop words và icon, sẽ có những câu trở thành trống (không còn chữ nào)
    # Ta cần loại bỏ những dòng trống này
    dieu_kien_khac_rong = (df['Cleaned_Review'] != "")
    df = df[dieu_kien_khac_rong]
    
    # Sắp xếp lại các cột cho đẹp: Giữ lại câu gốc, câu đã làm sạch và nhãn
    df = df[['Review', 'Cleaned_Review', 'Label']]
    
    # Lưu ra file cuối cùng
    thu_muc_luu = os.path.dirname(output_file)
    if os.path.exists(thu_muc_luu) == False:
        os.makedirs(thu_muc_luu)
        
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"[+] Hoàn thành 100% nhiệm vụ Tiền xử lý! Dữ liệu Model-Ready lưu tại: {output_file}")
    
    # In thử 3 dòng đầu tiên ra màn hình để kiểm tra
    print("-" * 50)
    print("XEM TRƯỚC 3 DÒNG DỮ LIỆU ĐÃ CHUẨN HÓA:")
    print(df[['Cleaned_Review', 'Label']].head(3))
    print("-" * 50)

if __name__ == "__main__":
    INPUT_PATH = "data/labeled_data.csv"
    OUTPUT_PATH = "data/clean_data.csv"
    
    preprocess_data(INPUT_PATH, OUTPUT_PATH)