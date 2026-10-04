import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score
from sklearn.manifold import TSNE
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
import skfuzzy as fuzz

file_name = 'country_wise_latest.csv'
print(f"Загрузка данных {file_name}...")
df_corona = pd.read_csv(file_name)

numeric_cols = df_corona.select_dtypes(include=[np.number]).columns
X_raw = df_corona[numeric_cols].copy()


X_raw = X_raw.replace([np.inf, -np.inf], np.nan).fillna(0)


scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_raw)


wcss = []
sil_scores = []
K_range = range(2, 11)

print("Обучение алгоритма для поиска оптимального числа кластеров...")
for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_scaled)
    wcss.append(kmeans.inertia_)
    sil_scores.append(silhouette_score(X_scaled, labels))


fig, ax = plt.subplots(1, 2, figsize=(12, 5))
ax[0].plot(K_range, wcss, marker='o', linestyle='--')
ax[0].set_title('Метод локтя (WCSS)')
ax[1].plot(K_range, sil_scores, marker='s', color='orange', linestyle='--')
ax[1].set_title('Коэффициент силуэта')
print("ЗАКРОЙТЕ ОКНО С ГРАФИКАМИ, ЧТОБЫ КОД ПОШЕЛ ДАЛЬШЕ!")
plt.savefig('elbow_silhouette.png')


optimal_k = 3


kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
kmeans_labels = kmeans.fit_predict(X_scaled)


cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
    X_scaled.T, c=optimal_k, m=2, error=0.005, maxiter=1000, init=None
)
fcm_labels = np.argmax(u, axis=0)


dbscan = DBSCAN(eps=0.5, min_samples=5)
dbscan_labels = dbscan.fit_predict(X_scaled)


Z = linkage(X_scaled, method='ward')
plt.figure(figsize=(10, 5))
dendrogram(Z, truncate_mode='lastp', p=30)
plt.title('Дендрограмма (Метод Уорда)')
print("ЗАКРОЙТЕ ДЕНДРОГРАММУ, ЧТОБЫ ПРОДОЛЖИТЬ!")
plt.savefig('dendrogram.png')


tsne = TSNE(n_components=2, perplexity=30, random_state=42)
X_tsne = tsne.fit_transform(X_scaled)

plt.figure(figsize=(8, 6))
sns.scatterplot(x=X_tsne[:, 0], y=X_tsne[:, 1], hue=kmeans_labels, palette='viridis', legend='full')
plt.title('t-SNE: Кластеры статистики COVID-19')
print("ЗАКРОЙТЕ ГРАФИК t-SNE ДЛЯ ВЫВОДА ПРОФИЛЕЙ В КОНСОЛЬ!")
plt.savefig('tsne.png')


df_corona['Cluster'] = kmeans_labels
profile = df_corona.groupby('Cluster')[numeric_cols].mean()
print("\n=== ПРОФИЛИ КЛАСТЕРОВ (Средние значения) ===")
print(profile)