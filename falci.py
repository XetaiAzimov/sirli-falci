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
GIZLI_SOZ = "Tac"  # İstədiyin vaxt dəyiş
WHATSAPP_NOMRE = "994708685101"
KART_NOMRE = "4098 0944 2188 8023"

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

# ================== ÖDƏNİŞ ==================
st.markdown(f"""
<div class="payment-card">
<h3 style="color:white;">💰 Fal Ödənişi: 1 AZN</h3>

<p style="color:#e0e0e0; font-size:18px;">
<b>💳 Kart nömrəsi:</b><br>
{KART_NOMRE}
</p>

<br>

<a href="https://wa.me/{WHATSAPP_NOMRE}?text=Salam%20Mən%20fal%20üçün%20ödəniş%20etdim.%20Qəbzi%20göndərirəm."
   target="_blank" style="text-decoration:none;">
<div style="background-color:#25D366; color:white; padding:12px; border-radius:10px; font-weight:bold;">
🟢 Qəbzi WhatsApp-a Göndər
</div>
</a>

</div>
""", unsafe_allow_html=True)

# ================== GİRİŞ ==================
name = st.text_input("Adınız:")
u_code = st.text_input("Kodunuz (Ad + Ayın Günü + Gizli Söz):", type="password")

# ================== FAL ==================
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
                            "content": f"Mənim adım {name}. Bu günün enerjisinə görə mənə geniş və sirli fal yaz."
                        }
                    ]
                )

                st.success(f"✨ {name}, taleyin açıldı!")
                st.write(completion.choices[0].message.content)
                st.balloons()

            except:
                st.error("Xəta baş verdi.")
    else:
        st.error("❌ Kod yanlışdır!")
