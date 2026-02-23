import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Sirli Falçı", page_icon="🔮")

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key tapılmadı.")

st.title("🔮 Sirli Falçı")

name = st.text_input("Adınız:")
payment_code = st.text_input("Ödəniş Kodunuz:")

if st.button("Falıma Bax ☕"):
    if name and payment_code:
        with st.spinner('Ulduzlarla əlaqə qurulur...'):
            try:
                # YENİ MODEL ADI BURADADIR
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"{name} adlı şəxs üçün Azərbaycan dilində maraqlı və pozitiv bir fal yaz."
                response = model.generate_content(prompt)
                
                st.success(f"Hörmətli {name}, budur sənin falın:")
                st.write(response.text)
                st.balloons()
            except Exception as e:
                st.error(f"Xəta baş verdi: {str(e)}")
