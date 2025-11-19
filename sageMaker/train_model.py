# train_model.py
from sklearn.linear_model import LinearRegression
import joblib
import numpy as np

# ===== 1. ダミーデータ作成 =====
# 例: CM本数(spots) → ROI
# 現場ではここを実データのCSV読み込みなどに差し替え
X = np.array([[10], [20], [30], [40], [50]])
y = np.array([0.05, 0.10, 0.23, 0.30, 0.45])

# ===== 2. モデルを学習 =====
model = LinearRegression()
model.fit(X, y)

# ===== 3. 保存 =====
joblib.dump(model, "model.joblib")

print("✅ model.joblib を出力しました")
