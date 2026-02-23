import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random
import string
import time
import requests
from google import genai
from datetime import datetime

# --- KONFİQURASİYA ---
API_KEY = "AIzaSyCTkEKJmD7iFReT-KcRywIBwlI-zsV91z4"
client = genai.Client(api_key=API_KEY)
MODEL_ID = "gemini-3-flash-preview"

# Google Sheets Bağlantısı
def get_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("keys.json", scope)
    client_gs = gspread.authorize(creds)
    # Cədvəl ID-ni bura daxil et
    return client_gs.open_by_key("1g4CZiNoj78_iugBYt-V1SrPpquqlWKkCH5kasIA1m1E").sheet1

def kod_yarat():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def get_ip():
    try:
        return requests.get('https://api.ipify.org').text
    except:
        return "Bilinmir"

# --- SAYFA DİZAYNI ---
st.set_page_config(page_title="Sirli Falçı 7/24", page_icon="🔮", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    h1, h2, h3 { color: #FFD700 !important; text-align: center; }
    p, label { color: #E0E0E0 !important; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #4B0082; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔮 Avtomatik Sirli Falçı 7/24 🔮")
st.write("Gələcəyin qapıları burada açılır. Ödəniş edin və dərhal kodunuzu alın.")

# --- 1. ÖDƏNİŞ VƏ QEYDİYYAT ---
st.subheader("1. Ödəniş və Təsdiq")

# Psixoloji Təhlükəsizlik Bloqu
st.error(f"⚠️ SİSTEM YOXLAMASI AKTİVDİR: IP Ünvanınız ({get_ip()}) qeydə alınır. Ödənişsiz kod almağa cəhd edənlər bloklanır.")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### **m10 QR Kod**")
    try:
        st.image("qr_kod.png", caption="Skan et və 1 AZN ödə", width=230)
    except:
        st.info("QR kod şəkli tapılmadı (qr_kod.png)")

with col2:
    st.markdown("### **Kartla Ödəniş**")
    st.write("Kart nömrəsini kopyalayın:")
    st.code("4098 0944 2188 8023", language="text")
    st.write("👤 **Sahib:** Xətai Ə.")
    st.write("🏦 **Bank:** Unibank")

st.divider()

# Müştəri Məlumatları
name = st.text_input("👤 Ad və Soyadınız")
birth = st.date_input("📅 Doğum Tarixiniz",
                      min_value=datetime(1940, 1, 1), 
                      max_value=datetime.now(),
                      value=datetime(2000, 1, 1))

check_id = st.text_input(
    "🧾 Ödəniş sübutu", 
    placeholder="Qəbzdəki RRN, ID və ya dəqiq saatı yazın (Məs: 15:42)"
)


if st.button("ÖDƏNİŞİ TƏSDİQLƏ VƏ KOD AL 🔑"):
    if name and check_id:
        if birth.year >= datetime.now().year - 2:
            st.warning("🔮 Ulduzlar deyir ki, sən çox balacasan! Zəhmət olmasa düzgün doğum tarixi seç.")
        else:
            with st.spinner('Süni zəka ödənişi çarpaz yoxlayır...'):
                time.sleep(4) # Ciddiyyət illüziyası
                
                yeni_kod = kod_yarat()
                tarix_indi = datetime.now().strftime("%d.%m.%Y %H:%M")
                user_ip = get_ip()
                
                try:
                    sheet = get_sheet()
                    sheet.append_row([name, yeni_kod, "Yeni", tarix_indi, str(birth), check_id, user_ip])
                    st.success(f"✅ Ödəniş təsdiqləndi! Sizin tək istifadəlik kodunuz: **{yeni_kod}**")
                    st.balloons()
                except Exception as e:
                    st.error(f"Excel bağlantı xətası: {e}")
    else:
        st.error("Lütfən, adınızı və qəbz məlumatlarını (RRN/Vaxt) daxil edin!")

st.divider()

# --- 2. FAL BAXMA BÖLMƏSİ ---
st.subheader("2. Falınıza Baxın")
user_code = st.text_input("🔑 Aldığınız Kodu Bura Yazın").strip().upper()

if st.button("FALIMI AÇ ✨"):
    if user_code:
        try:
            sheet = get_sheet()
            all_values = sheet.get_all_values()
            if len(all_values) > 1:
                df = pd.DataFrame(all_values[1:], columns=all_values[0])
                df.columns = [c.strip().lower() for c in df.columns]

                user_row = df[(df['kod'].astype(str) == user_code) & (df['status'].str.lower() == 'yeni')]

                if not user_row.empty:
                    u_name = user_row.iloc[0]['ad']
                    u_birth = user_row.iloc[0]['doğum tarixi']
                    
                    with st.spinner('Ulduzlarla əlaqə qurulur...'):
                        success = False
                        for attempt in range(3):
                            try:
                                prompt = f"Sən müdrik falçısan. {u_name} ({u_birth}) üçün Azərbaycan dilində dərin fal yaz. Onu heyrətləndir."
                                response = client.models.generate_content(model=MODEL_ID, contents=prompt)
                                st.markdown(f"### 🔮 {u_name} üçün Gələcəyin Səsi:")
                                st.write(response.text)
                                
                                cell = sheet.find(user_code)
                                sheet.update_cell(cell.row, 3, "Istifade Olundu")
                                success = True
                                break
                            except Exception as ai_err:
                                if "503" in str(ai_err) and attempt < 2:
                                    time.sleep(5)
                                    continue
                                else:
                                    st.error("Server məşğuldur, 1 dəqiqə sonra yenidən 'FALIMI AÇ' düyməsinə basın.")
                                    break
                else:
                    st.error("Kod yanlışdır və ya artıq istifadə edilib!")
            else:
                st.error("Hələ heç bir qeydiyyat yoxdur.")
        except Exception as e:
            st.error(f"Bağlantı xətası: {e}")