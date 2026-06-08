import re
from underthesea import word_tokenize

# Khởi tạo một danh sách các từ dừng (stop words) tiếng Việt cơ bản
# Bạn có thể bổ sung thêm các từ vô nghĩa khác vào danh sách này
STOP_WORDS = set(["là", "và", "của", "những", "các", "thì", "mà", "nhưng", "để", "này", "kia", "đó"])

def clean_text(text):
    if not isinstance(text, str):
        return ""
        
    # 1. Đưa về chữ thường
    text = text.lower()
    
    # 2. Xóa các ký tự đặc biệt, icon, dấu câu (chỉ giữ lại chữ cái và số)
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # 3. Xóa khoảng trắng thừa
    text = re.sub(r'\s+', ' ', text).strip()
    
    # 4. Tách từ tiếng Việt bằng underthesea (VD: "sản phẩm" -> "sản_phẩm")
    tokens = word_tokenize(text, format="text").split()
    
    # 5. Lọc bỏ các từ dừng (Stop words)
    filtered_tokens = [word for word in tokens if word not in STOP_WORDS]
    
    # 6. Ghép lại thành chuỗi
    return " ".join(filtered_tokens)

# --- Test thử hàm ---
if __name__ == "__main__":
    cau_mau = "Sản phẩm này tuyệt vời quá shop ơi!!! 😊 Giao hàng Rất nhanh luôn 10 điểm đuyyy"
    print("Câu gốc:", cau_mau)
    print("Sau xử lý:", clean_text(cau_mau))