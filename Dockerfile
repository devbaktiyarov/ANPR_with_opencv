# Используем официальный Python-образ
FROM python:3.10

# # Устанавливаем Tesseract OCR
# RUN apt update && apt install -y tesseract-ocr tesseract-ocr-eng  && apt-get -y install ffmpeg libsm6 libxext6
RUN apt update && apt install -y  tesseract-ocr  tesseract-ocr-eng libgl1-mesa-glx libglib2.0-0 ffmpeg libsm6 libxext6 


# Указываем переменную среды для Tesseract
ENV TESSDATA_PREFIX="/usr/share/tesseract-ocr/4.00/tessdata/"

# Устанавливаем зависимости из requirements.txt
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . .

# Команда для запуска скрипта
CMD ["python", "main.py"]
