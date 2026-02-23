import streamlit as st
import google.generativeai as genai
import requests
from datetime import datetime

# Secrets
GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
TELEGRAM_TOKEN = st.secrets["TELEGRAM_BOT_TOKEN"]
CHAT_ID = st.secrets["TELEGRAM_CHAT_ID"]

genai.configure(api_key=GEMINI_KEY)

def send_telegram_msg(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message}
        requests.post(url, json=payload)
    except:
        pass

st.set_page_config(page_title="Sirli Falçı", page_icon="🔮")

# Dizaynı bir az gözəlləşdirək
st.title("🔮 Sirli Falçı")
st.markdown("---")
st.write("Ulduzlar sənin üçün nə hazırlayıb? Doğum tarixini və adını yaz, taleyini öyrən.")

# Girişlər
name = st.text_input("Adınız:", placeholder="Məsələn: Leyla")
birth_date = st.date_input("Doğum tarixiniz:", min_value=datetime(1950, 1, 1), max_value=datetime.now())
code = st.text_input("Ödəniş Kodunuz:", placeholder="FAL2026")

if st.button("Ulduzları Soruş ☕"):
    if name and code:
        with st.spinner('Planetlərin hərəkəti izlənilir...'):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Gemini-yə doğum tarixini də göndəririk ki, bürclə bağlı danışsın
                prompt = f"""
                Sən sirli və uzaqgörən bir falçısan. 
                Adı {name} olan və doğum tarixi {birth_date} olan bir şəxs üçün Azərbaycan dilində maraqlı fal yaz. 
                Onun doğum tarixinə görə bürcünü müəyyən et və gələcəyi haqqında sirli, müsbət proqnozlar ver.
                """
                
                response = model.generate_content(prompt)
                
                if response.text:
                    st.markdown("### ✨ Sənin Taleyin:")
                    st.write(response.text)
                    st.balloons()
                    
                    # Telegram bildirişi
                    notif = f"🔮 Yeni Fal!\n👤 Ad: {name}\n📅 Doğum: {birth_date}\n🎫 Kod: {code}"
                    send_telegram_msg(notif)
                else:
                    st.warning("Ulduzlar hazırda görünmür, bir az sonra yoxla.")

            except Exception as e:
                st.error(f"Xəta: {str(e)}")
    else:
        st.info("Zəhmət olmasa adınızı və kodunuzu daxil edin.")
