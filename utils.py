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
    if not isinstance(text, str):
        return ""

    # Bước 1: Đưa về chữ in thường
    text = text.lower()

    # Bước 2: Xử lý Text Icon truyền thống (<3, :), :( )
    text = text.replace("<3", " positive_icon ")
    text = text.replace(":)", " positive_icon ")
    text = text.replace(":(", " negative_icon ")
    text = text.replace(":v", " funny_icon ")

    # Bước 3: Bắt và dịch toàn bộ Emoji (😡, 🌞, 👍...) thành Text Token
    # Ví dụ: 😡 -> :enraged_face:
    text = emoji.demojize(text)
    # Xóa dấu ':' bao quanh token để nó trở thành một từ vựng bình thường
    text = text.replace(":", " ")

    # Bước 4: Làm sạch ký tự lạ, giữ lại chữ cái (cả tiếng Anh lẫn Việt) và khoảng trắng
    text = re.sub(r'[^a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ\s_]', ' ', text)

    # Bước 5: Chữa bệnh spam chữ cái kéo dài (ví dụ: đẹppppp -> đẹp)
    text = re.sub(r'([a-zà-ỹ])\1+', r'\1', text)

    # Bước 6: Thay thế Teencode và Lỗi chính tả
    danh_sach_tu = text.split()
    cau_da_sua = []
    for tu in danh_sach_tu:
        if tu in DANH_SACH_TEENCODE:
            cau_da_sua.append(DANH_SACH_TEENCODE[tu])
        else:
            cau_da_sua.append(tu)
    text = " ".join(cau_da_sua)
    
    # Ghép từ "không", "chưa", "chẳng" với từ ngay sau nó bằng dấu gạch dưới
    # Ví dụ: "không tốt" -> "không_tốt", "chưa đẹp" -> "chưa_đẹp"
    text = re.sub(r'\b(không|chưa|chẳng|chả)\s+([a-zà-ỹ]+)\b', r'\1_\2', text)

    # Bước 7: Tách từ ghép tiếng Việt (Gắn dấu gạch dưới)
    text = word_tokenize(text, format="text")

    # Bước 8: Lọc bỏ rác vô nghĩa (Stop Words)
    danh_sach_tu_sau_tach = text.split()
    cau_cuoi_cung = []
    for tu in danh_sach_tu_sau_tach:
        if tu not in STOP_WORDS:
            cau_cuoi_cung.append(tu)

    return " ".join(cau_cuoi_cung)