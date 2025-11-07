import streamlit as st
import requests
import pandas as pd
import altair as alt
import os
from datetime import datetime, timedelta
import time

# === Streamlit Page Setup ===
st.set_page_config(page_title="🌤️ Weather & AQI Data Lake", layout="wide")
st.title("🌤️ Live Weather & AQI Data Lake Dashboard")
st.caption("Real-time environmental monitoring with automatic updates every 10 minutes")

# === User Inputs ===
api_key = "546417e943dbf71ee0c2cc4d210bd6b5"  # your OpenWeatherMap API key
city = st.text_input("Enter City Name:", "Delhi")

# === Create data_lake directory if not exists ===
os.makedirs("data_lake", exist_ok=True)
log_file = f"data_lake/{city}_weather_aqi.csv"

# === Initialize session state ===
if "last_update" not in st.session_state:
    st.session_state.last_update = datetime.now() - timedelta(minutes=11)  # force first update


# === Fetch weather + AQI data ===
def fetch_weather_aqi(city):
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    weather_data = requests.get(weather_url).json()

    if "coord" in weather_data:
        lat, lon = weather_data["coord"]["lat"], weather_data["coord"]["lon"]
        aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
        aqi_data = requests.get(aqi_url).json()
    else:
        aqi_data = {}
    return weather_data, aqi_data


# === Log data into CSV ===
def log_data(city, weather_data, aqi_data):
    if "main" not in weather_data:
        return None

    temp = weather_data["main"]["temp"]
    humidity = weather_data["main"]["humidity"]
    wind = weather_data["wind"]["speed"]
    desc = weather_data["weather"][0]["description"]
    aqi = aqi_data.get("list", [{}])[0].get("main", {}).get("aqi", None)

    new_entry = {
        "timestamp": datetime.now(),
        "city": city,
        "temperature": temp,
        "humidity": humidity,
        "wind_speed": wind,
        "description": desc,
        "aqi": aqi
    }

    df_new = pd.DataFrame([new_entry])
    if os.path.exists(log_file):
        df_existing = pd.read_csv(log_file)
        df = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df = df_new
    df.to_csv(log_file, index=False)
    return df_new


# === Display data chart + table ===
def display_data(city):
    if os.path.exists(log_file):
        df = pd.read_csv(log_file)
        df["timestamp"] = pd.to_datetime(df["timestamp"])

        st.subheader(f"📊 Historical Data for {city}")
        temp_chart = alt.Chart(df).mark_line(point=True).encode(
            x="timestamp:T",
            y="temperature:Q",
            color=alt.value("#1f77b4")
        ).properties(title="Temperature Trend Over Time")

        st.altair_chart(temp_chart, use_container_width=True)
        st.dataframe(df.tail(10))
    else:
        st.warning("No historical data yet. Fetch once to start logging.")


# === Auto-fetch every 10 min ===
now = datetime.now()
if (now - st.session_state.last_update).total_seconds() > 600:
    weather_data, aqi_data = fetch_weather_aqi(city)
    if "main" in weather_data:
        log_data(city, weather_data, aqi_data)
        st.session_state.last_update = now
        st.toast(f"🔄 Auto-updated data for {city} at {now.strftime('%H:%M:%S')}")
    else:
        st.error("❌ City not found or API limit reached!")


# === Manual Fetch Button ===
if st.button("Fetch Now"):
    weather_data, aqi_data = fetch_weather_aqi(city)
    if "main" in weather_data:
        log_data(city, weather_data, aqi_data)
        st.session_state.last_update = datetime.now()
        st.success("✅ Data updated successfully!")
    else:
        st.error("❌ Failed to fetch data. Please check city name or API key.")


# === Display latest metrics ===
if os.path.exists(log_file):
    df = pd.read_csv(log_file)
    latest = df.iloc[-1]
    st.metric("🌡 Temperature (°C)", latest["temperature"])
    st.metric("💧 Humidity (%)", latest["humidity"])
    st.metric("💨 Wind Speed (m/s)", latest["wind_speed"])
    st.metric("🌫 AQI Level", latest["aqi"])

# === Show history ===
display_data(city)

# === Info ===
st.info("⏳ Auto-fetches & saves new data every 10 minutes automatically.")
