import streamlit as st
import joblib
import os
import pandas as pd
# Import hàm làm sạch dữ liệu từ file utils
from utils import clean_text 

# Cấu hình thẻ trình duyệt và layout
st.set_page_config(page_title="AI Sentiment Analysis", page_icon="💡", layout="centered")

# Hàm tải mô hình (Dùng cache để không phải load lại file .pkl mỗi lần gõ chữ)
@st.cache_resource
def load_models():
    thu_muc_luu = "saved_models"
    vectorizer_path = os.path.join(thu_muc_luu, "tfidf_vectorizer.pkl")
    model_path = os.path.join(thu_muc_luu, "sentiment_model.pkl")
    
    if os.path.exists(vectorizer_path) and os.path.exists(model_path):
        vectorizer = joblib.load(vectorizer_path)
        model = joblib.load(model_path)
        return vectorizer, model
    else:
        return None, None

# 1. TIÊU ĐỀ VÀ MÔ TẢ
st.title("💡 Hệ thống AI Phân tích Cảm xúc Bình luận")
st.markdown("""
    Chào mừng bạn đến với hệ thống AI tự động phân tích cảm xúc bình luận của khách hàng.
    Hãy nhập một bình luận bất kỳ phía dưới để xem AI dự đoán nhé!
""")

# Load bộ não AI
vectorizer, model = load_models()

if model is None:
    st.error("⚠️ Không tìm thấy file mô hình! Hãy chắc chắn bạn đã chạy file train_model.ipynb để tạo thư mục saved_models.")
else:
    # 2. Ô NHẬP TEXT
    user_input = st.text_area("✍️ Nhập bình luận của khách hàng vào đây:", height=100, placeholder="Ví dụ: Áo đẹp lắm shop ơi, giao hàng nhanh...")
    
    # 3. NÚT BẤM DỰ ĐOÁN
    if st.button("🚀 Phân tích ngay", use_container_width=True):
        if user_input.strip() == "":
            st.warning("Vui lòng nhập bình luận trước khi phân tích!")
        else:
            with st.spinner("AI đang suy nghĩ..."):
                # --- PHẦN TÍCH HỢP LOGIC AI ---
                
                # Bước A: Làm sạch dữ liệu hệt như lúc huấn luyện
                cleaned_input = clean_text(user_input)
                
                if cleaned_input.strip() == "":
                    st.info("Bình luận này chỉ chứa icon vô nghĩa hoặc stop words, không đủ dữ kiện để AI phán đoán.")
                else:
                    # Bước B: Biến chữ thành Ma trận số (TF-IDF)
                    input_vector = vectorizer.transform([cleaned_input])
                    
                    # Bước C: AI đưa ra dự đoán
                    prediction = model.predict(input_vector)[0]
                    # Lấy thêm xác suất chắc chắn của AI (Tùy chọn cho sinh động)
                    probabilities = model.predict_proba(input_vector)[0]
                    confidence = max(probabilities) * 100
                    
                    # 4. VÙNG HIỂN THỊ KẾT QUẢ
                    st.markdown("### 📊 Kết quả phân tích:")
                    
                    if prediction == 1:
                        st.success(f"**TÍCH CỰC** (Độ tự tin: {confidence:.2f}%) 💖")
                        st.balloons() # Hiệu ứng bóng bay chúc mừng
                    else:
                        st.error(f"**TIÊU CỰC** (Độ tự tin: {confidence:.2f}%) 💔")
                        
                    # Hiển thị thêm góc nhìn của máy tính
                    with st.expander("🤖 Góc nhìn của AI (Dữ liệu đã qua xử lý)"):
                        st.write(f"- **Văn bản sau khi làm sạch (utils.py):** `{cleaned_input}`")
                        
                        # In thử các từ khóa được TF-IDF bắt trọng số
                        df_tfidf = pd.DataFrame(input_vector.toarray(), columns=vectorizer.get_feature_names_out())
                        words_caught = df_tfidf.loc[:, (df_tfidf != 0).any(axis=0)]
                        st.write("- **Các từ khóa được AI chấm điểm:**")
                        st.dataframe(words_caught)