import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

df = pd.read_csv("dashboard/main_data.csv")
st.sidebar.title("Information:")
st.sidebar.markdown("**• Nama: Ferdian Razak**")
st.sidebar.markdown(
    "**• Email: [ferdianrazak77@gmail.com](ferdianrazak77@gmail.com)**")
st.sidebar.markdown(
    "**• Dicoding: [ferdianrazak](https://www.dicoding.com/users/ferdianrazak/)**")

df['Tahun'] = df['Tanggal'].dt.year
df['Bulan'] = df['Tanggal'].dt.month

def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by='Tanggal').agg({
        'Total_Sewa': 'sum'
    }).reset_index()
    return daily_rent_df

def create_daily_casual_rent_df(df):
    daily_casual_rent_df = df.groupby(by='Tanggal').agg({'Non-member': 'sum'}).reset_index()
    return daily_casual_rent_df

def create_daily_registered_rent_df(df):
    daily_registered_rent_df = df.groupby(by='Tanggal').agg({
        'Member': 'sum'
    }).reset_index()
    return daily_registered_rent_df
    
def create_season_rent_df(df):
    season_rent_df = df.groupby(by='Musim')[['Member', 'Non-member']].sum().reset_index()
    return season_rent_df

def create_monthly_rent_df(df):
    monthly_rent_df = df.groupby(by=['Tahun', 'Bulan']).agg({'Total_Sewa': 'sum'})
    order_bulan = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 
                'September', 'Oktober', 'November', 'Desember'
    ]
    monthly_rent_df = monthly_rent_df.reindex(order_bulan, fill_value=0)
    return monthly_rent_df

def create_weekday_rent_df(df):
    weekday_rent_df = df.groupby(by='Hari').agg({
        'Total_Sewa': 'sum'
    }).reset_index()
    return weekday_rent_df
    
def create_weather_rent_df(df):
    weather_rent_df = df.groupby(by='Cuaca')[['Member', 'Non-member']].sum().reset_index()
    return weather_rent_df
   
# Membuat komponen filter
min_date = pd.to_datetime(df ['Tanggal']).dt.date.min()
max_date = pd.to_datetime(df ['Tanggal']).dt.date.max()

start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )

main_df = df [(df['Tanggal'] >= str(start_date)) & (df['Tanggal'] <= str(end_date))]

# Menyiapkan berbagai dataframe
daily_rent_df = create_daily_rent_df(main_df)
daily_casual_rent_df = create_daily_casual_rent_df(main_df)
daily_registered_rent_df = create_daily_registered_rent_df(main_df)
season_rent_df = create_season_rent_df(main_df)
monthly_rent_df = create_monthly_rent_df(main_df)
weekday_rent_df = create_weekday_rent_df(main_df)
weather_rent_df = create_weather_rent_df(main_df)

monthly_rent_df = monthly_rent_df.transpose()
monthly_rent_df['Total_Sewa_2011'] = monthly_rent_df[2011]
monthly_rent_df['Total_Sewa_2012'] = monthly_rent_df[2012]

# Membuat Dashboard secara lengkap

# Membuat judul
st.header('Final Project Data Analytics - Bike Sharing Dataset')

# Membuat jumlah penyewaan bulanan
st.subheader('Tren jumlah pengguna perbulan pada 2011 dan 2012')
fig, ax = plt.subplots(figsize=(24, 8))
# Garis untuk tahun 2011
ax.plot(
    monthly_rent_df.index,
    monthly_rent_df['Total_Sewa_2011'],
    marker='o', 
    linewidth=2,
    color='tab:blue',
    label='2011'  # Label untuk legenda
)
# Garis untuk tahun 2012
ax.plot(
    monthly_rent_df.index,
    monthly_rent_df['Total_Sewa_2012'],
    marker='o', 
    linewidth=2,
    color='tab:red',
    label='2012'  # Label untuk legenda
)

# Tambahkan teks jumlah sewa untuk setiap bulan untuk kedua tahun
for index, (sewa2011, sewa2012) in enumerate(zip(monthly_rent_df['Total_Sewa_2011'], monthly_rent_df['Total_Sewa_2012'])):
    ax.text(index, sewa2011 + 1, str(sewa2011), ha='center', va='bottom', fontsize=12, color='blue')
    ax.text(index, sewa2012 + 1, str(sewa2012), ha='center', va='bottom', fontsize=12, color='red')

# Pengaturan untuk sumbu x dan y
ax.tick_params(axis='x', labelsize=25, rotation=45)
ax.tick_params(axis='y', labelsize=20)

# Menambahkan legenda untuk membedakan antara data tahun 2011 dan 2012
ax.legend(fontsize=20)

# Tampilkan plot
st.pyplot(fig)

# Membuah jumlah penyewaan berdasarkan kondisi cuaca
st.subheader('Jumlah sewa berkaitan dengan cuaca')
fig, ax = plt.subplots(figsize=(16, 8))

sns.barplot(
    x='Cuaca',
    y='Member',
    data=weather_rent_df,
    label='Member',
    ax=ax
)

sns.barplot(
    x='Cuaca',
    y='Non-member',
    data=weather_rent_df,
    label='Non-member',
    ax=ax
)

for index, row in weather_rent_df.iterrows():
    ax.text(index, row['Member'], str(row['Member']), ha='center', va='bottom', fontsize=12)
    ax.text(index, row['Non-member'], str(row['Non-member']), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20, rotation=0)
ax.tick_params(axis='y', labelsize=15)
ax.legend()
st.pyplot(fig)

# Membuat jumlah penyewaan berdasarkan musim
st.subheader('Jumlah sewa berkaitan dengan musim')
fig, ax = plt.subplots(figsize=(16, 8))

sns.barplot(
    x='Musim',
    y='Member',
    data=season_rent_df,
    label='Member',
    ax=ax
)

sns.barplot(
    x='Musim',
    y='Non-member',
    data=season_rent_df,
    label='Non-member',
    ax=ax
)

for index, row in season_rent_df.iterrows():
    ax.text(index, row['Member'], str(row['Member']), ha='center', va='bottom', fontsize=12)
    ax.text(index, row['Non-member'], str(row['Non-member']), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20, rotation=0)
ax.tick_params(axis='y', labelsize=15)
ax.legend()
st.pyplot(fig)

st.caption('Copyright (c) Ferdian Razak 2024')
