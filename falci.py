import streamlit as st
from groq import Groq
import requests
from datetime import datetime
import hashlib

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

st.markdown("### Qiymət: **1 AZN**")
st.info("💳 Ödəniş: **M10 (+994 XX XXX XX XX)**. Qəbzi WhatsApp-a atın, kodunuzu alın.")

name = st.text_input("Adınız:")
birth_date = st.date_input("Doğum tarixiniz:", min_value=datetime(1950, 1, 1))
u_code = st.text_input("Ödəniş Kodunuz:", type="password")

if st.button("✨ Taleyimi Göstər"):
    # BU GÜNÜN ŞİFRƏSİ (Məsələn: FAL + bugünkü gün)
    # Hər gün kod avtomatik dəyişir: FAL23, FAL24 və s.
    today_code = f"FAL{datetime.now().day}" 
    
    # Və ya sabit kodlar siyahısı (GitHub-da hərdən dəyişərsən)
    valid_codes = ["BEXT2026", "ULDUZ77", "QISMET11", today_code]

    if not name or not u_code:
        st.warning("Xanaları doldurun!")
    elif u_code not in valid_codes:
        st.error("❌ Kod yanlışdır!")
    else:
        # TARİX YOXLANIŞI
        current_year = datetime.now().year
        if birth_date.year > current_year:
            st.warning("Hələ doğulmamısan ki? 😊")
        else:
            with st.spinner('🔮 Falın hazırlanır...'):
                try:
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": "Sən sirli Azərbaycanlı falçısan. Professional fal yaz."},
                            {"role": "user", "content": f"Adım {name}, tarixim {birth_date}. Fal yaz."}
                        ]
                    )
                    st.success(f"✨ {name}, taleyin:")
                    st.write(completion.choices[0].message.content)
                    st.balloons()
                    
                    # Sənə Telegramda xəbər veririk
                    send_telegram_msg(f"💰 1 AZN! \n👤 Müştəri: {name}\n🎫 Kod: {u_code}")
                except:
                    st.error("Sistemdə xəta!")
