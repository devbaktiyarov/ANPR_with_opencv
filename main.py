import cv2
import pytesseract
import requests
import os
from datetime import datetime

# Настройка Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Параметры
frameWidth = 1000
frameHeight = 480
minArea = 500
count = 0

# Создание папки для изображений
if not os.path.exists("./IMAGES"):
    os.makedirs("./IMAGES")

# Загрузка каскада
plateCascade = cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")
if plateCascade.empty():
    print("❌ Не удалось загрузить каскад. Проверь путь к 'haarcascade_russian_plate_number.xml'")
    exit()

# Подключение к камере
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 150)

while True:
    success, img = cap.read()
    if not success:
        print("❌ Не удалось получить кадр с камеры")
        continue

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    numberPlates = plateCascade.detectMultiScale(imgGray, 1.1, 4)

    for (x, y, w, h) in numberPlates:
        area = w * h
        if area > minArea:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(img, "NumberPlate", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

            imgRoi = img[y:y + h, x:x + w]
            cv2.imshow("Number Plate", imgRoi)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('s'):
                if imgRoi.size > 0:
                    filename = os.path.join("IMAGES", f"{count}.jpg")
                    success_save = cv2.imwrite(filename, imgRoi)
                    print(f"📷 Сохраняем изображение: {filename} — Успешно? {success_save}")

                    # Распознавание текста
                    custom_config = r'--oem 3 --psm 7'
                    number = pytesseract.image_to_string(imgRoi, config=custom_config).strip()
                    print("🔤 Распознанный текст:", number)

                    # Пример отправки POST-запроса
                    if number:
                        time = datetime.now()
                        data = {'plateNumber': number}
                        headers = {"Content-Type": "application/json"}
                        try:
                            response = requests.post('http://localhost:8080/v1/api', json=data, headers=headers)
                            print("📤 Отправлено на сервер:", response.status_code)
                        except Exception as e:
                            print("⚠️ Ошибка при отправке на сервер:", e)

                    # Подтверждение на экране
                    cv2.rectangle(img, (0, 200), (640, 300), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, "Scan Saved", (15, 265), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2)
                    cv2.imshow("Result", img)
                    cv2.waitKey(500)
                    count += 1

    cv2.imshow("Result", img)

    # Выход по клавише 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("🛑 Завершение программы")
        break

cap.release()
cv2.destroyAllWindows()
