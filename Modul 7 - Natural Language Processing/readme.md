# Modul 7 - Deep Learning for Text Mining: Sentiment Analysis and NLP Applications

<br>

![alt text](asset/image.jpg)

<br>

## Introduction
Pada modul ini, kita akan mempelajari **Natural Language Processing (NLP)** dan penerapannya dalam **Deep Learning for Text Mining**. NLP memungkinkan komputer untuk memahami, menafsirkan, dan menghasilkan teks yang bersifat **unstructured**, yang banyak digunakan dalam aplikasi seperti **sentiment analysis** dan **pengolahan bahasa alami** lainnya.

### Tantangan dalam Bahasa Indonesia pada NLP
Bahasa manusia sangat kompleks dan ambigu. Sebuah kalimat bisa memiliki banyak arti tergantung pada konteks. Bahasa Indonesia sendiri memiliki berbagai dialek, gaya bicara, dan bahasa gaul, yang menjadi tantangan tersendiri dalam NLP.

## NLP Pipeline
Proses dalam NLP dibagi dalam beberapa tahapan untuk memproses teks, di antaranya:

### 1. **Text Acquisition (Pengumpulan Teks)**
   Pengumpulan data teks dari berbagai sumber seperti web scraping, API, atau file teks.
   - **Web Scraping**: Menggunakan library seperti BeautifulSoup dan Requests.
   - **API Integration**: Menggunakan API untuk platform seperti Twitter atau Reddit.
   - **File Processing**: Membaca data dari file TXT, CSV, PDF, atau DOCX menggunakan library seperti pandas atau PyPDF2.

### 2. **Text Cleaning (Pembersihan Teks)**
   Pembersihan teks bertujuan untuk menghilangkan data yang tidak relevan atau noise dari teks mentah. Ini termasuk menghapus HTML tags, karakter khusus, URL, email, dan username.
   - Mengubah teks menjadi huruf kecil (case folding).
   - Menangani masalah encoding.
   - Menghapus whitespace yang tidak diperlukan.

### 3. **Text Preprocessing (Pra-pemrosesan Teks)**
   - **Tokenization**: Proses memecah teks menjadi token (kata, kalimat, atau karakter).
   - **Normalization**: Menggunakan teknik seperti stemming dan lemmatization untuk mengubah kata menjadi bentuk dasarnya.
   - **Stopword Removal**: Menghapus kata-kata yang tidak memberikan informasi penting.
   - **POS Tagging**: Menandai setiap kata dengan kategori gramatikal (misalnya kata benda, kata kerja).
   - **Named Entity Recognition (NER)**: Mengidentifikasi entitas dalam teks seperti nama orang atau tempat.

### 4. **Feature Extraction (Ekstraksi Fitur)**
   - **Count-Based Features**: Menggunakan teknik seperti Bag-of-Words (BoW) untuk menghitung frekuensi kata.
   - **Weight-Based Features**: Menggunakan teknik seperti **TF-IDF** (Term Frequency - Inverse Document Frequency) untuk memberi bobot pada kata berdasarkan pentingnya kata dalam dokumen.
   - **Static Word Embeddings**: Teknik seperti **Word2Vec**, **GloVe**, dan **FastText** untuk menghasilkan representasi kata dalam bentuk vektor.
   - **Contextual Embeddings**: Model berbasis Transformer seperti **BERT** yang memberikan representasi kata yang berubah tergantung pada konteks kalimat.

### 5. **Modeling & Evaluation (Pemodelan dan Evaluasi)**
   - **Traditional ML Approaches**: Menggunakan algoritma machine learning klasik seperti **Naive Bayes**, **SVM**, dan **Random Forest**.
   - **Deep Learning Models**:
     - **Recurrent Neural Networks (RNN)**: Model yang digunakan untuk urutan data, seperti **LSTM** dan **GRU**.
     - **Convolutional Neural Networks (CNN)**: Digunakan dalam pemrosesan data teks berbentuk gambar atau grid.
     - **Transformer Models**: Seperti **BERT**, **RoBERTa**, dan **GPT**, yang sangat kuat dalam NLP tasks.

## Sentiment Analysis
Salah satu aplikasi penting dalam NLP adalah **Sentiment Analysis**, yang digunakan untuk menentukan sentimen (positif, negatif, netral) dari teks.

**Traditional ML Approach - Notebook Link**:  
[Link Notebook Hands-On Traditional ML](https://github.com/lifeatedmlab/GWE-2025/blob/790e1fa32a69c5ec5c63345d08470e9ed0d56d30/Modul%207%20-%20Natural%20Language%20Processing/Hands-On!/ml_traditional.ipynb)

**DL (BERT) Approach - Notebook Link**:  
[Link Notebook Hands-On BERT](https://github.com/lifeatedmlab/GWE-2025/blob/790e1fa32a69c5ec5c63345d08470e9ed0d56d30/Modul%207%20-%20Natural%20Language%20Processing/Hands-On!/bert.ipynb)

**Enjoy! Hope it helps 🚀**