import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")

def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "main_data.csv")
    
    df = pd.read_csv(file_path)
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

all_df = load_data()

with st.sidebar:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "bicycle.png")
    
    st.image(file_path, width=100)
    st.title("Filter Data")
    
    min_date = all_df["dteday"].min()
    max_date = all_df["dteday"].max()
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
main_df = all_df[(all_df["dteday"] >= str(start_date)) & (all_df["dteday"] <= str(end_date))]

st.title("🚲 Bike Sharing Dashboard")
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    total_orders = main_df['total_count'].sum()
    st.metric("Total Sharing", value=f"{total_orders:,}")

with col2:
    daily_avg = main_df.groupby('dteday')['total_count'].sum().mean()
    st.metric("Rata-rata Harian", value=f"{daily_avg:,.0f}")

with col3:
    max_order_day = main_df.groupby('dteday')['total_count'].sum().max()
    st.metric("Rekor Harian Terbanyak", value=f"{max_order_day:,}")

st.markdown("---")

st.subheader("1. Pengaruh Musim & Cuaca")

col_viz1, col_viz2 = st.columns(2)

with col_viz1:
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.barplot(x="season", y="total_count", data=main_df, palette="Blues_d", errorbar=None, ax=ax1)
    ax1.set_title("Rata-rata Harian per Musim")
    ax1.set_xlabel(None)
    ax1.set_ylabel(None)
    st.pyplot(fig1)

with col_viz2:
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.barplot(x="weather_cond", y="total_count", data=main_df, palette="Reds_d", errorbar=None, ax=ax2)
    ax2.set_title("Rata-rata Sewa per Kondisi Cuaca (Per Jam)")
    ax2.set_xlabel(None)
    ax2.set_ylabel(None)
    st.pyplot(fig2)
    
st.subheader("2. Pola Jam Sibuk (Time of Day)")

fig_time, ax_time = plt.subplots(figsize=(10, 5))
sns.barplot(
    x="time_of_day", 
    y="total_count", 
    data=main_df, 
    order=['Morning', 'Afternoon', 'Evening'],
    palette="viridis",
    errorbar=None,
    ax=ax_time
)
ax_time.set_title("Distribusi Penyewaan Berdasarkan Waktu", fontsize=14)
ax_time.set_xlabel(None)
ax_time.set_ylabel(None)
st.pyplot(fig_time)

st.subheader("3. Analisis Kategori Suhu (Binning)")

fig_temp, ax_temp = plt.subplots(figsize=(10, 5))
sns.barplot(
    x="temp_category", 
    y="total_count", 
    data=main_df,
    order=['Cold', 'Mild', 'Hot'],
    palette="coolwarm",
    errorbar=None,
    ax=ax_temp
)
ax_temp.set_title("Distribusi Penyewaan Berdasarkan Kategori Suhu", fontsize=14)
ax_temp.set_xlabel(None)
ax_temp.set_ylabel(None)
st.pyplot(fig_temp)