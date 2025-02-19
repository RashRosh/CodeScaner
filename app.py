import streamlit as st
import pandas as pd
import easyocr
from PIL import Image
import io

# Настройки страницы
st.set_page_config(page_title="Code Scanner", layout="centered")

# Заголовок приложения
st.title("📸 Code Scanner App")
st.write("Загрузите изображение с кодом, выберите область распознавания, и приложение автоматически его распознает и сохранит в таблицу Excel.")

# Функция распознавания кода
def extract_code(image, region):
    reader = easyocr.Reader(['en'])
    cropped_image = image.crop(region)
    result = reader.readtext(cropped_image)
    if result:
        return result[0][-2]  # Берем самый крупный найденный текст
    return "Код не найден"

# Загрузка изображения
uploaded_file = st.file_uploader("Загрузите изображение", type=["png", "jpg", "jpeg"])

# Обработка изображения
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Загруженное изображение", use_column_width=True)
    
    # Выбор области распознавания
    st.write("Выберите координаты области распознавания (левая верхняя и правая нижняя точки):")
    x1 = st.number_input("X1", min_value=0, max_value=image.width, value=0)
    y1 = st.number_input("Y1", min_value=0, max_value=image.height, value=0)
    x2 = st.number_input("X2", min_value=0, max_value=image.width, value=image.width)
    y2 = st.number_input("Y2", min_value=0, max_value=image.height, value=image.height)
    
    region = (x1, y1, x2, y2)
    
    # Распознаем код
    code = extract_code(image, region)
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
