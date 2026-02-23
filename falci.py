import streamlit as st
import google.generativeai as genai
import requests

# Secrets
GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
TELEGRAM_TOKEN = st.secrets["TELEGRAM_BOT_TOKEN"]
CHAT_ID = st.secrets["TELEGRAM_CHAT_ID"]

# Gemini Ayarı
genai.configure(api_key=GEMINI_KEY)

def send_telegram_msg(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message}
        requests.post(url, json=payload)
    except:
        pass

st.set_page_config(page_title="Sirli Falçı", page_icon="🔮")
st.title("🔮 Sirli Falçı")

name = st.text_input("Adınız:", placeholder="Məsələn: Leyla")
code = st.text_input("Ödəniş Kodunuz:", placeholder="Məsələn: FAL2026")

if st.button("Falıma Bax ☕"):
    if name and code:
        with st.spinner('Ulduzlarla əlaqə qurulur...'):
            try:
                # Ən stabil modeli seçirik
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"{name} adlı şəxs üçün Azərbaycan dilində maraqlı, sirli və pozitiv bir fal yaz.")
                
                st.success(f"Hörmətli {name}, ulduzlar sizin üçün danışdı:")
                st.write(response.text)
                st.balloons()
                
                # Sənə bildiriş göndərir
                send_telegram_msg(f"✅ Yeni müştəri!\n👤 Ad: {name}\n🎫 Kod: {code}")
                
            except Exception as e:
                # Əgər 1.5-flash işləməsə, digərini yoxla
                try:
                    model = genai.GenerativeModel('gemini-pro')
                    response = model.generate_content(f"{name} üçün Azərbaycan dilində fal yaz.")
                    st.write(response.text)
                except:
                    st.error("Ulduzlar hazırda bir az dumanlı görünür, az sonra yenidən yoxlayın.")
    else:
        st.info("Davam etmək üçün adınızı və kodunuzu daxil edin.")
