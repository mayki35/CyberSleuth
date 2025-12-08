import time
import tempfile
from collections import defaultdict
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from ...config import C_WH, C_GR, C_RE, C_YE
from ...utils import is_option, get_driver

@is_option
def consulta_lineas_osiptel():
    """
    Consulta el número de líneas móviles registradas a nombre de un DNI en el servicio de OSIPTEL (Perú).
    """
    dni = input(f"\n {C_WH}Ingrese el número de DNI (8 dígitos): {C_GR}")
    if not dni.isdigit() or len(dni) != 8:
        print(f"{C_RE}\nError: El DNI debe contener 8 dígitos numéricos.")
        return

    driver = get_driver()
    if not driver:
        return

    try:
        print(f"\n{C_WH}[*] Iniciando navegador para consulta de líneas...")

        url = "https://checatuslineas.osiptel.gob.pe/"
        driver.get(url)

        try:
            dialog = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div.v-dialog--active[role='dialog']"))
            )
            print(f"{C_WH}[*] Modal de política de privacidad detectado. Intentando aceptar...")
            accept_button = dialog.find_element(By.XPATH, ".//button[contains(., 'ACEPTAR')]")
            driver.execute_script("arguments[0].click();", accept_button)
            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.v-dialog--active[role='dialog']"))
            )
            print(f"{C_GR}[+] Política de privacidad aceptada correctamente.")
        except TimeoutException:
            print(f"{C_YE}[!] No se detectó el modal de política de privacidad en 30 segundos (o ya fue aceptado). Continuando...")

        print(f"{C_WH}[*] Seleccionando el tipo de documento (DNI)...")
        doc_type_dropdown = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'document-type'))
        )
        driver.execute_script("arguments[0].click();", doc_type_dropdown)
        time.sleep(0.5)

        dni_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'v-list-item-title') and text()='DNI']"))
        )
        dni_option.click()

        dni_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'document-number'))
        )
        dni_input.send_keys(dni)

        print(f"\n{C_YE}--> ACCIÓN REQUERIDA <_--")
        print(f"{C_WH}Se ha abierto una ventana de Chrome.")
        print(f"{C_WH}Por favor, resuelva el CAPTCHA y haga clic en el botón 'Consultar'.")
        print(f"{C_WH}El script esperará hasta 2 minutos...")
        
        WebDriverWait(driver, 120).until(
            EC.visibility_of_element_located((By.XPATH, "//th[contains(text(), 'Empresa Operadora')]"))
        )

        print(f"\n{C_GR}[+] ¡Resultados encontrados! Extrayendo datos...")
        soup = BeautifulSoup(driver.page_source, 'lxml')

        results_table = soup.find('div', class_='v-data-table__wrapper').find('table')
        company_counts = defaultdict(int)
        if results_table:
            rows = results_table.find('tbody').find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 3:
                    company_name = cells[2].text.strip()
                    if company_name:
                        company_counts[company_name] += 1

        print(f"\n {C_WH}========== {C_GR}LÍNEAS MÓVILES REGISTRADAS (Fuente: OSIPTEL){C_WH} ==========")
        if company_counts:
            total_lines = 0
            for company, count in sorted(company_counts.items()):
                print(f" {C_WH}{company:<30}:{C_GR} {count} línea(s)")
                total_lines += count
            print(f" {C_WH}{'-'*42}")
            print(f" {C_WH}{'TOTAL':<30}:{C_GR} {total_lines} línea(s)")
        else:
            print(f" {C_RE}No se encontraron líneas registradas para el DNI proporcionado.")

        print(f"\n{C_YE}[AVISO IMPORTANTE]{C_WH}")
        print(f"El servicio de OSIPTEL muestra los números de teléfono de forma CENSURADA por razones de privacidad y seguridad.")
        print(f"Este script muestra la cantidad de líneas por operador, que es la información pública disponible.")

    except TimeoutException:
        print(f"{C_RE}\nError: El tiempo de espera se agotó después de 2 minutos.")
    except Exception as e:
        print(f"{C_RE}\nOcurrió un error inesperado durante la consulta con Selenium: {e}")
        if driver:
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html', encoding='utf-8') as f:
                f.write(driver.page_source)
                print(f"{C_YE}[!] Se ha guardado el estado actual de la página para depuración en: {f.name}")

    finally:
        if driver:
            driver.quit()
            print(f"\n{C_WH}[*] Navegador cerrado.")
