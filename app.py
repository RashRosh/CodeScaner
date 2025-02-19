import streamlit as st
import pandas as pd
from PIL import Image
import io
import easyocr

# Настройки страницы
st.set_page_config(page_title="Code Scanner", layout="centered")

# Заголовок приложения
st.title("📸 Code Scanner App")
st.write("Загрузите изображение с кодом, и приложение автоматически его распознает и сохранит в таблицу Excel.")

# Инициализация EasyOCR
reader = easyocr.Reader(['en'])

# Функция распознавания кода
def extract_code(image):
    result = reader.readtext(image)
    if result:
        return result[0][-2]  # Берем самый крупный найденный текст
    return "Код не найден"

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
