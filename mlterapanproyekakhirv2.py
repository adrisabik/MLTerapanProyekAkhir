# -*- coding: utf-8 -*-
"""MLTerapanProyekAkhirV2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/123T-tVbrDivVlkfphaKZcszjM6lu9mLx

## Nama : Adri Sabik Muhana

## Alamat : Kasihan, Bantul, DIY

## Instansi : UPN Veteran Yogyakarta

## email : adrisabik@gmail.com

### **Dataset : IMDb movies extensive dataset**

### **link dataset : https://www.kaggle.com/stefanoleone992/imdb-extensive-dataset**


---

## **Import Library**
"""

import pandas as pd
import numpy as np 
import tensorflow as tf
import matplotlib.pyplot as plt
from zipfile import ZipFile

from tensorflow import keras
from tensorflow.keras import layers
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

"""### **Import dataset**"""

from google.colab import drive
drive.mount('/content/drive')

"""### **Load dataset**"""

movie = pd.read_csv('drive/MyDrive/Datasets/IMDb Movie/IMDb movies.csv')
actor = pd.read_csv('drive/MyDrive/Datasets/IMDb Movie/IMDb names.csv')
rating = pd.read_csv('drive/MyDrive/Datasets/IMDb Movie/IMDb ratings.csv')
 
print('Jumlah film   : ', len(movie.imdb_title_id.unique()))
print('Jumlah actor  : ', len(actor.imdb_name_id.unique()))
print('Jumlah rating : ', len(rating.imdb_title_id.unique()))

"""## **Explor variabel movie**"""

movie.info()

"""### **Drop data yang tidak digunakan**"""

movie.drop(['original_title', 'date_published', 'language', 'writer', 'production_company', 'description', 'avg_vote', 'votes', 'budget', 'usa_gross_income', 'worlwide_gross_income', 'metascore', 'reviews_from_users', 'reviews_from_critics'], axis=1, inplace=True)

"""### **Membuat genre, country, dan actor menjadi satu**"""

# membuat genre menjadi 1
movie.genre = movie.genre.str.split(", ", expand = True)

# membuat country menjadi 1
movie.country = movie.country.str.split(", ", expand = True)

# membuat actor menjadi 1
movie.actors = movie.actors.str.split(", ", expand = True)

movie.head()

"""### **Eksplor genre lebih jauh**"""

count = movie.genre.value_counts()
percent = 100*movie.genre.value_counts(normalize=True)
df = pd.DataFrame({'jumlah sampel':count, 'persentase':percent.round(1)})
print(df)
count.plot(kind='bar', title='genre');

print('Jumlah film : ', len(movie.imdb_title_id.unique()))
print('Jumlah direktor : ', len(movie.director.unique()))
print('Direktor        : ', movie.director.unique())
print('Jumlah aktor : ', len(movie.actors.unique()))
print('Jumlah aktor : ', movie.actors.unique())
print('Jumlah genre : ', len(movie.genre.unique()))
print('genre        : ', movie.genre.unique())

"""## **Eksplorasi variabel actor**"""

actor.info()

"""### **Drop data yang tidak digunakan**"""

actor = actor[['imdb_name_id', 'name']]
actor

print('Jumlah aktor   : ', len(actor.imdb_name_id.unique()))

"""### **Eksplorasi variabel rating**"""

rating.info()

"""### **Drop data yang tidak digunakan**"""

rating = rating[['imdb_title_id', 'weighted_average_vote']]
rating = rating.rename(columns={'weighted_average_vote':'rating'})
rating

"""### **Melihat lebih jauh pada rating**"""

rating.describe()

"""Bisa dilihat bahwa rating berkisar antara 1-10"""

print('Jumlah film yang diberi rating : ', len(rating.imdb_title_id.unique()))

"""## **Data Preparation**"""

# Definisikan dataframe rating ke dalam variabel all_movie_rate
all_movie_rate = rating
all_movie_rate

"""### **Menggabungkan data**"""

# Menggabungkan all_movie_rate dengan dataframe movie(title, genre) berdasarkan imdb_title_id
all_movie = pd.merge(all_movie_rate, movie[['imdb_title_id','title', 'genre']], on='imdb_title_id', how='left')
 
# Print dataframe all_movie
all_movie

"""### **Mengecek missing value**"""

all_movie.isnull().sum()

"""### **Mengurutkan data**"""

preparation = all_movie.sort_values('imdb_title_id', ascending=True)
preparation

"""### **Mengurangi data karena crash ram tidak cukup**

Sebelumnya saya sudah mencoba beberapa cara tapi tidak bisa, jadi saya kurangi saja data yang saya pakai
"""

preparation = preparation.drop(preparation.index[20000:])
preparation

"""### **Mengecek kategori genre**"""

preparation.genre.unique()

"""### **Konversi data ke list**"""

# Mengonversi data series ‘imdb_title_id’ menjadi dalam bentuk list
movie_id = preparation['imdb_title_id'].tolist()
 
# Mengonversi data series ‘title’ menjadi dalam bentuk list
movie_name = preparation['title'].tolist()
 
# Mengonversi data series ‘genre’ menjadi dalam bentuk list
movie_genre = preparation['genre'].tolist()
 
print(len(movie_id))
print(len(movie_name))
print(len(movie_genre))

"""### **Membuat dictionary**"""

movie_new = pd.DataFrame({
    'id': movie_id,
    'title': movie_name,
    'genre': movie_genre
})
movie_new

"""## **Pemodelan dengan Content Based Filtering**

### **Menggunakan teknik TF-IDF Vectorizer**
"""

# Inisialisasi TfidfVectorizer
tf = TfidfVectorizer()
 
# Melakukan perhitungan idf pada movie_new genre
tf.fit(movie_new['genre']) 
 
# Mapping array dari fitur index integer ke fitur nama
tf.get_feature_names()

"""### **Melakukan fit lalu ditransformasikan ke bentuk matrix**"""

tfidf_matrix = tf.fit_transform(movie_new['genre']) 
 
# Melihat ukuran matrix tfidf
tfidf_matrix.shape

"""### **Mengubah vektor tf-idf dalam bentuk matriks dengan fungsi todense()**"""

tfidf_matrix.todense()

"""### **Membuat dataframe untuk melihat tf-idf matrix**"""

pd.DataFrame(
    tfidf_matrix.todense(), 
    columns=tf.get_feature_names(),
    index=movie_new.title
).sample(22, axis=1).sample(10, axis=0)

"""### **Menghitung cosine similarity pada matrix tf-idf**"""

cosine_sim = cosine_similarity(tfidf_matrix) 
cosine_sim

"""### **Membuat dataframe dari variabel cosine_sim**"""

# baris dan kolom nama film
cosine_sim_df = pd.DataFrame(cosine_sim, index=movie_new['title'], columns=movie_new['title'])
print('Shape:', cosine_sim_df.shape)
 
# Melihat similarity matrix pada setiap resto
cosine_sim_df.sample(5, axis=1).sample(10, axis=0)

"""### **Membuat fungsi movie_recommendations**"""

def movie_recommendations(movie_name, similarity_data=cosine_sim_df, items=movie_new[['title', 'genre']], k=10):
    # Mengambil data dengan menggunakan argpartition untuk melakukan partisi secara tidak langsung sepanjang sumbu yang diberikan    
    # Dataframe diubah menjadi numpy
    # Range(start, stop, step)
    index = similarity_data.loc[:,movie_name].to_numpy().argpartition(
        range(-1, -k, -1))
    
    # Mengambil data dengan similarity terbesar dari index yang ada
    closest = similarity_data.columns[index[-1:-(k+2):-1]]
    
    # Drop movie_name agar nama film yang dicari tidak muncul dalam daftar rekomendasi
    closest = closest.drop(movie_name, errors='ignore')
 
    return pd.DataFrame(closest).merge(items).head(k)

"""### **Evaluation**"""

movie_new[movie_new.title.eq('Ginger')]

# Mendapatkan rekomendasi film yang mirip dengan Ginger
movie_recommendations('Ginger')