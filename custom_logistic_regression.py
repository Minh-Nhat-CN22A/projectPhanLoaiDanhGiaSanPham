import math

class CustomLogisticRegression:
    """
    Mô hình phân loại Logistic Regression bằng Gradient Descent.
    Với cơ chế Trọng số lớp (Class Weights) để xử lý Dữ liệu Mất Cân Bằng
    """
    def __init__(self, learning_rate=0.1, num_iterations=500, class_weight=None):
        """
        Khởi tạo mô hình.
        
        Args:
            learning_rate (float): Tốc độ học (bước nhảy của Gradient Descent).
            num_iterations (int): Số lượng vòng lặp huấn luyện.
            class_weight (dict): Bảng trọng số phạt cho từng lớp. Ví dụ: {0: 10.0, 1: 1.0}
                                 Giúp giải quyết triệt để lỗi AI "lười biếng" do mất cân bằng dữ liệu.
        """
        self.learning_rate = learning_rate
        self.num_iterations = num_iterations
        self.class_weight = class_weight
        self.weights = []
        self.bias = 0.0

    def _sigmoid(self, z):
        """Hàm Sigmoid ép giá trị liên tục về khoảng xác suất (0, 1)."""
        # Giới hạn z để tránh lỗi tràn số (overflow) khi tính e^(-z)
        z = max(min(z, 250), -250)
        return 1.0 / (1.0 + math.exp(-z))

    def fit(self, X, y):
        """
        Huấn luyện mô hình tìm kiếm Trọng số (Weights) và Độ lệch (Bias) tốt nhất.
        """
        n_samples = len(X)
        n_features = len(X[0])
        
        # Khởi tạo trọng số và độ lệch bằng 0
        self.weights = [0.0] * n_features
        self.bias = 0.0
        
        # Khởi tạo mức phạt cho từng lớp (Mặc định là 1.0 - Không phạt thêm)
        w0 = self.class_weight.get(0, 1.0) if self.class_weight else 1.0
        w1 = self.class_weight.get(1, 1.0) if self.class_weight else 1.0
        
        for _ in range(self.num_iterations):
            dw = [0.0] * n_features
            db = 0.0
            
            # Tính toán Gradient cho toàn bộ tập dữ liệu (Batch Gradient Descent)
            for i in range(n_samples):
                # 1. Tính phương trình đường thẳng: z = w*x + b
                z = self.bias
                for j in range(n_features):
                    if X[i][j] > 0: # Bỏ qua các giá trị 0 để tối ưu tốc độ
                        z += self.weights[j] * X[i][j]
                
                # 2. Áp dụng hàm Sigmoid để ra dự đoán (xác suất)
                y_pred = self._sigmoid(z)
                
                # 3. Tính sai số cơ bản
                dz = y_pred - y[i]
                
                # --- ÁP DỤNG TRỌNG SỐ LỚP (CLASS WEIGHTS) ---
                # Nhân sai số với mức phạt tương ứng của lớp thực tế.
                # Nếu đoán sai câu Tiêu cực (nhãn 0), mức phạt dz sẽ bị nhân gấp nhiều lần,
                # ép đường Gradient phải rẽ ngoặt để sửa lỗi cho lớp thiểu số.
                weight_for_this_sample = w1 if y[i] == 1 else w0
                dz = dz * weight_for_this_sample
                
                # 4. Tích lũy Gradient cho Weights và Bias
                for j in range(n_features):
                    if X[i][j] > 0:
                        dw[j] += dz * X[i][j]
                db += dz
                
            # Cập nhật Weights và Bias sau mỗi vòng lặp
            for j in range(n_features):
                self.weights[j] -= self.learning_rate * (dw[j] / n_samples)
            self.bias -= self.learning_rate * (db / n_samples)
            
        return self

    def predict(self, X):
        """
        Dự đoán nhãn cho mẫu dữ liệu mới.
        """
        predictions = []
        for i in range(len(X)):
            z = self.bias
            for j in range(len(X[i])):
                if X[i][j] > 0:
                    z += self.weights[j] * X[i][j]
            
            y_pred = self._sigmoid(z)
            # Luật phân loại: Nếu xác suất >= 50% thì là Tích cực (1), ngược lại là Tiêu cực (0)
            predictions.append(1 if y_pred >= 0.5 else 0)
            
        return predictions