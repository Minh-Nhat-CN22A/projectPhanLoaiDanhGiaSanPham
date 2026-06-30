import pandas as pd
import matplotlib.pyplot as plt
import os
from wordcloud import WordCloud

def dem_so_tu(van_ban):
    chuoi_van_ban = str(van_ban)
    danh_sach_tu = chuoi_van_ban.split()
    return len(danh_sach_tu)

def thuc_hien_buoc_2_va_3(duong_dan_file):
    print("="*60)
    print(f"BƯỚC 2 & 3: ĐÁNH GIÁ CHẤT LƯỢNG TRÊN FILE: {os.path.basename(duong_dan_file)}")
    print("="*60)
    
    if not os.path.exists(duong_dan_file):
        print(f"[Lỗi Hệ Thống] Không tìm thấy {duong_dan_file}. Quá trình Profiling thất bại!")
        return

    df = pd.read_csv(duong_dan_file)
    tong_so_dong = len(df)
    print(f"[*] Tổng số lượng mẫu dữ liệu đầu vào: {tong_so_dong} dòng")
    
    thu_muc_anh = "data/"
    if not os.path.exists(thu_muc_anh):
        os.makedirs(thu_muc_anh)
        
    # ---------------------------------------------------------
    # 1. HỒ SƠ NHÃN & VẼ BIỂU ĐỒ CỘT
    # ---------------------------------------------------------
    print("\n[Hồ sơ 1] Phân phối Tích cực (1) / Tiêu cực (0):")
    phan_phoi_nhan = df['Label'].value_counts()
    print(phan_phoi_nhan)
    
    plt.figure(figsize=(6, 4))
    phan_phoi_nhan.plot(kind='bar', color=['#4CAF50', '#F44336'])
    plt.title('Phân phối Bình luận Tích cực vs Tiêu cực')
    plt.xlabel('Nhãn (1: Tích cực, 0: Tiêu cực)')
    plt.ylabel('Số lượng bình luận')
    plt.xticks(rotation=0)
    
    duong_dan_anh_bar = os.path.join(thu_muc_anh, "label_distribution.png")
    plt.savefig(duong_dan_anh_bar)
    plt.close()
    print(f" -> [+] Đã xuất biểu đồ phân phối: {duong_dan_anh_bar}")
    
    # ---------------------------------------------------------
    # 2. HỒ SƠ TỪ VỰNG & VẼ WORDCLOUD
    # ---------------------------------------------------------
    print("\n[Hồ sơ 2] Đang vẽ Đám mây từ vựng (WordCloud)...")
    
    # Ưu tiên dùng cột 'Cleaned_Review' nếu có, không thì dùng 'Review'
    cot_ve_wordcloud = 'Cleaned_Review' if 'Cleaned_Review' in df.columns else 'Review'
    print(f"[*] Hệ thống đang trích xuất từ vựng từ cột: '{cot_ve_wordcloud}'")
    
    van_ban_tich_cuc = " ".join(df[df['Label'] == 1][cot_ve_wordcloud].astype(str))
    van_ban_tieu_cuc = " ".join(df[df['Label'] == 0][cot_ve_wordcloud].astype(str))
    
    if len(van_ban_tich_cuc) > 0:
        wc_tich_cuc = WordCloud(width=800, height=400, background_color='white', colormap='Greens').generate(van_ban_tich_cuc)
        plt.figure(figsize=(10, 5))
        plt.imshow(wc_tich_cuc, interpolation='bilinear')
        plt.axis('off')
        duong_dan_wc_pos = os.path.join(thu_muc_anh, "wordcloud_tich_cuc.png")
        plt.savefig(duong_dan_wc_pos)
        plt.close()
        print(f" -> [+] Đã xuất WordCloud Tích cực: {duong_dan_wc_pos}")

    if len(van_ban_tieu_cuc) > 0:
        wc_tieu_cuc = WordCloud(width=800, height=400, background_color='black', colormap='Reds').generate(van_ban_tieu_cuc)
        plt.figure(figsize=(10, 5))
        plt.imshow(wc_tieu_cuc, interpolation='bilinear')
        plt.axis('off')
        duong_dan_wc_neg = os.path.join(thu_muc_anh, "wordcloud_tieu_cuc.png")
        plt.savefig(duong_dan_wc_neg)
        plt.close()
        print(f" -> [+] Đã xuất WordCloud Tiêu cực: {duong_dan_wc_neg}")

    # ---------------------------------------------------------
    # 3. HỒ SƠ CHIỀU DÀI CÂU
    # ---------------------------------------------------------
    df['So_Tu'] = df[cot_ve_wordcloud].apply(dem_so_tu)
    print("\n[Hồ sơ 3] Thống kê số lượng từ trong một câu bình luận:")
    print(f"- Chiều dài tối thiểu (Min): {df['So_Tu'].min()} từ")
    print(f"- Chiều dài tối đa (Max): {df['So_Tu'].max()} từ")
    print(f"- Chiều dài trung bình (Mean): {round(df['So_Tu'].mean(), 1)} từ/câu")
    
    print("\n" + "="*60)
    print("BƯỚC 3: DATA QUALITY ASSESSMENT (ĐÁNH GIÁ CHẤT LƯỢNG)")
    print("="*60)
    
    so_dong_trong = df[cot_ve_wordcloud].isnull().sum()
    so_dong_trung = df.duplicated(subset=[cot_ve_wordcloud]).sum()
    so_dong_vo_nghia = len(df[df['So_Tu'] < 2])
    
    print(f"[Cảnh báo - Missing] Số lượng dòng rỗng (NaN): {so_dong_trong} dòng")
    print(f"[Cảnh báo - Duplicated] Số lượng dòng trùng lặp: {so_dong_trung} dòng")
    print(f"[Cảnh báo - Invalid] Số lượng dòng < 2 từ (Vô nghĩa): {so_dong_vo_nghia} dòng")
    print("\n=> KIỂM TRA HOÀN TẤT.")
    print("="*60)

if __name__ == "__main__":
    # ĐỂ XEM KẾT QUẢ ĐÃ LÀM SẠCH, HÃY TRUYỀN VÀO FILE 'clean_data.csv'
    FILE_KHOI_CHAY = "data/clean_data.csv" 
    thuc_hien_buoc_2_va_3(FILE_KHOI_CHAY)