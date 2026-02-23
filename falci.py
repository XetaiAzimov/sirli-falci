import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Sirli Falçı", page_icon="🔮")

# API Key yoxlanışı
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key Secrets-də tapılmadı!")

st.title("🔮 Sirli Falçı")

name = st.text_input("Adınız:")
payment_code = st.text_input("Ödəniş Kodunuz:")

if st.button("Falıma Bax ☕"):
    if name and payment_code:
        with st.spinner('Ulduzlarla əlaqə qurulur...'):
            try:
                # Ən stabil model adı budur
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"{name} üçün Azərbaycan dilində maraqlı fal yaz.")
                
                if response.text:
                    st.success(f"Hörmətli {name}, budur sənin falın:")
                    st.write(response.text)
                    st.balloons()
            except Exception as e:
                st.error(f"Xəta: {str(e)}")
    else:
        st.info("Zəhmət olmasa xanaları doldurun.")
