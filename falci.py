import streamlit as st
import google.generativeai as genai

# Səhifə nizamlamaları
st.set_page_config(page_title="Sirli Falçı", page_icon="🔮")

# Gemini API Key-i Secrets-dən götürürük
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key tapılmadı. Zəhmət olmasa Secrets bölməsini yoxlayın.")

st.title("🔮 Sirli Falçıya Xoş Gəldiniz")
st.write("Ulduzlar sizin üçün nə deyir? Öyrənmək üçün məlumatları doldurun.")

# İstifadəçi girişləri
name = st.text_input("Adınız:", placeholder="Məsələn: Əli")
payment_code = st.text_input("Ödəniş Kodunuz:", placeholder="Məsələn: FAL2026")

if st.button("Falıma Bax ☕"):
    if name and payment_code:
        # Burada sadə bir ödəniş kodu yoxlanışı (İstədiyin kodu bura yaza bilərsən)
        if payment_code.strip() != "": 
            with st.spinner('Ulduzlarla əlaqə qurulur...'):
                try:
                    model = genai.GenerativeModel('gemini-pro')
                    prompt = f"{name} adlı şəxs üçün maraqlı, sirli və müsbət bir fal yaz. Azərbaycan dilində olsun."
                    response = model.generate_content(prompt)
                    
                    st.success(f"Hörmətli {name}, budur sənin falın:")
                    st.write(response.text)
                    st.balloons()
                    
                    # Excel yerinə sadəcə ekranda bildiriş
                    st.info("Qeyd: Falınız uğurla yaradıldı. Bizi seçdiyiniz üçün sağ olun!")
                    
                except Exception as e:
                    st.error(f"Xəta baş verdi: {str(e)}")
        else:
            st.warning("Zəhmət olmasa düzgün ödəniş kodu daxil edin.")
    else:
        st.info("Davam etmək üçün adınızı və ödəniş kodunuzu yazın.")
