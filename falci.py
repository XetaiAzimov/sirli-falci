import streamlit as st
import google.generativeai as genai
import requests
from datetime import datetime

# Secrets
GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
TELEGRAM_TOKEN = st.secrets["TELEGRAM_BOT_TOKEN"]
CHAT_ID = st.secrets["TELEGRAM_CHAT_ID"]

# Gemini Konfiqurasiyası
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
st.write("Ən son süni zəka texnologiyası ilə gələcəyinə bax...")

name = st.text_input("Adınız:", placeholder="Məsələn: Murad")
birth_date = st.date_input("Doğum tarixiniz:", min_value=datetime(1950, 1, 1))
code = st.text_input("Ödəniş Kodunuz:", placeholder="FAL2026")

if st.button("Ulduzları Soruş ☕"):
    if name and code:
        with st.spinner('Süni zəka ulduzları skan edir...'):
            # Modelləri sıra ilə yoxlayırıq - Ən yeni 2.0-dan başlayaraq
            model_list = [
                'gemini-2.0-flash-exp', 
                'gemini-1.5-flash', 
                'gemini-pro'
            ]
            
            success = False
            for m_name in model_list:
                try:
                    model = genai.GenerativeModel(m_name)
                    prompt = f"Sən peşəkar falçısan. {name} ({birth_date}) üçün Azərbaycan dilində maraqlı fal yaz."
                    response = model.generate_content(prompt)
                    
                    if response.text:
                        st.markdown("### ✨ Sənin Taleyin:")
                        st.write(response.text)
                        st.balloons()
                        send_telegram_msg(f"✅ Yeni Fal!\n👤 Ad: {name}\n📅 Doğum: {birth_date}\n🎫 Kod: {code}")
                        success = True
                        break
                except:
                    continue
            
            if not success:
                st.error("Ulduzlar hazırda əlçatmazdır. Zəhmət olmasa API Key-in aktiv olduğunu Google AI Studio-da yoxlayın.")
    else:
        st.info("Məlumatları doldurun.")
