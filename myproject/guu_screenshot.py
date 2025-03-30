from playwright.sync_api import sync_playwright
import os
from datetime import datetime

def capture_guu_screenshot():
    with sync_playwright() as p:
        try:
            # Запуск браузера
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Настройки страницы
            page.set_default_timeout(15000)
            page.set_viewport_size({"width": 1280, "height": 1024})
            
            # Переход на сайт
            page.goto("https://guu.ru/", wait_until="networkidle")
            
            # Создание папки для скриншотов
            os.makedirs("screenshots", exist_ok=True)
            filename = f"screenshots/guu_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            
            # Создание скриншота (без параметра quality для PNG)
            page.screenshot(
                path=filename,
                full_page=True,
                type="png"  # Явно указываем тип
            )
            
            print(f"✓ Скриншот сохранен: {filename}")
            
        except Exception as e:
            print(f"✗ Ошибка: {str(e)}")
        finally:
            if 'browser' in locals():
                browser.close()

if __name__ == "__main__":
    capture_guu_screenshot()