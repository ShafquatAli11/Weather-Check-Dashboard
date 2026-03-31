import streamlit as st
import requests

# 1. Page Configuration
st.set_page_config(
    page_title="SkyCheck | Global Weather Dashboard", 
    page_icon="🌡️",
    layout="wide" # Dashboard ke liye wide layout behtar hai
)

# 2. Modern UI Styling (Glassmorphism effect)
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background: linear-gradient(45deg, #007bff, #00d2ff);
        color: white;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,123,255,0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar for Settings & History
with st.sidebar:
    st.header("⚙️ Settings")
    unit_choice = st.radio("Choose Temperature Unit:", ["Celsius", "Fahrenheit"])
    unit_type = "metric" if unit_choice == "Celsius" else "imperial"
    symbol = "°C" if unit_choice == "Celsius" else "°F"
    
    st.markdown("---")
    st.info("💡 **Tip:** Check spelling for accurate results.")

# 4. Main Dashboard Header
col_title, col_icon = st.columns([4, 1])
with col_title:
    st.title("🌡️ SkyCheck Dashboard")
    st.write("Real-time meteorological insights for data-driven decisions.")

# 5. Input Section
city = st.text_input("", placeholder="Enter city name (e.g. Islamabad, London...)", label_visibility="collapsed")

API_KEY = "3e54cac6b28374baff88a1a12561062d"

if st.button("Analyze Weather"):
    if city.strip():
        with st.spinner('Accessing Global Satellite Data...'):
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={unit_type}"
            
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    
                    # Data Extraction
                    temp = data['main']['temp']
                    humidity = data['main']['humidity']
                    wind = data['wind']['speed']
                    desc = data['weather'][0]['description']
                    icon = data['weather'][0]['icon']
                    feels_like = data['main']['feels_like']
                    
                    st.markdown(f"### 📍 Weather in {city.capitalize()}")
                    
                    # Row 1: Key Metrics
                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Temperature", f"{temp}{symbol}")
                    m2.metric("Feels Like", f"{feels_like}{symbol}")
                    m3.metric("Humidity", f"{humidity}%")
                    m4.metric("Wind Speed", f"{wind} m/s")
                    
                    # Row 2: Visual Summary
                    st.markdown("---")
                    res_col1, res_col2 = st.columns([1, 2])
                    with res_col1:
                        st.image(f"http://openweathermap.org/img/wn/{icon}@4x.png", width=200)
                    with res_col2:
                        st.subheader("Condition Summary")
                        st.write(f"The current sky condition is **{desc.capitalize()}**.")
                        if temp > 30:
                            st.warning("It's quite hot outside. Stay hydrated!")
                        elif temp < 15:
                            st.info("It's a bit chilly. A light jacket is recommended.")
                        else:
                            st.success("The weather seems pleasant today!")
                
                elif response.status_code == 404:
                    st.error("❌ City not found. Please verify the name.")
                else:
                    st.error("⚠️ Service temporarily unavailable.")
            
            except Exception:
                st.error("📡 Network Error. Please check your connection.")
    else:
        st.warning("Please enter a city name.")

# 6. Professional Footer
st.markdown("---")
footer_col1, footer_col2 = st.columns(2)
with footer_col1:
    st.caption("Developed by **Shafquat Ali** | Computer Science Student")
with footer_col2:
    st.markdown("<p style='text-align: right; color: grey;'>Data Source: OpenWeatherMap API</p>", unsafe_allow_html=True)