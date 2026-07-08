import math
from collections import defaultdict

class CustomMultinomialNB:
    """
    Mô hình phân loại Multinomial Naive Bayes.
    Với cơ chế Cào bằng xác suất (Uniform Prior) để xử lý Dữ liệu Mất Cân Bằng.
    """
    def __init__(self, alpha=1.0, fit_prior=True):
        """
        Khởi tạo mô hình.
        
        Args:
            alpha (float): Hệ số làm trơn Laplace (Laplace smoothing) để tránh lỗi xác suất bằng 0.
            fit_prior (bool): Có học xác suất tiên nghiệm từ dữ liệu không?
                              - True (Mặc định): Học theo tỷ lệ thực tế (ví dụ 90% Khen - 10% Chê).
                              - False (Cào bằng): Giả định các lớp có tỷ lệ bằng nhau (50% Khen - 50% Chê).
                              => RẤT HỮU ÍCH KHI DỮ LIỆU BỊ MẤT CÂN BẰNG.
        """
        self.alpha = alpha
        self.fit_prior = fit_prior
        self.classes_ = []          # Danh sách các nhãn (ví dụ: [0, 1])
        self.class_log_prior_ = {}  # Xác suất tiên nghiệm của mỗi class (dạng Logarit)
        self.feature_log_prob_ = {} # Xác suất có điều kiện của từng từ vựng trong mỗi class (dạng Logarit)

    def fit(self, X, y):
        """
        Huấn luyện mô hình Naive Bayes.
        """
        n_samples = len(X)
        n_features = len(X[0])
        
        # 1. Thu thập các nhãn duy nhất
        self.classes_ = list(set(y))
        n_classes = len(self.classes_)
        
        # Biến phụ trợ để đếm
        class_doc_counts = defaultdict(int)                 # Số lượng câu của từng class
        feature_sums_by_class = defaultdict(lambda: [0.0] * n_features) # Tổng điểm TF-IDF của từng từ trong từng class
        
        # 2. Phân loại và tính tổng điểm đặc trưng (TF-IDF) cho từng nhóm nhãn
        for i in range(n_samples):
            label = y[i]
            class_doc_counts[label] += 1
            
            for j in range(n_features):
                feature_sums_by_class[label][j] += X[i][j]
                
        # 3. Tính toán Log Prior (Xác suất tiên nghiệm) và Log Likelihood (Xác suất có điều kiện)
        self.feature_log_prob_ = {}
        
        for label in self.classes_:
            # --- XỬ LÝ MẤT CÂN BẰNG BẰNG UNIFORM PRIOR ---
            if self.fit_prior:
                # Học theo tỷ lệ thực tế (Ví dụ: log(270/298))
                self.class_log_prior_[label] = math.log(class_doc_counts[label] / n_samples)
            else:
                # Cào bằng tỷ lệ (Ví dụ có 2 nhãn thì mỗi nhãn là 1/2 -> log(0.5))
                # Ép AI không được có định kiến ban đầu
                self.class_log_prior_[label] = math.log(1.0 / n_classes)
            
            # Tính tổng số điểm TF-IDF của tất cả các từ trong class này (dùng cho mẫu số)
            # Cộng thêm alpha * n_features để làm trơn (Laplace Smoothing)
            total_feature_sum = sum(feature_sums_by_class[label]) + (self.alpha * n_features)
            
            self.feature_log_prob_[label] = [0.0] * n_features
            for j in range(n_features):
                # Xác suất có điều kiện: P(Word_j | Class) 
                prob = (feature_sums_by_class[label][j] + self.alpha) / total_feature_sum
                # Lưu dưới dạng Logarit để tránh Underflow khi nhân các số quá nhỏ
                self.feature_log_prob_[label][j] = math.log(prob)
                
        return self

    def predict(self, X):
        """
        Dự đoán nhãn cho các mẫu dữ liệu mới.
        """
        predictions = []
        
        for i in range(len(X)):
            best_label = None
            max_log_prob = -float('inf')
            
            # Với mỗi câu, ta tính xác suất thuộc về từng class
            for label in self.classes_:
                # Bắt đầu với Log Prior: log(P(Class))
                log_prob = self.class_log_prior_[label]
                
                # Cộng dồn Log Likelihood của từng từ xuất hiện trong câu
                for j in range(len(X[i])):
                    if X[i][j] > 0: # Chỉ tính những từ thực sự có mặt trong câu để tối ưu tốc độ
                        log_prob += X[i][j] * self.feature_log_prob_[label][j]
                
                # Cập nhật nhãn có xác suất cao nhất
                if log_prob > max_log_prob:
                    max_log_prob = log_prob
                    best_label = label
                    
            predictions.append(best_label)
            
        return predictions