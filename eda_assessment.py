import pandas as pd
import matplotlib.pyplot as plt
import os
from wordcloud import WordCloud

def count_words(text):
    """Đếm số lượng từ trong một chuỗi văn bản."""
    return len(str(text).split())

def generate_eda_report(file_path):
    """
    Thực hiện Khám phá Dữ liệu (EDA) và Đánh giá Chất lượng Dữ liệu (Data Quality Assessment).
    Xuất các biểu đồ trực quan và báo cáo thống kê ra console.
    """
    print("="*70)
    print(" BÁO CÁO EDA & ĐÁNH GIÁ CHẤT LƯỢNG DỮ LIỆU ".center(70, "="))
    print("="*70)
    print(f"[INFO] File nguồn xử lý: {os.path.basename(file_path)}")
    
    if not os.path.exists(file_path):
        print(f"[ERROR] Không tìm thấy file dữ liệu tại: {file_path}. Hủy bỏ quá trình EDA.")
        return

    df = pd.read_csv(file_path)
    total_records = len(df)
    print(f"[INFO] Tổng số lượng bản ghi (records): {total_records}")
    
    output_dir = "data/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # ---------------------------------------------------------
    # 1. PHÂN PHỐI NHÃN (CLASS DISTRIBUTION)
    # ---------------------------------------------------------
    print("\n[REPORT] 1. Thống kê phân phối nhãn dữ liệu:")
    label_distribution = df['Label'].value_counts()
    print(label_distribution.to_string())
    
    plt.figure(figsize=(6, 4))
    label_distribution.plot(kind='bar', color=['#4CAF50', '#F44336'])
    plt.title('Phân phối Cảm xúc Tích cực (1) vs Tiêu cực (0)')
    plt.xlabel('Nhãn dữ liệu (Label)')
    plt.ylabel('Số lượng bản ghi')
    plt.xticks(rotation=0)
    
    bar_chart_path = os.path.join(output_dir, "label_distribution.png")
    plt.savefig(bar_chart_path)
    plt.close()
    print(f"[SUCCESS] Đã xuất biểu đồ phân phối nhãn tại: {bar_chart_path}")
    
    # ---------------------------------------------------------
    # 2. PHÂN TÍCH TỪ VỰNG (WORDCLOUD)
    # ---------------------------------------------------------
    print("\n[REPORT] 2. Phân tích Tần suất Từ vựng (WordCloud)...")
    
    # Ưu tiên dùng cột 'Cleaned_Review' nếu có, không thì dùng 'Review'
    text_column = 'Cleaned_Review' if 'Cleaned_Review' in df.columns else 'Review'
    print(f"[INFO] Trích xuất đặc trưng từ cột: '{text_column}'")
    
    positive_text = " ".join(df[df['Label'] == 1][text_column].astype(str))
    negative_text = " ".join(df[df['Label'] == 0][text_column].astype(str))
    
    if len(positive_text) > 0:
        wc_pos = WordCloud(width=800, height=400, background_color='white', colormap='Greens').generate(positive_text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wc_pos, interpolation='bilinear')
        plt.axis('off')
        wc_pos_path = os.path.join(output_dir, "wordcloud_positive.png")
        plt.savefig(wc_pos_path)
        plt.close()
        print(f"[SUCCESS] Đã xuất WordCloud Tích cực tại: {wc_pos_path}")

    if len(negative_text) > 0:
        wc_neg = WordCloud(width=800, height=400, background_color='black', colormap='Reds').generate(negative_text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wc_neg, interpolation='bilinear')
        plt.axis('off')
        wc_neg_path = os.path.join(output_dir, "wordcloud_negative.png")
        plt.savefig(wc_neg_path)
        plt.close()
        print(f"[SUCCESS] Đã xuất WordCloud Tiêu cực tại: {wc_neg_path}")

    # ---------------------------------------------------------
    # 3. THỐNG KÊ ĐỘ DÀI VĂN BẢN (TEXT LENGTH)
    # ---------------------------------------------------------
    df['Word_Count'] = df[text_column].apply(count_words)
    print("\n[REPORT] 3. Thống kê độ dài văn bản (theo số lượng từ):")
    print(f"  - Độ dài tối thiểu (Min) : {df['Word_Count'].min()} từ/câu")
    print(f"  - Độ dài tối đa (Max)    : {df['Word_Count'].max()} từ/câu")
    print(f"  - Độ dài trung bình (Avg): {round(df['Word_Count'].mean(), 1)} từ/câu")
    
    print("\n" + "="*70)
    print(" TỔNG KẾT ĐÁNH GIÁ CHẤT LƯỢNG DỮ LIỆU (DATA QUALITY METRICS) ".center(70, "="))
    print("="*70)
    
    missing_rows = df[text_column].isnull().sum()
    duplicated_rows = df.duplicated(subset=[text_column]).sum()
    invalid_rows = len(df[df['Word_Count'] < 2])
    
    print(f"[METRIC] Số lượng bản ghi rỗng (Missing Values)     : {missing_rows}")
    print(f"[METRIC] Số lượng bản ghi trùng lặp (Duplicated)    : {duplicated_rows}")
    print(f"[METRIC] Số lượng bản ghi quá ngắn (< 2 từ/Invalid) : {invalid_rows}")
    print("\n[INFO] Hoàn tất quá trình Khám phá và Đánh giá Dữ liệu.")
    print("="*70)

if __name__ == "__main__":
    DATA_FILE_PATH = "data/clean_data.csv" 
    generate_eda_report(DATA_FILE_PATH)