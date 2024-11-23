import streamlit as st
import pickle
import pandas as pd

# Saqlangan modelni yuklash
with open('diagnosis_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Datasetni yuklash (davolash, shifokor va xavf darajasi uchun)
data = pd.read_csv('dataset.csv')

# Streamlit interfeysini sozlash
st.set_page_config(page_title="Kasallikni bashorat qiluvchi model", page_icon="🩺", layout="centered")

st.markdown(
    """
    <style>
    /* Umumiy fon uchun rangli gradient */
    .stApp {
        background: linear-gradient(135deg, #ffecd2, #fcb69f);
        color: #34495E;
        font-family: Arial, sans-serif;
    }

    /* Karta uchun quti ko'rinishi */
    .main {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 25px;
        box-shadow: 0px 15px 30px rgba(0, 0, 0, 0.2);
        max-width: 750px;
        margin: 20px auto;
        border: 2px solid #f39c12;
    }

    /* Sarlavha */
    h1 {
        color: #2E4053;
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 25px;
        text-shadow: 2px 2px 5px #f39c12;
    }

    /* Matn maydoni sarlavhasi */
    .stTextArea>label {
        font-size: 1.3rem;
        color: #5D6D7E;
        font-weight: bold;
        margin-bottom: 10px;
    }

    /* Tugmalar */
    .stButton>button {
        background-color: #e74c3c !important;
        color: #ffffff !important;
        border-radius: 50px !important;
        padding: 15px 35px !important;
        font-size: 20px !important;
        font-weight: bold;
        border: none;
        box-shadow: 0px 8px 15px rgba(231, 76, 60, 0.4);
        transition: 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #c0392b !important;
        box-shadow: 0px 12px 20px rgba(192, 57, 43, 0.4);
        transform: scale(1.05);
    }

    /* Tashxis natijalari qutisi */
    .result-section {
        background-color: #f7f1e3;
        padding: 25px;
        border-radius: 20px;
        margin-top: 20px;
        box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.1);
    }

    .result-section h3 {
        font-size: 1.7rem;
        color: #34495E;
        font-weight: bold;
        margin-bottom: 15px;
    }

    .result-section p {
        font-size: 1.2rem;
        color: #2c3e50;
        margin-bottom: 10px;
    }

    /* Ikonalar */
    .icon {
        font-size: 1.8rem;
        margin-right: 10px;
        color: #2980b9;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sarlavha
st.title("Kasallik Tashxislash Dasturi")

# Belgilarni kiritish
st.markdown("<h3 style='color:#34495E;'>🔍 Kasallik belgilarini kiriting:</h3>", unsafe_allow_html=True)
symptoms = st.text_area(
    "Kasallik belgilarini kiriting (vergul bilan ajrating):",
    placeholder="Masalan: bosh og'rig'i, yo'tal, isitma"
)

# Bashorat qilish
if st.button("Tashxislash"):
    if symptoms:
        # Kirishni modelga mos formatda tayyorlash
        input_data = [symptoms]
        disease_prediction = model.predict(input_data)[0]  # Model yordamida kasallik bashorati

        # Tashxis natijasini ko'rsatish
        st.markdown(f"<div class='result-section'><h3>📋 Tashxis: {disease_prediction}</h3>", unsafe_allow_html=True)

        # Davolash usullari, shifokor va xavf darajasini olish
        diagnosis_info = data[data['disease'] == disease_prediction].iloc[0]
        treatment = diagnosis_info['cures']
        doctor = diagnosis_info['doctor']
        risk_level = diagnosis_info['risk level']

        # Ma'lumotlarni ko'rsatish
        st.markdown(f"<p><span class='icon'>💊</span><b>Davolash uchun dorilar</b>: {treatment}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><span class='icon'>🩺</span><b>Shifokor</b>: {doctor}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><span class='icon'>⚠️</span><b>Xavf darajasi</b>: {risk_level}</p></div>", unsafe_allow_html=True)
    else:
        st.error("Iltimos, kamida bitta simptom kiriting.")
