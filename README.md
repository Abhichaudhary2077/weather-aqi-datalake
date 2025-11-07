📘 Overview

This project is a real-time environmental monitoring system that fetches live weather and air quality (AQI) data for any city using the OpenWeatherMap API, and logs it into a local data lake (CSV-based storage).
It also includes visual dashboards built with Streamlit to monitor temperature, humidity, wind speed, and AQI trends over time.

🧩 Key Features

✅ Real-time Weather + AQI fetching
✅ Automatic logging to a data lake (CSV per city)
✅ Interactive dashboard using Streamlit + Altair
✅ Auto-refresh option (every 10 minutes)
✅ Integrated version control using Git + GitHub

🏗️ Architecture Flow
        ┌────────────────────────────┐
        │     Streamlit Frontend     │
        │  (User inputs city name)   │
        └────────────┬───────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │ OpenWeatherMap API         │
        │ Fetch live Weather + AQI   │
        └────────────┬───────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │  Data Lake (CSV Storage)   │
        │ Auto-append for each city  │
        └────────────┬───────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │ Streamlit Visualization    │
        │ Line charts + Tables       │
        └────────────────────────────┘

⚙️ Tech Stack & Tools Used
Category	Tools / Skills
Frontend	Streamlit, Altair
Backend / Data Fetching	Python, Requests
Data Processing	Pandas
Storage	Local CSV Data Lake
Version Control	Git + GitHub
Collaboration	ChatGPT (AI Assistant Guidance)
📦 Installation

Clone this repository

git clone https://github.com/Abhichaudhary2077/weather-aqi-datalake.git
cd weather-aqi-datalake


Install dependencies

pip install -r requirements.txt


Run the Streamlit dashboard

streamlit run app.py


Enter your OpenWeatherMap API key in app.py

api_key = "YOUR_API_KEY"

📈 Example Output

Dashboard Metrics

🌡 Temperature

💧 Humidity

💨 Wind Speed

🌫 AQI Level

Chart Visualization
Altair line chart displaying temperature and AQI trends.

🕒 Auto-Refresh & Logging

The dashboard fetches data automatically every 10 minutes.

Each city gets its own log file inside data_lake/, e.g.

data_lake/Delhi_weather_aqi.csv
data_lake/Mumbai_weather_aqi.csv

💬 Acknowledgments

This project was fully built by Abhi Choudhary
with AI guidance and co-development support from ChatGPT (GPT-5).

“A human–AI collaboration project demonstrating modern data engineering & visualization workflows.”README.md
