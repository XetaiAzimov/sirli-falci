import streamlit as st
from groq import Groq
from datetime import datetime

# ================== SECRETS ==================
GROQ_KEY = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=GROQ_KEY)

# ================== AYARLAR ==================
GIZLI_SOZ = "Tac"   # Bunu istədiyin vaxt dəyiş
WHATSAPP_NOMRE = "994708685101"

# ================== UI ==================
st.title("🔮 Sirli Falçı")

st.markdown("### 💰 Ödəniş: 1 AZN")

# ================== WHATSAPP DÜYMƏ ==================
whatsapp_link = f"https://wa.me/{WHATSAPP_NOMRE}?text=Salam%20❓%20Mən%20fal%20üçün%20ödəniş%20etdim.%20Zəhmət%20olmasa%20gizli%20sözü%20göndərin."

st.markdown(f"""
<a href="{whatsapp_link}" target="_blank">
<button style="
background-color:#25D366;
color:white;
border:none;
padding:12px 20px;
border-radius:12px;
cursor:pointer;
font-weight:bold;
width:100%;
font-size:16px;">
🟢 WhatsApp ilə Qəbzi Göndər və Kodu Al
</button>
</a>
""", unsafe_allow_html=True)

st.info("💳 M10/Kart: +994 70 868 51 01\n\nQəbzi göndər, gizli sözü al, sonra kodu daxil et.")

# ================== İSTİFADƏÇİ MƏLUMATLARI ==================
name = st.text_input("Adınız:")
u_code = st.text_input("Sizə verilən tam kod (Ad + Gün + Gizli Söz):", type="password")

# ================== FAL DÜYMƏSİ ==================
if st.button("✨ Falıma Bax"):
    
    expected_code = f"{name}{datetime.now().day}{GIZLI_SOZ}"

    if u_code == expected_code:
        with st.spinner("🔮 Ulduzlar oxunur..."):
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
        st.error("❌ Kod yanlışdır! Gizli sözü düzgün daxil etdiyinizdən əmin olun.")
