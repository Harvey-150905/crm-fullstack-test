from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests
import csv
import time


def main():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    try:
        print("Iniciando")

        driver.get("http://localhost:8765/panel/")

        # LOGIN
        print("Intentando login...")

        wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys("demo")
        driver.find_element(By.NAME, "password").send_keys("demo")
        driver.find_element(By.TAG_NAME, "button").click()

        wait.until(EC.url_contains("/panel"))
        print("OK")

        # COOKIES → requests
        session = requests.Session()
        for c in driver.get_cookies():
            session.cookies.set(c['name'], c['value'])

        all_orders = []

        # SIMULACIÓN DE ENDPOINT (no disponible en entorno)
        for page in range(1, 13):
            print(f"📄 Página {page}")

            for intento in range(3):
                try:
                    # endpoint hipotético descubierto vía DevTools
                    url = f"http://localhost:8765/api/orders?page={page}"

                    res = session.get(url)
                    res.raise_for_status()

                    data = res.json()
                    orders = data.get("results", [])

                    print(f"   → {len(orders)} filas")

                    all_orders.extend(orders)
                    break

                except Exception as e:
                    print(f"⚠️ Error en página {page}, intento {intento+1}")
                    time.sleep(2 ** intento)

        # EXPORT CSV
        if all_orders:
            with open("orders.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=all_orders[0].keys())
                writer.writeheader()
                writer.writerows(all_orders)

            print("csv listo")

        else:
            print("No se obtuvieron datos (endpoint no disponible)")

    finally:
        driver.quit()
        print("Driver cerrado")


if __name__ == "__main__":
    main()