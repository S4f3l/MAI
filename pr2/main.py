import re
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, classification_report
import numpy as np
import nltk

nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

data = [
    ("I love this movie, it is amazing!", 1),
    ("Terrible film, waste of time.", 0),
    ("Absolutely fantastic performance.", 1),
    ("Worst movie ever, hated it.", 0),
    ("Great acting and direction.", 1),
    ("Boring and slow, did not like it.", 0),
    ("Excellent story and visuals.", 1),
    ("Poor script, disappointed.", 0),
    ("Awesome movie, highly recommend!", 1),
    ("Not worth watching at all.", 0)
]


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


texts = [preprocess_text(t) for t, _ in data]
labels = [l for _, l in data]

print("1. Предобработка текстовых данных")
print("-" * 50)
for i, (original, processed) in enumerate(zip([t for t, _ in data], texts)):
    print(f"Исходный: {[t for t, _ in data][i]}")
    print(f"Очищенный: {processed}")
    print(f"Метка: {labels[i]}")
    print("-" * 50)

X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.2, random_state=42, stratify=labels
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

print("\n" + "=" * 60)
print("3. Нейронная сеть для классификации текста")
print("=" * 60)

try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Embedding, LSTM, Dense
    from tensorflow.keras.preprocessing.text import Tokenizer
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    from tensorflow.keras.callbacks import EarlyStopping

    np.random.seed(42)
    tf.random.set_seed(42)

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
        X_train_pad, np.array(y_train),
        epochs=10,
        batch_size=32,
        validation_split=0.2,
        callbacks=[early_stop],
        verbose=1
    )

    loss, accuracy_nn = model.evaluate(X_test_pad, np.array(y_test), verbose=0)
    y_pred_nn = (model.predict(X_test_pad, verbose=0) > 0.5).astype(int)
    f1_nn = f1_score(y_test, y_pred_nn)

    print("\nНейронная сеть (LSTM)")
    print(f"Accuracy: {accuracy_nn:.4f}")
    print(f"F1-score: {f1_nn:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred_nn))

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

except ImportError:
    print("\nTensorFlow не установлен. Пропуск нейронной сети.")
    print("\n" + "=" * 60)
    print("4. Итоговый результат")
    print("=" * 60)
    print(f"\nML модель (Логистическая регрессия):")
    print(f"  - Accuracy: {accuracy_ml:.4f}")
    print(f"  - F1-score: {f1_ml:.4f}")
    print("\nОбъяснение:")
    print("- ML модель показала хороший результат на малом объеме данных")
    print("- TF-IDF эффективно работает с короткими текстами")
    print("- Для обучения нейронной сети требуется больше данных")