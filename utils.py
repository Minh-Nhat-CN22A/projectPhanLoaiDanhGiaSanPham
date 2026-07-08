import re
from underthesea import word_tokenize
import emoji

# Nối các từ ghép bằng dấu gạch dưới "_"
DANH_SACH_TEENCODE = {
    # Bổ sung từ WordCloud
    "khum": "không", "ko": "không", "k": "không", "hk": "không",
    "ok": "tốt", "okay": "tốt", "op": "tốt",
    "sp": "sản_phẩm", "hàng": "sản_phẩm",
    "dc": "được", "đc": "được",
    "r": "rồi", "rùi": "rồi",
    "mn": "mọi_người", "shop": "cửa_hàng",
    "iu": "yêu", "vđ": "vấn_đề",
    "qa": "quá", "wa": "quá", 
    "chất": "chất_lượng", "mún": "muốn",
    "lun": "luôn",
    "mạc": "mặc", "dỏm": "kém", "nhìu": "nhiều"
}

# Bổ sung từ dừng chuyên ngành thời trang và từ đệm
STOP_WORDS = set([
    # Từ nối ngữ pháp
    "là", "và", "của", "những", "các", "thì", "mà", "nhưng", "để",
    "này", "kia", "đó", "ở", "có", "bị", "được", "với", "cho", "từ",
    "rồi", "lần",

    # Từ đệm / Từ cảm thán
    "nha", "ạ", "nhé", "nè", "đi", "vậy", "ơi", "luôn", "mình",

    # Từ chỉ đối tượng / người (ít mang ý nghĩa cảm xúc)
    "mọi_người",

    # Từ dừng chuyên ngành (Domain stopwords)
    "áo", "quần", "sản_phẩm", "sản", "phẩm",
    "cửa_hàng", "cửa", "hàng", "shop"
])

def clean_text(text):
    """
    Tiền xử lý và chuẩn hóa văn bản tiếng Việt cho mô hình Machine Learning.
    
    Args:
        text (str): Chuỗi văn bản thô đầu vào.
        
    Returns:
        str: Chuỗi văn bản đã được làm sạch, tách từ và chuẩn hóa.
    """
    if not isinstance(text, str):
        return ""

    # 1. Chuyển đổi về chữ in thường
    text = text.lower()

    # 2. Xử lý biểu tượng cảm xúc (Emoticons) thành các token mang sắc thái
    # Mặt cười / Tích cực: <3 | :) :)) =) ;) :] :-) | ^^ ^_^ ^-^ | :D =D
    text = re.sub(
        r'<3|[:=;]-?[\)\]]+|\^[-_]?\^|[:=]-?[dD]\b',
        ' tích_cực ', text, flags=re.IGNORECASE
    )
    
    # Mặt buồn / Tiêu cực: :( :(( =( ;( :[ :-( | T_T T.T TT | :'(
    text = re.sub(
        r"[:=;]-?[\(\[]+|:'\(|t[_.]t",
        ' tiêu_cực ', text, flags=re.IGNORECASE
    )
    
    # Mặt troll / Hài hước: :v :3 XD
    text = re.sub(
        r':v|:3|xd\b',
        ' hài_hước ', text, flags=re.IGNORECASE
    )

    # 3. Chuyển hóa Emoji đồ họa thành văn bản (VD: 👍 -> thumbs_up)
    text = emoji.demojize(text)
    text = text.replace(":", " ")

    # 4. Loại bỏ ký tự đặc biệt và chữ số (chỉ giữ lại chữ cái và khoảng trắng)
    text = re.sub(r'[^\w\s_]', ' ', text) 
    text = re.sub(r'\d+', ' ', text)

    # 5. Khắc phục lỗi lặp ký tự (VD: đẹppppp -> đẹp)
    text = re.sub(r'([a-zà-ỹ])\1+', r'\1', text)

    # 6. Chuẩn hóa Teencode dựa trên từ điển cấu hình
    danh_sach_tu = text.split()
    cau_da_sua = []
    
    if 'DANH_SACH_TEENCODE' in globals():
        for tu in danh_sach_tu:
            cau_da_sua.append(DANH_SACH_TEENCODE.get(tu, tu))
        text = " ".join(cau_da_sua)
    
    # 7. Xử lý từ phủ định (Ghép từ phủ định với từ mô tả đứng ngay sau)
    # VD: "không tốt" -> "không_tốt", "chưa đẹp" -> "chưa_đẹp"
    text = re.sub(r'\b(không|chưa|chẳng|chả)\s+(\w+)\b', r'\1_\2', text)

    # 8. Tách từ tiếng Việt (Word Segmentation) bằng thư viện underthesea
    text = word_tokenize(text, format="text")

    # 9. Loại bỏ từ dừng (Stopwords)
    if 'STOP_WORDS' in globals():
        danh_sach_tu_sau_tach = text.split()
        cau_cuoi_cung = [tu for tu in danh_sach_tu_sau_tach if tu not in STOP_WORDS]
        text = " ".join(cau_cuoi_cung)

    # 10. Loại bỏ khoảng trắng thừa và hoàn tất
    text = re.sub(r'\s+', ' ', text)
    return text.strip()