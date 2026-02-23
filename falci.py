import streamlit as st
import google.generativeai as genai
import requests
from datetime import datetime

# Secrets-dən dataları oxuyuruq
try:
    GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
    TELEGRAM_TOKEN = st.secrets["TELEGRAM_BOT_TOKEN"]
    CHAT_ID = st.secrets["TELEGRAM_CHAT_ID"]
except Exception as e:
    st.error("Secrets (Şifrələr) bölməsində məlumatlar tapılmadı!")
    st.stop()

# API Konfiqurasiyası
genai.configure(api_key=GEMINI_KEY)

def send_telegram_msg(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": message})
    except:
        pass

st.set_page_config(page_title="Sirli Falçı", page_icon="🔮")
st.title("🔮 Sirli Falçı")

name = st.text_input("Adınız:", placeholder="Məsələn: Murad")
birth_date = st.date_input("Doğum tarixiniz:", min_value=datetime(1950, 1, 1))
code = st.text_input("Ödəniş Kodunuz:", placeholder="FAL2026")

if st.button("Ulduzları Soruş ☕"):
    if name and code:
        with st.spinner('Ulduzlarla əlaqə qurulur...'):
            try:
                # ƏN STABİL MODEL ADI
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"Sən peşəkar falçısan. {name} ({birth_date}) üçün Azərbaycan dilində maraqlı, pozitiv bir fal yaz."
                response = model.generate_content(prompt)
                
                if response.text:
                    st.markdown("### ✨ Sənin Taleyin:")
                    st.write(response.text)
                    st.balloons()
                    
                    # Telegram bildirişi
                    send_telegram_msg(f"✅ Müştəri gəldi!\n👤 Ad: {name}\n📅 Doğum: {birth_date}\n🎫 Kod: {code}")
                else:
                    st.error("Ulduzlar susur. API Key-in aktivliyini yoxlayın.")

            except Exception as e:
                # Xətanın tam kodunu burada göstərəcək ki, səbəbi bilək
                st.error(f"Xəta baş verdi: {str(e)}")
    else:
        st.info("Zəhmət olmasa xanaları doldurun.")
