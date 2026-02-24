import streamlit as st
from groq import Groq
from datetime import datetime
import time  # Gözləmə simulyasiyası üçün lazımdır

# ================== SƏHİFƏ AYARI ==================
st.set_page_config(page_title="Sirli Falçı 🔮", page_icon="🔮", layout="centered")

# ================== SECRETS ==================
try:
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
except:
    st.error("XƏTA: GROQ_API_KEY tapılmadı! Zəhmət olmasa Streamlit Secrets hissəsinə əlavə edin.")
    st.stop()

client = Groq(api_key=GROQ_KEY)

# ================== AYARLAR & FUNKSİYALAR ==================
GIZLI_SOZLER = {
    1: "Ugur", 2: "Tac", 3: "Bahar", 4: "Ulduz", 5: "Gunesh",
    6: "Deniz", 7: "Xezri", 8: "Zirve", 9: "Yarpag", 10: "Cinar",
    11: "Zaman", 12: "Sehr"
}
KART_NOMRE = "4098 0944 2188 8023"

def burc_tap(gun, ay):
    if (ay == 3 and gun >= 21) or (ay == 4 and gun <= 19): return "Qoç"
    if (ay == 4 and gun >= 20) or (ay == 5 and gun <= 20): return "Buğa"
    if (ay == 5 and gun >= 21) or (ay == 6 and gun <= 20): return "Əkizlər"
    if (ay == 6 and gun >= 21) or (ay == 7 and gun <= 22): return "Xərçəng"
    if (ay == 7 and gun >= 23) or (ay == 8 and gun <= 22): return "Şir"
    if (ay == 8 and gun >= 23) or (ay == 9 and gun <= 22): return "Qız"
    if (ay == 9 and gun >= 23) or (ay == 10 and gun <= 22): return "Tərəzi"
    if (ay == 10 and gun >= 23) or (ay == 11 and gun <= 21): return "Əqrəb"
    if (ay == 11 and gun >= 22) or (ay == 12 and gun <= 21): return "Oxatan"
    if (ay == 12 and gun >= 22) or (ay == 1 and gun <= 19): return "Oğlaq"
    if (ay == 1 and gun >= 20) or (ay == 2 and gun <= 18): return "Dolça"
    return "Balıqlar"

# ================== DİZAYN (CSS) ==================
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .payment-box {
        background: linear-gradient(135deg, #1e1e3f 0%, #0b0b1a 100%);
        padding: 25px;
        border-radius: 15px;
        border: 2px solid #4b0082;
        text-align: center;
        box-shadow: 0px 4px 15px rgba(75, 0, 130, 0.5);
        margin-bottom: 20px;
    }
    h1 { color: #9d50bb; text-align: center; font-family: 'Georgia', serif; }
    .stButton>button { background-color: #4b0082; color: white; border-radius: 8px; width: 100%; }
</style>
""", unsafe_allow_html=True)

st.title("🔮 Sirli Falçı")

# ================== ÖDƏNİŞ BÖLMƏSİ ==================
st.markdown(f"""
<div class="payment-box">
    <h3 style="color:white; margin-bottom:5px;">💳 Fal Ödənişi: 1 AZN</h3>
    <p style="color:#bbb; font-size:14px;">Ödənişi aşağıdakı karta (UniBank/Leo) edin və məlumatları doldurun:</p>
    <code style="font-size:24px; color:#00ffcc;">{KART_NOMRE}</code>
</div>
""", unsafe_allow_html=True)

# ================== MÜŞTƏRİ MƏLUMATLARI ==================
st.write("### ✨ Falına baxılacaq şəxsin məlumatları")
name = st.text_input("Ad (Kodu almaq üçün mütləqdir):", placeholder="Məsələn: Xətai")
soyad = st.text_input("Soyad (Könüllü):", placeholder="Məsələn: Məmmədov")

st.markdown("#### 📅 Doğum Tarixi")
cari_il = datetime.now().year
col1, col2, col3 = st.columns(3)
with col1:
    gun = st.selectbox("Gün", list(range(1, 32)))
with col2:
    ay = st.selectbox("Ay", list(range(1, 13)))
with col3:
    il = st.selectbox("İl", list(range(1940, cari_il - 2)))

user_burc = burc_tap(gun, ay)

# ================== TƏHLÜKƏSİZ KOD GENERATORU ==================
if name:
    st.markdown("---")
    st.write("### 🔑 Giriş Kodunu Aktivləşdir")
    
    # 1. Psixoloji Baryer: Qəbz rəqəmi tələbi
    cek_no = st.text_input("🧾 Ödəniş qəbzinin son 4 rəqəmini daxil edin:", placeholder="Məsələn: 4582")
    
    # 2. Xəbərdarlıq mətni
    st.warning("⚠️ Diqqət: Sistem bank terminalları ilə sinxronizasiya olunub. Ödəniş etmədən saxta məlumat daxil edənlərin girişi avtomatik bloklanır.")
    
    if st.checkbox("✅ 1 AZN ödəniş etdiyimi təsdiqləyirəm"):
        if len(cek_no) < 2:
            st.error("❗ Zəhmət olmasa qəbzin son 4 rəqəmini daxil edin!")
        else:
            # 3. Gözləmə Simulyasiyası (10 saniyə)
            with st.status("🔍 Ödəniş bank sistemi ilə yoxlanılır...", expanded=True) as status:
                time.sleep(4)
                st.write("📡 Bank serverinə qoşulur...")
                time.sleep(3)
                st.write("💹 Əməliyyat ID-si yoxlanılır...")
                time.sleep(3)
                status.update(label="✅ Ödəniş təsdiqləndi!", state="complete", expanded=False)
            
            indi = datetime.now()
            bu_saat = indi.hour
            gizli_s = GIZLI_SOZLER.get(indi.month, "Zirve")
            hazir_kod = f"{name.strip().lower()}{indi.day}{bu_saat}{gizli_s.lower()}"
            
            st.success(f"Təşəkkürlər! Giriş kodunuz: **{hazir_kod}**")
            st.info(f"💡 Bu kod saat {bu_saat}:59-a qədər aktivdir. Kodu kopyalayıb aşağıdakı xanaya yazın.")
            st.toast("Ödəniş qeydə alındı!", icon='💰')
else:
    st.info("ℹ️ Kodu görmək üçün əvvəlcə yuxarıda 'Ad' bölməsini doldurun.")

# ================== FAL BÖLMƏSİ ==================
st.write("---")
u_code = st.text_input("Aldığınız kodu bura daxil edin:", type="password")

if st.button("✨ Taleyi Oxu"):
    if name and u_code:
        indi = datetime.now()
        bugun = indi.day
        bu_saat = indi.hour
        kecen_saat = bu_saat - 1 if bu_saat > 0 else 23
        gizli_s = GIZLI_SOZLER.get(indi.month, "Zirve")
        
        correct_codes = [
            f"{name.strip().lower()}{bugun}{bu_saat}{gizli_s.lower()}",
            f"{name.strip().lower()}{bugun}{kecen_saat}{gizli_s.lower()}"
        ]

        if u_code.strip().lower() in correct_codes:
            with st.spinner("🔮 Ulduzlar hizalanır, taleyin vərəqlənir..."):
                try:
                    yas = cari_il - il
                    prompt = (f"Sən müdrik bir azərbaycanlı falçısan. Namizəd: {name} {soyad}. "
                             f"Yaşı: {yas}, Bürcü: {user_burc}. ")
                    
                    if yas < 12:
                        prompt += "Bu uşaqdır. Onun gələcək istedadları və xarakteri haqqında valideynlərinə maraqlı fal yaz."
                    else:
                        prompt += f"Bu şəxs üçün sirli, poetik və {user_burc} bürcünə uyğun fal yaz."
                    
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    st.markdown(f"### 🔮 {user_burc} bürcü altında doğulan {name}, bax gör ulduzlar nə deyir...")
                    st.write(completion.choices[0].message.content)
                    st.balloons()
                except:
                    st.error("Ulduzlarla əlaqə kəsildi. Bir az sonra yenidən cəhd edin.")
        else:
            st.error("❌ Kod yanlışdır və ya vaxtı bitib. Zəhmət olmasa ödəniş edib yeni kod alın.")
    else:
        st.warning("⚠️ Ad və kodu daxil etmək mütləqdir!")
