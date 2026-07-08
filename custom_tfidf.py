import math
from collections import Counter

class CustomTfidfVectorizer:
    """
    TF-IDF (Term Frequency-Inverse Document Frequency).
    Chuyển đổi một tập hợp các tài liệu văn bản thành ma trận đặc trưng TF-IDF.
    """
    def __init__(self):
        self.vocab = {}         # Từ điển ánh xạ: Từ vựng -> Chỉ số cột
        self.idf_ = {}          # Lưu giá trị IDF của từng từ
        self.feature_names = [] # Danh sách từ vựng theo thứ tự từ điển

    def fit(self, corpus):
        """
        Học từ vựng và tính toán chỉ số IDF từ tập dữ liệu huấn luyện.
        
        Args:
            corpus (list of str): Danh sách các văn bản đầu vào.
            
        Returns:
            self: Đối tượng vectorizer đã được huấn luyện.
        """
        N = len(corpus)
        df = Counter()

        # 1. Tính Document Frequency (DF)
        for doc in corpus:
            words_in_doc = set(doc.split())
            for word in words_in_doc:
                df[word] += 1

        # 2. Xây dựng bộ từ điển (Vocabulary)
        self.feature_names = sorted(list(df.keys()))
        self.vocab = {word: idx for idx, word in enumerate(self.feature_names)}

        # 3. Tính toán Inverse Document Frequency (IDF) có áp dụng smoothing
        self.idf_ = {}
        for word, idx in self.vocab.items():
            doc_freq = df[word]
            # Công thức Smooth IDF: ln((N + 1) / (DF + 1)) + 1
            idf_val = math.log((N + 1) / (doc_freq + 1)) + 1
            self.idf_[idx] = idf_val

        return self

    def transform(self, corpus):
        """
        Biến đổi văn bản đầu vào thành ma trận TF-IDF dựa trên từ điển đã được huấn luyện.
        
        Args:
            corpus (list of str): Danh sách các văn bản cần biến đổi.
            
        Returns:
            list of list of float: Ma trận đặc trưng TF-IDF.
        """
        matrix = []
        vocab_size = len(self.vocab)
        
        for doc in corpus:
            words = doc.split()
            term_counts = Counter(words)
            doc_vector = [0.0] * vocab_size

            # 4. Tính toán giá trị TF-IDF cục bộ
            for word, count in term_counts.items():
                if word in self.vocab:
                    idx = self.vocab[word]
                    tf = count
                    doc_vector[idx] = tf * self.idf_[idx]

            # 5. Áp dụng chuẩn hóa L2 (L2 Normalization) cho từng vector
            norm = math.sqrt(sum(val ** 2 for val in doc_vector))
            if norm > 0:
                doc_vector = [val / norm for val in doc_vector]

            matrix.append(doc_vector)

        return matrix

    def fit_transform(self, corpus):
        """
        Thực hiện tuần tự quá trình học từ vựng và biến đổi tập dữ liệu huấn luyện.
        
        Args:
            corpus (list of str): Danh sách các văn bản đầu vào.
            
        Returns:
            list of list of float: Ma trận đặc trưng TF-IDF.
        """
        self.fit(corpus)
        return self.transform(corpus)