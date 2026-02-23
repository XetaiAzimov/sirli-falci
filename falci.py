import streamlit as st
from groq import Groq
from datetime import datetime

# Secrets (Bunlar artıq səndə var)
GROQ_KEY = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=GROQ_KEY)

st.title("🔮 Sirli Falçı")

# --- ADMIN HİSSƏSİ (Sənin üçün) ---
# Sən bura hər gün və ya həftə yeni bir sirli söz yaza bilərsən
# Müştəri ödəniş edəndə ona bu sözü deyəcəksən
GIZLI_SOZ = "ALMA" # Bunu hərdən dəyiş (məsələn: NAR, ULDUZ, BEXT)

st.markdown("### Ödəniş: 1 AZN")
st.info(f"💳 M10/Kart: +994 XX XXX XX XX. Qəbzi atın, **GİZLİ SÖZÜ** alın.")

name = st.text_input("Adınız:")
u_code = st.text_input("Sizə verilən tam kod (Ad + Tarix + Gizli Söz):", type="password")

if st.button("✨ Falıma Bax"):
    # Gözlənilən kod formatı: Xetai24ALMA
    expected_code = f"{name}{datetime.now().day}{GIZLI_SOZ}"
    
    if u_code == expected_code:
        with st.spinner('🔮 Ulduzlar skan edilir...'):
            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": f"Adım {name}. Mənə geniş bir fal yaz."}]
                )
                st.success(f"✨ {name}, taleyin hazırdır!")
                st.write(completion.choices[0].message.content)
                st.balloons()
            except:
                st.error("Xəta baş verdi.")
    else:
        st.error("❌ Kod yanlışdır! Gizli sözü düzgün daxil etdiyinizdən əmin olun.")
