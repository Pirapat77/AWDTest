import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import numpy as np

# ฟังก์ชันดึงข้อมูลจาก Google Sheets
def load_data_from_gsheet(sheet_url, sheet_name):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('your_credentials.json', scope)
    client = gspread.authorize(creds)
    
    sheet = client.open_by_url(sheet_url).worksheet(sheet_name)
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# ฟังก์ชันคำนวณค่า Penman-Monteith (ตัวอย่างค่า)
def penman_monteith(temp, humidity, wind_speed, radiation):
    # ค่าคงที่ที่ใช้ในการคำนวณ
    delta = 4098 * (0.6108 * np.exp((17.27 * temp) / (temp + 237.3))) / (temp + 237.3) ** 2
    gamma = 0.665 * 10**-3
    eto = (0.408 * delta * radiation + gamma * (900 / (temp + 273)) * wind_speed * (humidity)) / (delta + gamma * (1 + 0.34 * wind_speed))
    return eto

# หน้าจอหลัก Streamlit
st.title("Penman-Monteith Calculation")

# รับค่า URL ของ Google Sheets และชื่อแผ่น
sheet_url = st.text_input("Enter Google Sheets URL")
sheet_name = st.text_input("Enter Sheet Name")

if sheet_url and sheet_name:
    # โหลดข้อมูล
    data = load_data_from_gsheet(sheet_url, sheet_name)
    st.write("Loaded Data from Google Sheets:")
    st.write(data)
    
    # คำนวณค่า Penman-Monteith
    if not data.empty:
        data['ETo'] = data.apply(lambda row: penman_monteith(row['Temp'], row['Humidity'], row['WindSpeed'], row['Radiation']), axis=1)
        st.write("Penman-Monteith ETo Calculations:")
        st.write(data)
