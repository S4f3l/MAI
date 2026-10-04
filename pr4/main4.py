import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

file_name = 'spambase.data'
print(f"Загрузка локального файла {file_name}...")


df_labeled = pd.read_csv(file_name, header=None)


target_col = df_labeled.columns[-1]
print(f"В качестве целевой переменной (меток классов) выбрана последняя колонка: {target_col}")


y_true = df_labeled[target_col].values
X_raw = df_labeled.drop(columns=[target_col])


print("Очистка данных и масштабирование...")

X_raw = X_raw.fillna(X_raw.mean())


scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_raw)


n_clusters = len(np.unique(y_true))
print(f"Истинное количество классов в файле (Спам и Не Спам): {n_clusters}")


kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
kmeans_labels = kmeans.fit_predict(X_scaled)


ari_score = adjusted_rand_score(y_true, kmeans_labels)

print("\n=== РЕЗУЛЬТАТЫ ОЦЕНКИ КАЧЕСТВА ===")
print(f"Скорректированный индекс Рэнда (ARI): {ari_score:.4f}")