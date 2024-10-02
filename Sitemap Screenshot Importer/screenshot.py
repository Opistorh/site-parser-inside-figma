from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import sys
import time


def take_screenshot(url, output_path="screenshot.png"):
    # Настройки для headless режима
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Запуск без GUI
    chrome_options.add_argument("--disable-gpu")  # Отключение GPU (для Windows)
    chrome_options.add_argument("--window-size=1920,1080")  # Размер окна

    # Укажите путь к chromedriver, если он не добавлен в PATH
    # Например: 'C:/path/to/chromedriver.exe'
    chromedriver_path = 'chromedriver.exe'  # Предполагается, что chromedriver.exe в той же папке, что и скрипт

    if not os.path.exists(chromedriver_path):
        print(f"Ошибка: Не найден файл chromedriver по пути: {chromedriver_path}")
        sys.exit(1)

    service = Service(chromedriver_path)

    try:
        print("Запуск браузера...")
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        print(f"Ошибка при запуске браузера: {e}")
        sys.exit(1)

    try:
        print(f"Переход на страницу: {url}")
        driver.get(url)

        # Ждём, пока страница полностью загрузится
        time.sleep(5)  # Можно заменить более надёжным методом ожидания

        # Альтернативный способ ожидания загрузки страницы:
        # from selenium.webdriver.common.by import By
        # from selenium.webdriver.support.ui import WebDriverWait
        # from selenium.webdriver.support import expected_conditions as EC
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Сохранение скриншота
        absolute_output_path = os.path.abspath(output_path)
        print(f"Сохранение скриншота как: {absolute_output_path}")
        success = driver.save_screenshot(absolute_output_path)
        if success:
            print(f"Скриншот успешно сохранён: {absolute_output_path}")
        else:
            print("Не удалось сохранить скриншот.")
    except Exception as e:
        print(f"Ошибка при создании скриншота: {e}")
    finally:
        print("Закрытие браузера.")
        driver.quit()


def main():
    try:
        url = input("Введите URL веб-страницы: ").strip()
        if not url:
            print("Ошибка: URL не может быть пустым.")
            return

        if not url.startswith(("http://", "https://")):
            url = "http://" + url

        output = input("Введите имя файла для скриншота (по умолчанию screenshot.png): ").strip()
        if not output:
            output = "screenshot.png"

        # Проверка, имеет ли файл допустимое расширение
        valid_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif']
        _, ext = os.path.splitext(output)
        if not ext.lower() in valid_extensions:
            print(
                f"Предупреждение: Неизвестное расширение файла '{ext}'. Рекомендуется использовать одно из {valid_extensions}.")

        take_screenshot(url, output)
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем.")


if __name__ == "__main__":
    main()
