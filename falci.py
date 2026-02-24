import streamlit as st
from groq import Groq
from datetime import datetime
import time

# ================== SƏHİFƏ AYARI ==================
st.set_page_config(page_title="Sirli Falçı", page_icon="🔮", layout="centered")

# ================== YADDAŞI (SESSION STATE) BAŞLATMA ==================
if 'payment_verified' not in st.session_state:
    st.session_state.payment_verified = False
if 'generated_code' not in st.session_state:
    st.session_state.generated_code = ""

# ================== SECRETS ==================
try:
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
except:
    st.error("API açarı tapılmadı.")
    st.stop()

client = Groq(api_key=GROQ_KEY)

# ================== AYARLAR ==================
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
    #MainMenu, footer, header {visibility: hidden;}
    .main { background-color: #0e1117; }
    .payment-box {
        background: linear-gradient(135deg, #15152e 0%, #050510 100%);
        padding: 25px;
        border-radius: 15px;
        border: 2px solid #4b0082;
        text-align: center;
        margin-bottom: 20px;
    }
    code {
        background-color: #1a1a2e !important;
        color: #00ffcc !important;
        padding: 10px !important;
        border-radius: 5px;
        font-size: 20px !important;
    }
    h1 { color: #9d50bb; text-align: center; font-family: 'Georgia', serif; }
</style>
""", unsafe_allow_html=True)

st.title("🔮 Sirli Falçı")

# ================== ÖDƏNİŞ BÖLMƏSİ ==================
st.markdown(f"""
<div class="payment-box">
    <h3 style="color:white; margin-bottom:5px;">💳 Fal Ödənişi: 1 AZN</h3>
    <p style="color:#bbb;">Ödənişi aşağıdakı karta edin:</p>
    <code>{KART_NOMRE}</code>
</div>
""", unsafe_allow_html=True)

# ================== MÜŞTƏRİ MƏLUMATLARI ==================
name = st.text_input("Adınız:", placeholder="Kodu almaq üçün vacibdir")
soyad = st.text_input("Soyadınız:", placeholder="Könüllüdür")

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
    # Əgər ödəniş hələ təsdiqlənməyibsə, yoxlama panelini göstər
    if not st.session_state.payment_verified:
        cek_no = st.text_input("🧾 Qəbz nömrəsi və ya əməliyyat vaxtı:", placeholder="Məs: 14:35")
        st.warning("⚠️ Diqqət: Ödəniş etmədən saxta məlumat daxil edənlər bloklanır.")
        
        if st.button("✅ Ödənişi Təsdiqlə və Kodumu Al"):
            if len(cek_no) < 2:
                st.error("❗ Zəhmət olmasa qəbz məlumatını daxil edin!")
            else:
                with st.status("🔍 Ödəniş yoxlanılır...", expanded=True) as status:
                    time.sleep(3); st.write("📡 Serverlərlə əlaqə qurulur...")
                    time.sleep(4); st.write("💹 Əməliyyat ID-si təsdiqlənir...")
                    time.sleep(2)
                    status.update(label="✅ Ödəniş təsdiqləndi!", state="complete", expanded=False)
                
                indi = datetime.now()
                gizli_s = GIZLI_SOZLER.get(indi.month, "Zirve")
                st.session_state.generated_code = f"{name.strip().lower()}{indi.day}{indi.hour}{gizli_s.lower()}"
                st.session_state.payment_verified = True
                st.rerun() # Səhifəni yeniləyirik ki, kod görünsün
    
    # Ödəniş təsdiqlənibsə, kodu sabit göstər
    else:
        st.success(f"🎊 Təsdiqləndi! Sizin giriş kodunuz: **{st.session_state.generated_code}**")
        st.warning("⏳ Bu kod 15 dəqiqə ərzində aktivdir. Kodu kopyalayıb aşağıya yazın.")
else:
    st.info("ℹ️ Kodu görmək üçün yuxarıda adınızı daxil edin.")

# ================== FAL BÖLMƏSİ ==================
st.write("---")
u_code = st.text_input("Kodunuzu daxil edin:", type="password")

# Maraqlı cümlə (Advice hissəsi)
if not u_code:
    st.markdown("*“Ulduzlar sənin haqqında pıçıldayır, sadəcə kodu yaz və onları dinlə...”*")
else:
    st.markdown("*“Kod daxil edildi. Qədim ruhlar sənin taleyini vərəqləməyə hazırlaşır...”*")
if st.button("✨ Falıma Bax"):
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
            with st.spinner("🔮 Taleyin vərəqlənir..."):
                try:
                    # ================== YENİ GİZEMLİ PROMPT BURADAN BAŞLAYIR ==================
                    yas = cari_il - il
                    if yas < 12:
                        rol_telimati = (f"Sən qədim ruhların dilini bilən, müdrik və şəfqətli bir azərbaycanlı falçısan. "
                                        f"Namizəd: {name}. Yaşı: {yas} (bu bir uşaqdır), Bürcü: {user_burc}. "
                                        f"Valideynlərinə bu uşaq haqqında sirli, parlaq və maraqlı bir fal yaz.")
                    else:
                        rol_telimati = (f"Sən əsrlərin tozunu udmuş, ulduzların dilini oxuyan qədim və sirli bir azərbaycanlı falçısan. "
                                        f"Müştərin: {name}, Bürcü: {user_burc}, Yaşı: {yas}. "
                                        f"Onun üçün uzun (minimum 3-4 abzas), dərin mənalı, gizemli və poetik bir fal yaz. "
                                        f"Azərbaycan dilinin zənginliyindən istifadə et. Əvvəlcə bürcün xüsusiyyətlərindən başla, "
                                        f"sonra sevgi, iş və gözlənilməz xəbərlər haqqında proqnozlar ver. "
                                        f"Sonda isə ona sirli bir məsləhət və ya xəbərdarlıq qoy.")

                    # API-ya göndərilən hissə
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": rol_telimati}]
                    )
                    # ================== YENİ PROMPT BURADA BİTİR ==================
                    
                    st.markdown(f"### 🔮 {user_burc} bürcü, {name}...")
                    st.write(completion.choices[0].message.content)
                    st.balloons()
                except Exception as e:
                    st.error(f"Ulduzlarla əlaqə kəsildi: {e}")
        else:
            st.error("❌ Kod yanlışdır və ya vaxtı bitib.")
    else:
        st.warning("⚠️ Ad və kodu daxil etmək mütləqdir!")
