from pygame import *   
import sounddevice as sd 
import numpy as np

# === Налаштування ===
fs = 44100     # Частота дискретизації (кількість вимірів за секунду)
chunk = 1024   # Кількість семплів (відліків) за один кадр
width, height = 800, 400  

init()
screen = display.set_mode((width, height))
display.set_caption("Live Audio (Mic)")
clock = time.Clock()
font = font.SysFont("Arial", 24)

# Початкові дані — масив нулів (ще немає звуку)
data = [0.0] * chunk

# === Функція, яку викликає sounddevice, коли приходить нова порція звуку ===
def audio_callback(indata, frames, time_info, status):
    global audio_data, recording_data
    if status:
        print(status)  # Якщо є помилки або попередження, виводимо їх
    # Перетворюємо отриманий звук у список і масштабуємо під висоту екрану
    data = [sample * (height // 2) for sample in indata[:, 0].tolist()]

# === Запуск потоку з мікрофона ===
stream = sd.InputStream(
    callback=audio_callback,  # Функція для отримання аудіо
    channels=1,               # Один канал (моно)
    samplerate=fs,             # Частота дискретизації
    blocksize=chunk,           # Розмір буфера (chunk)
    dtype='float32'            # Тип даних (числа з плаваючою комою)
)
stream.start()

button_rect = Rect(200, 550, 300, 30)

running = True
while running:
    mouse_pos = mouse.get_pos()
    for event in event.get():
        if event.type == QUIT:
            running = False
        if event.type == MOUSEBUTTONDOWN:
            if button_rect.collidepoint(mouse_pos) and is_recording:
                is_recording = False
                stream.stop()
                if recording_data:
                    full_recording = concatenate(recording_data, axis = 0)

    screen.fill((0, 0, 0))
    btn_color = (200, 50, 50)
    draw.rect(screen, btn_color, button_rect, border_radius = 5)

    label_text = "ЗУПИНИТИ ТА ЗБЕРЕГТИ" if is_recording else "ЗБЕРЕЖЕНО"
    text_surf = font.render(label_text, True, (255, 255, 255))
    screen.blit(text_surf, (button_rect.x + 10, button_rect.y +2))

    # Готуємо список точок для малювання хвилі
    points = []
    for i, sample in enumerate(data):
        x = int(i * width / chunk)          # Позиція X для точки
        y = int(height / 2 + sample)        # Позиція Y для точки
        points.append((x, y))               # Додаємо точку в список

    # Малюємо лінію по точках, якщо їх більше однієї
    if len(points) > 1:
        draw.lines(screen, (0, 255, 0), False, points, 2)

    display.update()
    clock.tick(60)

quit()


    
