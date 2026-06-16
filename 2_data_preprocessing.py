import pandas as pd
import os
from utils import clean_text

def kiem_tra_du_so_luong_tu(van_ban):
    """
    Hàm này dùng để chữa bệnh 'Invalid'. 
    Đếm số lượng chữ trong một câu. Nếu câu chỉ có 1 chữ (ví dụ: 'a', 'ok') thì trả về False để xóa.
    """
    # Ép kiểu về chuỗi chữ và cắt câu thành danh sách các từ dựa trên khoảng trắng
    danh_sach_cac_tu = str(van_ban).split()
    
    # Đếm số lượng từ trong danh sách
    so_luong_tu = len(danh_sach_cac_tu)
    
    if so_luong_tu >= 2:
        return True   # Giữ lại câu này
    else:
        return False  # Loại bỏ câu này

def preprocess_data(input_file, output_file):
    print(f"[*] Đang đọc dữ liệu từ: {input_file}")
    
    if os.path.exists(input_file) == False:
        print(f"[Lỗi] Không tìm thấy file {input_file}. Hãy chạy file 1_data_labeling.py trước!")
        return
        
    df = pd.read_csv(input_file)
    so_luong_ban_dau = len(df)
    print(f"[*] Tổng số dòng dữ liệu ban đầu: {so_luong_ban_dau}")
    print("[*] Đang tiến hành làm sạch dữ liệu. Vui lòng đợi...\n")
    
    # BƯỚC 1: CHỮA BỆNH TRÙNG LẶP (DUPLICATED)
    # Lọc bỏ các dòng bình luận spam giống hệt nhau, chỉ giữ lại dòng xuất hiện đầu tiên
    df = df.drop_duplicates(subset=['Review'], keep='first')
    so_luong_sau_xoa_trung = len(df)
    print(f"[-] Đã xóa {so_luong_ban_dau - so_luong_sau_xoa_trung} dòng bình luận bị spam trùng lặp.")
    
    # BƯỚC 2: CHỮA BỆNH NHIỄU (NOISY) BẰNG NLP
    # Dùng hàm apply để cho toàn bộ cột Review chạy qua bộ lọc clean_text (xóa icon, link, teencode...)
    df['Cleaned_Review'] = df['Review'].apply(clean_text)
    
    # BƯỚC 3: CHỮA BỆNH THIẾU HỤT (MISSING)
    # Sau khi xóa link và icon, có những câu không còn chữ nào (trở thành chuỗi rỗng "")
    dieu_kien_khac_rong = (df['Cleaned_Review'] != "")
    df = df[dieu_kien_khac_rong]
    so_luong_sau_xoa_rong = len(df)
    print(f"[-] Đã xóa {so_luong_sau_xoa_trung - so_luong_sau_xoa_rong} dòng bị rỗng sau khi làm sạch.")
    
    # BƯỚC 4: CHỮA BỆNH VÔ NGHĨA (INVALID)
    # Lọc bỏ các câu quá ngắn, chỉ gõ 1 chữ cái lách luật
    dieu_kien_du_tu = df['Cleaned_Review'].apply(kiem_tra_du_so_luong_tu)
    df = df[dieu_kien_du_tu]
    so_luong_cuoi_cung = len(df)
    print(f"[-] Đã xóa {so_luong_sau_xoa_rong - so_luong_cuoi_cung} dòng vô nghĩa (chỉ có 1 chữ cái).")
    
    # BƯỚC 5: LƯU TRỮ VÀ KẾT THÚC
    print(f"\n[*] Dữ liệu sẵn sàng đưa vào AI (Model-Ready): {so_luong_cuoi_cung} câu bình luận chất lượng cao.")
    
    # Sắp xếp lại các cột cho đẹp: Giữ lại câu gốc, câu đã làm sạch và nhãn
    df = df[['Review', 'Cleaned_Review', 'Label']]
    
    # Kiểm tra thư mục và lưu ra file
    thu_muc_luu = os.path.dirname(output_file)
    if os.path.exists(thu_muc_luu) == False:
        os.makedirs(thu_muc_luu)
        
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"[+] Hoàn thành 100%! Đã lưu file chuẩn hóa tại: {output_file}")

if __name__ == "__main__":
    INPUT_PATH = "data/labeled_data.csv"
    OUTPUT_PATH = "data/clean_data.csv"
    
    preprocess_data(INPUT_PATH, OUTPUT_PATH)