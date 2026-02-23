import streamlit as st
from groq import Groq
from datetime import datetime

# ================== SƏHİFƏ AYARI ==================
st.set_page_config(page_title="Sirli Falçı", page_icon="🔮")

# ================== SECRETS ==================
try:
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
except:
    st.error("Secrets tapılmadı! GROQ_API_KEY əlavə edilməyib.")
    st.stop()

client = Groq(api_key=GROQ_KEY)

# ================== AYARLAR ==================
GIZLI_SOZ = "Tac"  # Bunu istədiyin vaxt dəyiş
WHATSAPP_NOMRE = "994708685101"
KART_NOMRE = "4098 0944 2188 8023"
M10_LINK = "https://m10.onelink.me/g54T/r3zhexqx"
QR_KOD_URL = "https://i.postimg.cc/mDByMv0P/qr-kod.png"

# ================== DİZAYN ==================
st.markdown("""
<style>
.payment-card {
    background-color: #1a1a2e;
    padding: 20px;
    border-radius: 15px;
    border: 2px solid #4b0082;
    text-align: center;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

st.title("🔮 Sirli Falçı")

# ================== ÖDƏNİŞ BÖLMƏSİ ==================
st.markdown(f"""
<div class="payment-card">
<h3 style="color:white;">💰 Fal Ödənişi: 1 AZN</h3>

<p style="color:#e0e0e0;">
<b>💳 Kart:</b> {KART_NOMRE}
</p>

<div style="margin: 15px 0;">
    <a href="{M10_LINK}" target="_blank">
        <img src="{QR_KOD_URL}" width="180" style="border: 4px solid white; border-radius:10px;">
    </a>
</div>

<a href="{M10_LINK}" target="_blank" 
   style="text-decoration:none; color:#25D366; font-weight:bold;">
📲 M10 ilə Sürətli Ödə
</a>

<br><br>

<a href="https://wa.me/{WHATSAPP_NOMRE}?text=Salam%20Mən%20fal%20üçün%20ödəniş%20etdim.%20Zəhmət%20olmasa%20gizli%20sözü%20göndərin."
   target="_blank" style="text-decoration:none;">
<div style="background-color:#25D366; color:white; padding:12px; border-radius:10px; font-weight:bold;">
🟢 Qəbzi WhatsApp-a Göndər
</div>
</a>

</div>
""", unsafe_allow_html=True)

# ================== GİRİŞ BÖLMƏSİ ==================
name = st.text_input("Adınız:")
u_code = st.text_input("Kodunuz (Ad + Gün + Gizli Söz):", type="password")

# ================== FAL BÖLMƏSİ ==================
if st.button("✨ Falıma Bax"):
    gun = datetime.now().day
    expected_code = f"{name}{gun}{GIZLI_SOZ}"

    if u_code == expected_code:
        with st.spinner("🔮 Falın yazılır..."):
            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "user",
                            "content": f"Adım {name}. Mənə geniş və sirli bir fal yaz."
                        }
                    ]
                )

                st.success(f"✨ {name}, taleyin açıldı!")
                st.write(completion.choices[0].message.content)
                st.balloons()

            except Exception as e:
                st.error("Xəta baş verdi.")
    else:
        st.error("❌ Kod yanlışdır!")
