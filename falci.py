import streamlit as st
from groq import Groq
import requests
from datetime import datetime

# Secrets
GROQ_KEY = st.secrets["GROQ_API_KEY"]
TELEGRAM_TOKEN = st.secrets["TELEGRAM_BOT_TOKEN"]
CHAT_ID = st.secrets["TELEGRAM_CHAT_ID"]

client = Groq(api_key=GROQ_KEY)

def send_telegram_msg(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": message})
    except: pass

st.set_page_config(page_title="Sirli Falçı", page_icon="🔮")
st.title("🔮 Sirli Falçı")

# ÖDƏNİŞ QUTUSU
st.markdown(f"""
<div style="background-color:#1a1a2e; padding:15px; border-radius:10px; border:1px solid #4b0082">
    <h4 style="color:#e0e0e0">💰 Falınızı Alın (1 AZN)</h4>
    <p>1. <b>M10 / Kart:</b> 4169 XXXX XXXX XXXX</p>
    <p>2. Qəbzi bota göndər və kodunu al:</p>
    <a href="https://t.me/SeninBotunUsernamesi" target="_blank">
        <button style="background-color:#4b0082; color:white; border:none; padding:8px 15px; border-radius:5px; cursor:pointer">
            📩 Qəbzi Göndər
        </button>
    </a>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

name = st.text_input("Adınız (Ödənişdəki adla eyni olmalıdır):")
u_code = st.text_input("Sizə verilən Ödəniş Kodu:", type="password")

if st.button("✨ Falıma Bax"):
    # RİYAZİ YOXLAMA: Kod müştərinin adı + bugünkü gün olmalıdır
    # Məsələn: Eli + 24 = Eli24
    expected_code = f"{name}{datetime.now().day}"
    
    if not name or not u_code:
        st.warning("Zəhmət olmasa bütün xanaları doldurun.")
    
    elif u_code != expected_code:
        st.error("❌ Kod yanlışdır! Kod sizin adınız və günün tarixindən ibarət olmalıdır.")
    
    else:
        with st.spinner('🔮 Ulduzlar skan edilir...'):
            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "Sən sirli Azərbaycanlı falçısan. Professional fal yaz."},
                        {"role": "user", "content": f"Adım {name}. Mənə geniş bir fal yaz."}
                    ]
                )
                st.success(f"✨ {name}, taleyin hazır!")
                st.write(completion.choices[0].message.content)
                st.balloons()
                
                # Sənə bildiriş gəlir ki, Eli bu kodu İŞLƏTDİ
                send_telegram_msg(f"✅ 1 AZN QAZANILDI!\n👤 Müştəri: {name}\n🎫 Kod: {u_code}")
                
            except:
                st.error("Sistemdə xəta!")
