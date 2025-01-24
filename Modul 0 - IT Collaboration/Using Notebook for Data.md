# **IT Collaboration (Notebook, Git, & Github)**

Pada pertemuan GWE yang pertama ini, kita akan membahas mengenai tools-tools yang akan teman-teman pakai selama belajar di Study Group EDM. Mulai dari Notebook hingga Github, tools-tools ini dibutuhkan karena kalian akan berkolaborasi dalam sebuah kelompok untuk mengerjakan suatu projek.

<h2 style="border-bottom: 0.5px solid red; width: 80%; margin: 0 auto;">

## What is Notebook and How to Use It?

**Notebook** adalah lingkungan interaktif untuk menulis dan menjalankan kode, membuat visualisasi, serta menambahkan teks naratif dalam satu dokumen yang dapat diakses dan dibagikan.

### Tools

**Jupyter Notebook** adalah aplikasi web open-source yang memungkinkan pengguna untuk membuat dan berbagi notebook yang berisi kode Python (atau bahasa pemrograman lainnya), teks, dan visualisasi.

**Google Colab** adalah platform cloud berbasis Jupyter Notebook yang disediakan oleh Google, memungkinkan pengguna untuk membuat, menjalankan, dan berbagi notebook Python secara gratis dengan akses ke GPU dan TPU secara gratis.

**Kaggle** menyediakan lingkungan Jupyter Notebook (Kaggle Kernels) yang memungkinkan pengguna untuk menjalankan kode Python dan R di cloud dengan akses ke dataset Kaggle, kompetisi data, dan integrasi dengan komunitas data scientist.

**Perbedaan antara ketiganya:**

1. Jupyter Notebook: Memerlukan instalasi dan pengelolaan sendiri, dapat dijalankan secara lokal.
2. Google Colab: Platform cloud dengan akses gratis ke GPU/TPU, integrasi dengan Google Drive, dan kolaborasi real-time.
3. Kaggle Kernels: Lingkungan cloud untuk analisis data dan kompetisi, dengan akses ke dataset Kaggle dan komunitas data scientist.

<br>

### [Click here for Example of Machine learning project using Google Colab Notebook](https://colab.research.google.com/github/ageron/handson-ml2/blob/master/02_end_to_end_machine_learning_project.ipynb#scrollTo=tmJG3W51lp2G)

<br>

### How to read and using data for processing on Google Colab Notebook

Berikut cara ketika data sudah didownload dan dimasukkan ke Gdrive yang sudah terhubung dengan Google Colab.

> ### Step 1: Mount the Google Drive

    Langkah pertama adalah mounting Google Drive ke notebook Google Colab . Ini akan memungkinkan untuk mengakses file Google Drive langsung dari notebook. Untuk mounting Google Drive, bisa menggunakan kode berikut:

    from google.colab import drive
    drive.mount('/content/drive')

> ### Step 2: Navigate to the file you want to read

    Setelah mounting Google Drive, kita dapat mengakses file yang ingin  dibaca. Google Colab menyediakan penjelajah file yang dapat digunakan untuk menjelajahi Google Drive. Untuk membuka penjelajah file, berikut kodenya:

    !ls "/content/drive/My Drive/"

    Kode di atas akan menampilkan daftar isi dari direktori utama Google Drive. Kita dapat mengganti /My Drive/ dengan jalur ke direktori yang berisi file kita.

> ### Step 3: Read the file into your notebook

Setelah menavigasi ke file yang ingin dibaca, kita dapat membacanya ke dalam notebook. Metode yang digunakan untuk membaca file akan bergantung pada jenis file yang dikerjakan.

Berikut adalah beberapa contohnya:

- ### Reading a text file

  with open('/content/drive/My Drive/example.txt', 'r') as f:
    
  text = f.read()
    
  print(text)


- ### Reading a CSV file

  import pandas as pd

  data = pd.read_csv('/content/drive/My Drive/my_data/data.
  csv')

  print(data.head())

- ### Reading an image file

  from PIL import Image

  import matplotlib.pyplot as plt

  image = Image.open('/content/drive/MyDrive/saturn-cloud-saturn-cloud.png')
  
  plt.imshow(image)

- ### Reading data from kaggle (Additional)

  Steps:

  1. Download API Credentials
  2. Upload file kaggle.json ke Google Colab
  3. Instalasi (seperti library dll) pada Google Colab
  4. Download dataset dengan mencari nama dari dataset pada kaggle

     [Untuk detail dan lebih jelas klik disini](https://www.analyticsvidhya.com/blog/2021/06/how-to-load-kaggle-datasets-directly-into-google-colab/)
