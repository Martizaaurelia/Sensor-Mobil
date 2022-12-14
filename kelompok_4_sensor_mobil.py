# -*- coding: utf-8 -*-
"""Kelompok 4 - Sensor Mobil

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16k6hzsYgaCSr7H-vh8npOFyIYfDQJpno

## Data Visualization Sensor Mobil
"""

# Import library yang dibutuhkan

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

"""## **DATA UNDERSTANDING**"""

# Mengimport dataset yang digunakan

df = pd.read_csv("https://github.com/Martizaaurelia/Sensor-Mobil-Data-Visualization/raw/main/kecelakaan.csv")

# Melihat data teratas

df.head()

# Melihat data terbawah

df.tail()

# Melihat info dari dataset yang digunakan

df.info()

# Melihat informasi data secara statistik

df.describe()

#Menampilkan semua deskripsi data
df.describe(include="all")

"""## **DATA PREPARATION**"""

# Melakukan pengecekan tipe data

print(df.dtypes)

# Handling missing value

df.isnull().sum()

import missingno as mno
mno.matrix(df)

# Mengambil kolom untuk data yang dibutuhkan

kecelakaan = df[["ACCIDENT NO","ACCIDENT DATE","ACCIDENT TIME","ACCIDENT TYPE","ACCIDENT TYPE DESC","DAY OF WEEK","DAY WEEK DESCRIPTION","DCA DESCRIPTION","NO PERSONS","NO PERSONS KILLED","ROAD GEOMETRY","ROAD GEOMETRY  DESC","SPEED ZONE"]]
kecelakaan

"""## **DATA MODELING**"""

# Grafik data kecelakaan berdasarkan tipe kecelakaan dan zona kecepatan

perSZ = kecelakaan[['ACCIDENT TYPE', 'SPEED ZONE']].groupby('ACCIDENT TYPE', as_index=False).agg('sum').sort_values(by='ACCIDENT TYPE', ascending=False)

sns.barplot(x = 'ACCIDENT TYPE', y = 'SPEED ZONE', data=perSZ)
plt.title("Data Kecelakaan Berdasarkan Tipe Kecelakaan dan Zona Kecepatan")

# Grafik data kecelakaan per hari tanpa menimbulkan korban
perHari = kecelakaan[['DAY WEEK DESCRIPTION', 'NO PERSONS']].groupby('DAY WEEK DESCRIPTION').agg('sum')

sns.lineplot(x = "DAY WEEK DESCRIPTION", y = "NO PERSONS", markers=True, dashes=False, data=perHari)
plt.title("Data Kecelakaan per Hari Tanpa Menimbulkan Korban")
plt.xticks(rotation=90)

# Grafik data kecelakaan per hari tanpa menimbulkan korban meninggal
perHariKM = kecelakaan[['DAY WEEK DESCRIPTION', 'NO PERSONS KILLED', 'ACCIDENT DATE']].groupby('DAY WEEK DESCRIPTION', as_index=False).sum().melt(id_vars='DAY WEEK DESCRIPTION')
print(perHariKM)
sns.barplot(x='value', y='DAY WEEK DESCRIPTION', hue='variable', data=perHariKM)
plt.title("Data Kecelakaan per Hari Tanpa Menimbulkan Korban Meninggal")

# Grafik perhitungan data kecelakaan berdasarkan tanggal
sns.countplot(x="ACCIDENT DATE", hue='DAY WEEK DESCRIPTION', data=kecelakaan)

plt.title("Perhitungan Data Kecelakaan Berdasarkan Tanggal")
plt.xticks(rotation=90)
plt.xlim(0,10)

# Mencari rata-rata data
kecelakaan.mean()

# Mencari total nilai dalam data
kecelakaan.sum()

# Mencari median dalam data
kecelakaan.median()

# Mencari variasi dalam data
kecelakaan.var()

# Mencari standar deviasi dalam data
kecelakaan.std()

# Mencari nilai quartil dalam data
q3 = kecelakaan.quantile(0.75)
q1 = kecelakaan.quantile(0.25)

# Mencari jarak (jangkauan) data
iqr = q3 - q1
iqr

# Mencari pencilan data

kecelakaan_align, iqr_new = kecelakaan.align(iqr, axis = 1, copy=False, join="outer")
outlier_filter = (kecelakaan <q1 - 1.5 * iqr_new) | (kecelakaan >q3 + 1.5 * iqr_new)
outlier_filter

# Menentukan pencilan data

kecelakaan[outlier_filter['NO PERSONS']].loc[:,['ACCIDENT TIME', 'NO PERSONS']].sort_values(by=['NO PERSONS'], ascending = False)

# Mencari korelasi semua data kecelakaan
kecelakaan.corr()

# Mencari korelasi dari kecelakaan yang tidak menimbulkan korban dalam data

kecelakaan.loc[:, 'NO PERSONS':].corr()

# Membuat pie chart dari data

kecelakaan['DAY WEEK DESCRIPTION'].value_counts().plot(kind='pie', autopct='%1.1f%%', shadow=True)
plt.title("Persentase Kecelakaan dalam Kurun Waktu 7 Hari")

# Membuat bar chart dari data

kecelakaan[['DAY WEEK DESCRIPTION', 'NO PERSONS']].value_counts().plot(kind='bar')
plt.title("Persentase Kecelakaan Tanpa Menimbulkan Korban")

# Membuat histogram dari data kecelakaan tanpa menimbulkan korban

kecelakaan.hist(column='NO PERSONS', bins = 30)

# Menampilkan data kecelakaan yang tidak menimbulkan korban berdasarkan hari

kecelakaan.hist(column='NO PERSONS', by='DAY OF WEEK', bins = 30)

# Menampilkan data kecelakaan per hari berdasarkan geometri jalan yang dilalui

kecelakaan[['DAY OF WEEK', 'ROAD GEOMETRY']].plot(kind='hist',
                                          alpha = 0.7,
                                          bins = 30,
                                          title = 'Histogram Data Kecelakaan per Hari Berdasarkan Geometri Jalan yang Dilalui',
                                          rot = 45, grid = True, 
                                          figsize=(12,8),
                                          fontsize=15,
                                          color=['#FD841F', '#AF0171'])
plt.xlabel('Day of Week')
plt.ylabel('Road Geometry')

# Import library
from scipy import stats

# Membuat koefisien korelasi dan hubungan sebab-akibat dari data

pearson_coef, p_value = stats.pearsonr(kecelakaan['DAY OF WEEK'], kecelakaan['NO PERSONS'])
print("The Pearson Correlation Coefficient is", pearson_coef, 'with p-value = ', p_value)

# Membuat regresi dari data kecelakaan yang tidak mengakibatkan korban per minggu
sns.regplot(x='DAY OF WEEK', y='NO PERSONS', data=kecelakaan)

# Dimulai dari 0 hingga tak terhingga
plt.ylim(0,)
plt.show()

kecelakaan[['DAY OF WEEK', 'NO PERSONS']].corr()

# Menampilkan semua deskripsi data termasuk object
kecelakaan.describe(include=['object'])

# Mengganti nama sebuah data
accident_type_counts = df['ACCIDENT TYPE'].value_counts().to_frame()

accident_type_counts.rename(columns={'ACCIDENT TYPE' : 'TYPE OF ACCIDENT'}, inplace=True)
accident_type_counts

# Mengetahui index dari data yang ingin dicari

accident_type_counts.index.name='ACCIDENT TYPE'
accident_type_counts

"""## Outlier (Trims dan Winsorize)"""

from scipy.stats.mstats import winsorize
from scipy.stats.mstats import trima
from sklearn.preprocessing import Normalizer

a = kecelakaan['NO PERSONS']
a

# Menghilangkan 10% nilai terbawah dan 20% nilai teratas
wins = winsorize(a, limits=[0.1,0.2])
print(wins)

# Menghilangkan nilai dibawah 2 dan nilai diatas 8

trims = trima(a, limits=(2,8))
print(trims)

"""## Discretization / Binning"""

kecelakaan.head()
kecelakaan

days = np.linspace(min(kecelakaan['DAY OF WEEK']), 
                max(kecelakaan['DAY OF WEEK']), 8)
days

print(min(kecelakaan['DAY OF WEEK']), max(kecelakaan['DAY OF WEEK']))

kategori = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

kecelakaan['DAY DESC'] = pd.cut(kecelakaan['DAY OF WEEK'], days, labels=kategori,
                            include_lowest=True)
kecelakaan

interval_range = pd.interval_range(start=0,
                                   freq=1,
                                   end=7)
kecelakaan['DAY DESC 2'] = pd.cut(kecelakaan['DAY OF WEEK'], bins = interval_range)
kecelakaan

kecelakaan['DAY DESC 3'] = pd.qcut(kecelakaan['DAY OF WEEK'], 3)
kecelakaan

"""## Normalisasi"""

a = kecelakaan['NO PERSONS']
a

means = a.mean(axis=0)

max_min = a.max(axis=0) - a.min(axis=0)

max_min_no_persons = (a - a.min(axis=0)) / max_min
kecelakaan

# Melihat distribusi data dari target classes --> DAY WEEK DESCRIPTION

import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('seaborn')

sns.countplot(kecelakaan["DAY WEEK DESCRIPTION"])
xlabel = "DAYS"
ylabel = "count"

# Melakukan visualisasi kolom numerik yang dikelompokkan berdasarkan day week description (hari)

sns.pairplot(kecelakaan,hue='DAY WEEK DESCRIPTION')

# Import train test split
from sklearn.model_selection import train_test_split as tts

# Melihat korelasi antar dua variabel
# Melihat causation (sebab akibat) antar dua variabel

kecepatan = kecelakaan[['SPEED ZONE']]
korban = kecelakaan[['NO PERSONS KILLED']]

X_train, X_test, y_train, y_test = tts(kecepatan, korban, random_state=101, test_size = 0.25)

plt.scatter(X_train, y_train)
plt.xlabel('Speed Zone')
plt.ylabel('No Persons Killed')
plt.title('Besarnya Kecepatan dan Tidak Adanya Korban Meninggal')
plt.show()

sns.regplot(x='SPEED ZONE', y='NO PERSONS KILLED', data=kecelakaan)
plt.ylim(0,)
plt.xlabel('Speed Zone')
plt.ylabel('No Persons Killed')
plt.title('Besarnya Kecepatan dan Tidak Adanya Korban Meninggal')
plt.show()

kecelakaan[['SPEED ZONE','NO PERSONS KILLED']].corr()

# Import LinearRegression

from sklearn.linear_model import LinearRegression as lr
model1 = lr()
model1.fit(X_train,y_train)

# Perbandingan nilai antara y_test dan y_pred
y_pred = model1.predict(X_test)

from sklearn import metrics

r2 = metrics.r2_score(y_test, y_pred)
print("Performansi model untuk pengujian")
print("Nilai R2 adalah {}".format(r2))

# Nilai R2 adalah -0.0004286282705445732
# Ini merupakan hasil yang kurang baik karena seharusnya y_test yang sempurna akan menghasilkan nilai R2 = 1

# import LogisticRegression
from sklearn.linear_model import LogisticRegression

lg = LogisticRegression()
lg.fit(X_train,y_train)

y_pred = lg.predict(X_test)

# AUC (Area Under Curve) = sebuah daerah dalam kurva ROC
# Semakin mendekati nilai 1, maka semakin baik juga model dalam menggambarkan dataset yang dimiliki

from sklearn import metrics
auc = metrics.accuracy_score(y_test,y_pred)
print(f"Nilai AUC = {auc}")

# Nilai AUC = 0.984, nilai yang cukup bagus karena sudah mendekati nilai 1.

# Korelasi di setiap variabel di dalam dataset yang digunakan

corrmat = kecelakaan.corr()
top_corr_features = corrmat.index
plt.figure(figsize=(13,13))

# plot heatmap
h = sns.heatmap(kecelakaan[top_corr_features].corr(),annot=True,cmap="RdBu")

"""## **UNSUPERVISED LEARNING (CLUSTERING)**"""

# feature scaling
# standarisasi untuk kolom Day Of Week, No Persons Killed dan Speed Zone

from sklearn.preprocessing import StandardScaler

kecelakaan_new = kecelakaan[['DAY OF WEEK','NO PERSONS KILLED','SPEED ZONE']].copy()

scaler = StandardScaler()

scaled_data = scaler.fit_transform(kecelakaan_new)
print(scaled_data)

kecelakaan_scaled = pd.DataFrame(scaled_data, columns=['DAY OF WEEK','NO PERSONS KILLED','SPEED ZONE'])
kecelakaan_scaled

# Elbow method untuk menemukan jumlah kluster yang sesuai

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def elbowMethod(X, k_min=1, k_max=10, save=False):
    K_range = range(k_min,k_max+1)

    result = []
    for k in K_range:
        model = KMeans(n_clusters = k, random_state=20)
        model.fit(X)
        result.append(model.inertia_)
        
    fig, ax = plt.subplots(figsize=(15,8))
    
    ax.plot(K_range, result, marker='o')
    
    for i, value in enumerate(result):
        ax.text(i+1.15, value-0.005, round(value,2), fontsize=13, fontweight='bold')
    
    plt.xticks(K_range)
    plt.grid()
    plt.title('Elbow Method\n', fontsize=18)
    plt.xlabel('\nn-Cluster', fontsize=15)
    plt.ylabel('WCSS\n', fontsize=15)
    
    if save==True:
        plt.savefig('elbowMethod.png', dpi=200)
    
    plt.show()

elbowMethod(kecelakaan_scaled)

"""Dari hasil plot tersebut, kita dapat mengetahui nilai kluster terbaik adalah k = 1 """

# Silhouette method

def silMethod(X, k_min=2, k_max=10, save=False):
    K_range2 = range(k_min,k_max+1)

    result_sm = []
    for k in K_range2:
        model2 = KMeans(n_clusters = k, random_state=20)
        model2.fit(X)
        labels = model2.labels_
    
        s_score = silhouette_score(X, labels, metric='euclidean')
        result_sm.append(s_score)
        
    fig2, ax2 = plt.subplots(figsize=(15,8))
    ax2.plot(K_range2, result_sm, marker='o')
    
    for i, value in enumerate(result_sm):
        ax2.text(i+2.15, value-0.005, round(value,2), fontsize=13, fontweight='bold')
    
    plt.xticks(K_range2)
    plt.grid()
    plt.title('Silhouette Method\n', fontsize=18)
    plt.xlabel('\nn-Cluster', fontsize=15)
    plt.ylabel('Silhouette Score\n', fontsize=15)
    if save==True:
        plt.savefig('silMethod.png', dpi=200)
    plt.show()

silMethod(kecelakaan_scaled)

"""Dari hasil plot tersebut, kita dapat mengetahui nilai kluster terbaik adalah k = 9

**Menggunakan k = 9**
"""

# import kmeans
from sklearn.cluster import KMeans

k9 = KMeans(n_clusters=1, random_state=15)

k9.fit(kecelakaan_scaled)
kecelakaan_scaled['lbl_k9'] = k9.labels_

kecelakaan_scaled

kecelakaan_scaled['lbl_k9'].value_counts()

"""**Melakukan plotting hasil clustering dengan centroid**"""

# Get the centroid
centroid_k9 = k9.cluster_centers_
centroid_k9

# X axis of Centroid
centroidX = centroid_k9[:,0]
centroidX

# Y axis of Centroid
centroidY = centroid_k9[:,1]
centroidY

# Z axis of Centroid
centroidZ = centroid_k9[:,2]
centroidZ

fig, ax = plt.subplots(figsize=(14,10))

# Create custom color dictionary
colorDict = {0:'#B88E8D', 1:'#60E1E0'}

# set axes bg color
ax.patch.set_facecolor('#CCCCCC')

# plot the data
ax.scatter(kecelakaan_scaled['SPEED ZONE'], kecelakaan_scaled['NO PERSONS KILLED'],
           s=(kecelakaan_scaled['DAY OF WEEK']+abs(kecelakaan_scaled['NO PERSONS KILLED'].min()))*100,
           c=kecelakaan_scaled['lbl_k9'].map(colorDict), alpha=0.75, zorder=2)

# plot the centroids
ax.scatter(centroidX, centroidY,
           s=(centroidZ+abs(min(centroidZ))+0.7)*100,
           c='black', marker='o', zorder=3)

ax.set_title('Cluster DAY OF WEEK (Hari) (K=9)\n', fontsize=16, weight='bold')
ax.set_xlabel('\nSpeed Zone (km)', fontsize=14, weight='bold')
ax.set_ylabel('No Persons Killed\n', fontsize=14, weight='bold')

# Create list of marker objects for legend parameter input
markers = [plt.Line2D([0,0],[0,0], color=color, marker='o', linestyle='') for color in colorDict.values()]

# Create the legend
plt.legend(markers, list(colorDict.keys())[:4], prop={'size':13},
           title='Cluster\n', title_fontsize=16)

plt.grid(color='white', zorder=0)

plt.show()

kecelakaan_data = kecelakaan_new[['DAY OF WEEK','NO PERSONS KILLED','SPEED ZONE']].copy()
kecelakaan_data

# Membuat object variabel linier regression

from sklearn.linear_model import LinearRegression
regressor = LinearRegression()

regressor.fit(X_train, y_train)

# Nilai slope/koefisien (m) dan intercept (b),
print(regressor.coef_)
print(regressor.intercept_)

regressor.score(X_test,y_test)

y_prediksi = regressor.predict(X_test)

# Mencari mean absolute error, mean squared error, dan root mean squared error

from sklearn import metrics 
 
print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_prediksi))  
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_prediksi))  
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_prediksi)))

plt.title('Perbandingan antara Y values ketika prediksi dan test')
plt.ylabel('Predicted values')
plt.xlabel('Test Set')
plt.plot(y_prediksi, '.', y_test, 'x')
plt.show()