import streamlit as st
from groq import Groq
import requests
from datetime import datetime

# Secrets yoxlanışı
try:
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
    TELEGRAM_TOKEN = st.secrets["TELEGRAM_BOT_TOKEN"]
    CHAT_ID = st.secrets["TELEGRAM_CHAT_ID"]
except Exception as e:
    st.error("Secrets bölməsində məlumatlar tapılmadı!")
    st.stop()

# Groq müştərisini başladırıq
client = Groq(api_key=GROQ_KEY)

def send_telegram_msg(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": message})
    except:
        pass

st.set_page_config(page_title="Sirli Falçı", page_icon="🔮")
st.title("🔮 Sirli Falçı")
st.write("Süni zəka ilə gələcəyin qapılarını açın...")

name = st.text_input("Adınız:", placeholder="Məsələn: Əli")
birth_date = st.date_input("Doğum tarixiniz:", min_value=datetime(1950, 1, 1))
code = st.text_input("Ödəniş Kodunuz:", placeholder="Ödəniş kodunu daxil edin")

if st.button("Ulduzları Soruş ☕"):
    if name and code:
        with st.spinner('Ulduzlar sənin üçün hizalanır...'):
            try:
                # Groq üzərindən Llama 3 modelini çağırırıq
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "Sən Azərbaycanca danışan, sirli və müdrik bir falçısan. İnsanlara doğum tarixlərinə görə maraqlı, uzun və pozitiv fallar yazırsan. Azərbaycan dilində çox səlis və şirin danış."},
                        {"role": "user", "content": f"Mənim adım {name}, doğum tarixim {birth_date}. Mənim üçün Azərbaycan dilində sirli, geniş və maraqlı bir fal yaz. Bürclərimi və gələcək şanslarımı qeyd et."}
                    ],
                    temperature=0.8
                )
                
                result = completion.choices[0].message.content
                
                st.markdown("---")
                st.markdown(f"### ✨ Hörmətli {name}, sənin falın:")
                st.write(result)
                st.balloons()
                
                # Telegram bildirişi
                send_telegram_msg(f"🔮 Yeni Fal!\n👤 Ad: {name}\n📅 Doğum: {birth_date}\n🎫 Kod: {code}")
                
            except Exception as e:
                st.error(f"Sistemdə kiçik bir problem oldu: {str(e)}")
    else:
        st.info("Zəhmət olmasa bütün xanaları doldurun.")
