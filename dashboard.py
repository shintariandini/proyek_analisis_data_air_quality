# Import library yang dibutuhkan
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Load dataset
all_df = pd.read_csv("./dataset_project.csv")


# Get the range of years
min_year = all_df["year"].min()
max_year = all_df["year"].max()

# Sidebar configuration
with st.sidebar:
    # Memilih tahun
    start_year, end_year = st.select_slider(
        label='Filter Tahun',
        options=list(range(min_year, max_year + 1)),
        value=(min_year, max_year)
    )

# Filter data berdasarkan tahun
filtered_df = all_df[(all_df["year"] >= start_year) & (all_df["year"] <= end_year)]

# Pilih kolom numerik saja untuk analisis korelasi
numeric_columns = filtered_df[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']]

# Hitung matriks korelasi
correlation_matrix = numeric_columns.corr()

st.header('Air Quality Analysis Dongsi vs Tiantan :sparkles:')

# Visualisasi matriks korelasi dengan heatmap
st.subheader("Analisis Korelasi")
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True, ax=ax)
plt.title("Heatmap Korelasi")
st.pyplot(fig)

st.markdown(
    """
    Terdapat hubungan positif antara indikator PM2.5, PM10, SO2, NO2, dan CO. 
    Sedangkan indikator O3 bernilai negatif yang artinya memiliki hubungan yang lemah atau tidak kuat.
    """
)

st.subheader("Visualisasi Indikator Polutan Per Tahun")

# Memisah data untuk Dongsi dan Tiantan
dongsi_data = filtered_df[filtered_df['station'] == 'Dongsi']
tiantan_data = filtered_df[filtered_df['station'] == 'Tiantan']

# Mengelompokkan data berdasarkan tahun dengan nilai rata-ratanya 
year_dongsi = dongsi_data.groupby("year").mean(numeric_only=True)
year_tiantan = tiantan_data.groupby("year").mean(numeric_only=True)

# VISUALISASI GABUNGAN
fig = plt.figure(figsize=(10, 6))
# Menambahkan trend line dari Dongsi
for column in ["PM2.5", "PM10", "SO2", "NO2", "O3"]:
    plt.plot(year_dongsi.index, year_dongsi[column], marker="o", label=f"{column} (Dongsi)", linestyle="-")

# Menambahkan trend line dari Tiantan
for column in ["PM2.5", "PM10", "SO2", "NO2", "O3"]:
    plt.plot(year_tiantan.index, year_tiantan[column], marker="x", label=f"{column} (Tiantan)", linestyle="--")

# Menambahkan judul, label, dan legenda
plt.title("Trend Line Rata-rata Indikator Polutan Udara per Tahun (Dongsi vs Tiantan)", fontsize=16)
plt.xlabel("Tahun", fontsize=12)
plt.ylabel("Rata-rata Konsentrasi (μg/m³)", fontsize=12)
plt.xticks(year_dongsi.index, fontsize=10)
plt.legend(title="Indikator dan Lokasi", fontsize=10, bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(alpha=0.5)

# Menampilkan plot
plt.tight_layout()
st.pyplot(fig)

st.markdown(
    """
  Indikator PM2.5 , PM10, SO2, NO2, dan CO (5 dari 6 indikator polutan) mengalami kenaikan yang signifikan ditahun akhir (tahun 2017) dan memiliki nilai terendah pada tahun 2016. Rata-rata dari setiap indikator stasiun Tiantan lebih rendah daripada stasiun Dongsi. 
"""
)

## VISUALISASI CO
fig = plt.figure(figsize=(10, 6))

# Menambahkan trend line dari Dongsi
plt.plot(year_dongsi.index, year_dongsi["CO"], marker="o", label=f"CO (Dongsi)", linestyle="-")

# Menambahkan trend line dari Tiantan
plt.plot(year_tiantan.index, year_tiantan["CO"], marker="x", label=f"CO (Tiantan)", linestyle="--")

# Menambahkan judul, label, dan legenda
plt.title("Trend Line Rata-rata Indikator Polutan Udara per Tahun (CO)", fontsize=16)
plt.xlabel("Tahun", fontsize=12)
plt.ylabel("Rata-rata Konsentrasi (μg/m³)", fontsize=12)
plt.xticks(year_dongsi.index, fontsize=10)
plt.legend(title="Indikator dan Lokasi", fontsize=10, bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(alpha=0.5)

# Menampilkan plot
plt.tight_layout()
st.pyplot(fig)

st.markdown(
    """
    Untuk indikator parameter CO memiliki nilai tertinggi di stasiun Tiantan pada tahun 2017 hingga mencapai angka 1700-an.
    """
)

st.subheader("Visualisasi Persentase Perbandingan Polutan di Kedua Stasiun")
# Menghitung rata-rata polutan untuk setiap stasiun
mean_values =filtered_df.groupby("station")[["PM2.5", "PM10", "CO", "NO2", "SO2", "O3"]].mean()
print(mean_values) 

# Membuat figure untuk 6 diagram pie
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
axes = axes.flatten()  # Mempermudah iterasi dengan axes dalam bentuk array

# Daftar warna untuk pie chart
colors = [["#FF9999", "#9999FF"], ["#FFC1C1", "#B0C4DE"], ["#FFA07A", "#87CEFA"],
          ["#FF6347", "#4682B4"], ["#FFD700", "#4169E1"], ["#FF4500", "#6495ED"]]

# Membuat diagram pie untuk masing-masing polutan
for i, polutan in enumerate(mean_values.columns):
    ax = axes[i]
    ax.pie(
        mean_values[polutan],  # Data untuk pie chart
        labels=mean_values.index,  # Label berdasarkan stasiun
        autopct="%1.1f%%",  # Format persentase
        startangle=90,  # Rotasi awal
        colors=colors[i],  # Warna untuk setiap pie
        wedgeprops={"edgecolor": "black"}  # Garis tepi pie
    )
    ax.set_title(f"Rata-rata {polutan}", fontsize=14)

# Menambahkan judul besar untuk keseluruhan figure
fig.suptitle("Perbandingan Rata-rata Konsentrasi Polutan (Pie Chart)", fontsize=18)

# Menyesuaikan tata letak
plt.tight_layout(rect=[0, 0, 1, 0.95])  # Memberi ruang untuk judul besar
st.pyplot(fig)

st.markdown(
    """
     Stasiun Tiantan Memiliki Kualitas Udara yang Lebih Baik dibandingkan Stasiun Dongsi karena kualitas udara di Stasiun Dongsi memiliki jumlah polutan yang lebih banyak (persentase diatas 50% disemua indikator polutannya) dibanding dengan Stasiun Tiantan.
    """
)
