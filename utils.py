import re
from underthesea import word_tokenize

DANH_SACH_TEENCODE = {
    "khum": "không", "ko": "không", "k": "không", "hk": "không",
    "ok": "tốt", "okay": "tốt", "op": "tốt",
    "sp": "sản phẩm", "hàng": "sản phẩm",
    "dc": "được", "đc": "được",
    "r": "rồi", "rùi": "rồi",
    "mn": "mọi người", "shop": "cửa hàng",
    "iu": "yêu", "vđ": "vấn đề",
    "qa": "quá", "wa": "quá", "chất": "chất lượng", "mún": "muốn"
}

# Tập từ dừng tiếng Việt (Những từ nối vô nghĩa, xuất hiện nhiều nhưng không mang cảm xúc)
STOP_WORDS = set(["là", "và", "của", "những", "các", "thì", "mà", "nhưng", "để", "này", "kia", "đó", "ở", "có", "bị", "được", "với", "cho", "nha", "ạ"])

def clean_text(text):
    if isinstance(text, str) == False:
        return ""
        
    text = text.lower()
    
    # 1. Thay thế icon cảm xúc
    text = text.replace("<3", " yêu ")
    text = text.replace(":)", " tốt ")
    text = text.replace(":(", " tệ ")
    text = text.replace(":v", " vui ")
    
    # 2. Xóa ký tự lặp (đẹppppp -> đẹp)
    text = re.sub(r'([a-z])\1+', r'\1', text)
    
    # 3. Xóa ký tự đặc biệt
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # 4. Dịch Teencode
    danh_sach_tu = text.split()
    danh_sach_tu_sau_sua = []
    
    for tu in danh_sach_tu:
        if tu in DANH_SACH_TEENCODE:
            danh_sach_tu_sau_sua.append(DANH_SACH_TEENCODE[tu])
        else:
            danh_sach_tu_sau_sua.append(tu)
            
    cau_da_dich = " ".join(danh_sach_tu_sau_sua)
    
    # 5. TÁCH TỪ TIẾNG VIỆT (Ví dụ: "sản phẩm" -> "sản_phẩm")
    cau_da_tach_tu = word_tokenize(cau_da_dich, format="text")
    
    # 6. LỌC TỪ DỪNG (Stop words)
    danh_sach_tu_cuoi = []
    for tu in cau_da_tach_tu.split():
        if tu not in STOP_WORDS:
            danh_sach_tu_cuoi.append(tu)
            
    # 7. Ghép lại thành câu hoàn chỉnh
    cau_hoan_chinh = " ".join(danh_sach_tu_cuoi)
    cau_hoan_chinh = re.sub(r'\s+', ' ', cau_hoan_chinh).strip()
    
    return cau_hoan_chinh

# if __name__ == "__main__":
#     cau_test = "áo đẹp lắm nha shop iu <3!!! sp ok khum vđ gì đâu mn ạ"
#     print("Kết quả NLP:", clean_text(cau_test))
    # Bạn sẽ thấy "sản phẩm" được nối bằng dấu gạch dưới, và các từ "nha", "ạ" bị xóa đi.