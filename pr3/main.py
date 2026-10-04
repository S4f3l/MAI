import pandas as pd
import numpy as np
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt
import seaborn as sns

np.random.seed(42)
tf.random.set_seed(42)

nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

data = pd.DataFrame({
    'text': [
        'I love this movie, it is amazing!',
        'Terrible film, waste of time.',
        'Absolutely fantastic performance.',
        'Worst movie ever, hated it.',
        'Great acting and direction.',
        'Boring and slow, did not like it.',
        'Excellent story and visuals.',
        'Poor script, disappointed.',
        'Awesome movie, highly recommend!',
        'Not worth watching at all.'
    ],
    'label': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
})

def preprocess_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    tokens = text.split()
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return ' '.join(tokens)

print("1. Предобработка текстовых данных")
print("-" * 50)
print("Исходные данные:")
print(data[['text', 'label']].to_string(index=False))
print("\n")

data['clean_text'] = data['text'].apply(preprocess_text)

print("После предобработки:")
for i, row in data.iterrows():
    print(f"Исходный: {row['text']}")
    print(f"Очищенный: {row['clean_text']}")
    print(f"Метка: {row['label']}")
    print("-" * 50)

X_train, X_test, y_train, y_test = train_test_split(
    data['clean_text'], data['label'], test_size=0.2, random_state=42, stratify=data['label']
)

print(f"\nРазмер обучающей выборки: {len(X_train)}")
print(f"Размер тестовой выборки: {len(X_test)}")
print("\n" + "=" * 60)
print("2. ML модель для классификации текста")
print("=" * 60)

vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

ml_model = LogisticRegression(max_iter=1000, random_state=42)
ml_model.fit(X_train_tfidf, y_train)

y_pred_ml = ml_model.predict(X_test_tfidf)

accuracy_ml = accuracy_score(y_test, y_pred_ml)
f1_ml = f1_score(y_test, y_pred_ml)

print("ML модель (Логистическая регрессия)")
print(f"Accuracy: {accuracy_ml:.4f}")
print(f"F1-score: {f1_ml:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred_ml))

cm_ml = confusion_matrix(y_test, y_pred_ml)
plt.figure(figsize=(5, 4))
sns.heatmap(cm_ml, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix - Logistic Regression')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

print("\n" + "=" * 60)
print("3. Нейронная сеть для классификации текста")
print("=" * 60)

MAX_NB_WORDS = 5000
MAX_SEQUENCE_LENGTH = 100
EMBEDDING_DIM = 100

tokenizer = Tokenizer(num_words=MAX_NB_WORDS, lower=True)
tokenizer.fit_on_texts(X_train)
X_train_seq = tokenizer.texts_to_sequences(X_train)
X_test_seq = tokenizer.texts_to_sequences(X_test)

X_train_pad = pad_sequences(X_train_seq, maxlen=MAX_SEQUENCE_LENGTH)
X_test_pad = pad_sequences(X_test_seq, maxlen=MAX_SEQUENCE_LENGTH)

model = Sequential([
    Embedding(MAX_NB_WORDS, EMBEDDING_DIM, input_length=MAX_SEQUENCE_LENGTH),
    LSTM(64, dropout=0.2, recurrent_dropout=0.2),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

early_stop = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

history = model.fit(
    X_train_pad, y_train,
    epochs=10,
    batch_size=32,
    validation_split=0.2,
    callbacks=[early_stop],
    verbose=1
)

loss, accuracy_nn = model.evaluate(X_test_pad, y_test, verbose=0)
y_pred_nn = (model.predict(X_test_pad, verbose=0) > 0.5).astype(int)
f1_nn = f1_score(y_test, y_pred_nn)

print("\nНейронная сеть (LSTM)")
print(f"Accuracy: {accuracy_nn:.4f}")
print(f"F1-score: {f1_nn:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred_nn))

cm_nn = confusion_matrix(y_test, y_pred_nn)
plt.figure(figsize=(5, 4))
sns.heatmap(cm_nn, annot=True, fmt='d', cmap='Greens')
plt.title('Confusion Matrix - LSTM')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Model Accuracy - LSTM')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss - LSTM')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.show()

print("\n" + "=" * 60)
print("4. Сравнение результатов")
print("=" * 60)

print(f"\nML модель (Логистическая регрессия):")
print(f"  - Accuracy: {accuracy_ml:.4f}")
print(f"  - F1-score: {f1_ml:.4f}")
print(f"\nНейронная сеть (LSTM):")
print(f"  - Accuracy: {accuracy_nn:.4f}")
print(f"  - F1-score: {f1_nn:.4f}")

print("\n" + "-" * 50)
print("Объяснение результатов:")
print("-" * 50)

if f1_nn > f1_ml:
    print("✓ Нейронная сеть (LSTM) показала лучший результат.")
    print("  Причины:")
    print("  - LSTM учитывает последовательность слов и контекст")
    print("  - Эмбеддинги позволяют捕捉语义ческие связи")
    print("  - Нейросеть лучше обобщает на новых данных")
else:
    print("✓ ML модель показала сравнимый или лучший результат.")
    print("  Причины:")
    print("  - Малый объем данных (всего 10 примеров)")
    print("  - Логистическая регрессия эффективна на разреженных данных")
    print("  - TF-IDF хорошо работает с короткими текстами")