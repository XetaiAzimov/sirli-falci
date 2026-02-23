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
    st.error("Secrets bölməsində məlumatlar tapılmadı!")
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
            # MODELİ TAPMAQ ÜÇÜN AGILLI SISTEM
            working_model = None
            # Google-un tanıya biləcəyi bütün mümkün model adları
            test_models = [
                'models/gemini-1.5-flash', 
                'models/gemini-1.5-flash-latest', 
                'models/gemini-pro',
                'gemini-1.5-flash',
                'gemini-pro'
            ]
            
            for m_name in test_models:
                try:
                    model = genai.GenerativeModel(m_name)
                    # Kiçik bir test sorğusu edirik
                    response = model.generate_content("Salam")
                    if response:
                        working_model = model
                        break
                except:
                    continue
            
            if working_model:
                try:
                    prompt = f"Sən peşəkar falçısan. {name} ({birth_date}) üçün Azərbaycan dilində maraqlı, pozitiv bir fal yaz."
                    final_response = working_model.generate_content(prompt)
                    
                    st.markdown("### ✨ Sənin Taleyin:")
                    st.write(final_response.text)
                    st.balloons()
                    send_telegram_msg(f"✅ Yeni Fal!\n👤 Ad: {name}\n📅 Doğum: {birth_date}\n🎫 Kod: {code}")
                except Exception as final_err:
                    st.error(f"Fal hazırlanarkən xəta: {str(final_err)}")
            else:
                st.error("Xəta: Google sənin API açarına heç bir model (Flash və ya Pro) üçün icazə vermir.")
                st.info("Zəhmət olmasa Google AI Studio-da 'Gemini API' bölməsində modelin aktiv olduğunu yoxla.")
    else:
        st.info("Zəhmət olmasa xanaları doldurun.")
