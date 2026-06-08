import pandas as pd
import os

# --- HÀM PHỤ TRỢ: CHUYỂN SỐ SAO THÀNH NHÃN ---
# Viết rõ ràng bằng if-else thay vì dùng cú pháp viết tắt (lambda)
def chuyen_sao_thanh_nhan(so_sao):
    if so_sao >= 4:
        return 1  # 4 và 5 sao là Tích cực
    else:
        return 0  # 1 và 2 sao là Tiêu cực

# --- CHƯƠNG TRÌNH CHÍNH ---
def label_data(input_file, output_file):
    print(f"[*] Đang đọc dữ liệu từ: {input_file}...")
    
    # Kiểm tra xem file có tồn tại không
    if os.path.exists(input_file) == False:
        print(f"[Lỗi] Không tìm thấy file {input_file}.")
        return
        
    # Đọc file dữ liệu thô
    df = pd.read_csv(input_file)
    print(f"[*] Tổng số bình luận thô ban đầu: {len(df)} dòng")
    
    # Bước 1: Xóa các dòng bị trống dữ liệu
    df = df.dropna(subset=['Review', 'Rating'])
    
    # Bước 2: Lọc bỏ các đánh giá 3 sao (Trung lập)
    # Viết rõ điều kiện ra một biến riêng cho dễ đọc
    dieu_kien_khac_3_sao = (df['Rating'] != 3)
    df = df[dieu_kien_khac_3_sao] 
    
    # Bước 3: Gán nhãn bằng cách gọi hàm if-else đã định nghĩa ở trên
    df['Label'] = df['Rating'].apply(chuyen_sao_thanh_nhan)
    
    # Bước 4: Lưu file dữ liệu đã gán nhãn
    # Tạo thư mục nếu chưa có
    thu_muc_luu = os.path.dirname(output_file)
    if os.path.exists(thu_muc_luu) == False:
        os.makedirs(thu_muc_luu)
        
    df.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"[+] Đã gán nhãn thành công! Dữ liệu lưu tại: {output_file}")
    print("-" * 40)
    print("📊 THỐNG KÊ PHÂN BỐ NHÃN DỮ LIỆU:")
    print("Tổng số câu Tích cực (1):", len(df[df['Label'] == 1]))
    print("Tổng số câu Tiêu cực (0):", len(df[df['Label'] == 0]))
    print("-" * 40)

# Khởi chạy chương trình
if __name__ == "__main__":
    INPUT_PATH = "data/raw_data.csv"
    OUTPUT_PATH = "data/labeled_data.csv"
    
    label_data(INPUT_PATH, OUTPUT_PATH)