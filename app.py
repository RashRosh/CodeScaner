import streamlit as st
import pandas as pd
import pytesseract
from PIL import Image
import io

# Настройки страницы
st.set_page_config(page_title="Code Scanner", layout="centered")

# Заголовок приложения
st.title("📸 Code Scanner App")
st.write("Загрузите изображение с кодом, и приложение автоматически его распознает и сохранит в таблицу Excel.")

# Функция распознавания кода
def extract_code(image):
    text = pytesseract.image_to_string(image, config='--psm 6')
    return text.strip()

# Загрузка изображения
uploaded_file = st.file_uploader("Загрузите изображение", type=["png", "jpg", "jpeg"])

# Обработка изображения
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Загруженное изображение", use_column_width=True)
    
    # Распознаем код
    code = extract_code(image)
    st.success(f"Распознанный код: {code}")
    
    # Сохранение в Excel
    df = pd.DataFrame([code], columns=["Распознанный код"])
    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, index=False)
    excel_buffer.seek(0)
    
    st.download_button(
        label="📥 Скачать Excel-файл",
        data=excel_buffer,
        file_name="codes.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
