# Программа открытия нескольких браузеров в Chrome
# Проверяет список ссылок и открывает только те, которые ещё не открыты
# Записывает дату и время открытия каждой ссылки
# При запуске проверяет дату: если не сегодняшняя — очищает файл

import webbrowser
import os
import psutil   # pip install psutil
from datetime import datetime

URLS_FILE = "opened_urls.txt"   # файл для хранения уже открытых ссылок
INPUT_FILE = "urls.txt"         # файл со списком ссылок для открытия

# --- Проверка даты в начале программы ---
today = datetime.now().date()
if os.path.exists(URLS_FILE):
    with open(URLS_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    if lines:
        # Берём дату из первой строки (после разделителя "|")
        first_line = lines[0]
        parts = first_line.split(" | ")
        if len(parts) == 2:
            try:
                file_date = datetime.strptime(parts[1], "%Y-%m-%d %H:%M:%S").date()
                if file_date != today:
                    # Если дата не сегодняшняя — очищаем файл
                    print("Дата в файле не совпадает с сегодняшней. Очищаем файл...")
                    open(URLS_FILE, "w").close()
            except ValueError:
                # Если формат даты некорректный — тоже очищаем
                print("Некорректная дата в файле. Очищаем файл...")
                open(URLS_FILE, "w").close()

# Загружаем уже открытые адреса из файла (после очистки при необходимости)
if os.path.exists(URLS_FILE):
    with open(URLS_FILE, "r", encoding="utf-8") as f:
        opened_urls = set(line.strip().split(" | ")[0] for line in f if line.strip())
else:
    opened_urls = set()

def is_chrome_running():
    """Проверяем, запущен ли процесс Chrome"""
    for proc in psutil.process_iter(['name']):
        name = proc.info.get('name') or ''
        if "chrome.exe" in name.lower():
            return True
    return False

def open_url(url):
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    # chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

    # Проверка: если адрес уже открыт
    if url in opened_urls:
        print(f"Адрес {url} уже был открыт ранее, повторно не открываем.")
        return

    # Проверка: запущен ли Chrome
    if not is_chrome_running():
        print("Chrome не запущен. Открываем браузер...")
    else:
        print("Chrome уже работает. Добавляем вкладку...")

    # Регистрируем Chrome как браузер
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
    browser = webbrowser.get('chrome')
    browser.open_new_tab(url)

    # Добавляем адрес в список и сохраняем в файл с датой
    opened_urls.add(url)
    with open(URLS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{url} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

def open_urls_from_file():
    """Открывает список адресов из файла urls.txt"""
    if not os.path.exists(INPUT_FILE):
        print(f"Файл {INPUT_FILE} не найден. Создайте его и добавьте ссылки построчно.")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    # Если список открытых страниц пустой → открыть все
    if not opened_urls:
        print("Нет открытых страниц. Открываем все ссылки из файла.")
        for url in urls:
            open_url(url)
    else:
        print("Есть уже открытые страницы. Проверяем новые ссылки...")
        for url in urls:
            open_url(url)

if __name__ == "__main__":
    open_urls_from_file()
    print("Все адреса обработаны")
    os._exit(0)