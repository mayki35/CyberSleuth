import tempfile
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
def consulta_placa_sunarp():
    """
    Consulta información de una placa vehicular en SUNARP (Perú) usando Selenium.
    """
    placa = input(f"\n {C_WH}Ingrese el número de placa (ej. ABC-123): {C_GR}").upper()
    if not placa:
        print(f"{C_RE}\nError: Debe ingresar un número de placa.")
        return

    driver = get_driver()
    if not driver:
        return

    try:
        print(f"\n{C_WH}[*] Iniciando navegador para consulta vehicular en SUNARP...")
        driver.get("https://www.sunarp.gob.pe/ConsultaVehicular/")

        placa_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'txtPlaca')))
        placa_input.send_keys(placa)

        print(f"\n{C_YE}--> ACCIÓN REQUERIDA <_--")
        print(f"{C_WH}Por favor, resuelva el CAPTCHA en la ventana de Chrome y haga clic en 'Realizar Búsqueda'.")
        print(f"{C_WH}El script esperará hasta 2 minutos por los resultados...")

        WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Placa') and contains(@class, 'titulo')]")))

        print(f"\n{C_GR}[+] ¡Resultados encontrados! Extrayendo datos...")
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        data_divs = soup.find_all('div', class_='row')
        data = {}
        for div in data_divs:
            label_tag = div.find('div', class_='col-sm-3')
            value_tag = div.find('div', class_='col-sm-9')
            if label_tag and value_tag:
                key = label_tag.text.strip().replace(':', '')
                value = value_tag.text.strip()
                if key:
                    data[key] = value

        print(f"\n {C_WH}========== {C_GR}INFORMACIÓN VEHICULAR (Fuente: SUNARP){C_WH} ==========")
        if data:
            for key, value in data.items():
                print(f" {C_WH}{key:<20}:{C_GR} {value}")
        else:
            print(f"{C_RE}No se pudieron extraer los datos. La estructura de la página puede haber cambiado.")

    except TimeoutException:
        print(f"{C_RE}\nError: El tiempo de espera se agotó. Posibles causas:")
        print(f"{C_YE}  - No se resolvió el CAPTCHA o la placa no arrojó resultados.")
    except Exception as e:
        print(f"{C_RE}\nOcurrió un error inesperado: {e}")
        if driver:
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html', encoding='utf-8') as f:
                f.write(driver.page_source)
                print(f"{C_YE}[!] Se ha guardado el estado de la página para depuración en: {f.name}")
    finally:
        if driver:
            driver.quit()
            print(f"\n{C_WH}[*] Navegador cerrado.")

@is_option
def consulta_licencia_mtc():
    """
    Consulta información de una licencia de conducir en el MTC (Perú) usando Selenium.
    """
    dni = input(f"\n {C_WH}Ingrese el número de DNI (8 dígitos): {C_GR}")
    if not dni.isdigit() or len(dni) != 8:
        print(f"{C_RE}\nError: El DNI debe contener 8 dígitos numéricos.")
        return

    driver = get_driver()
    if not driver:
        return

    try:
        print(f"\n{C_WH}[*] Iniciando navegador para consulta de licencia en MTC...")
        driver.get("https://licencias.mtc.gob.pe/")

        try:
            terminos_check = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'chkTerminos')))
            driver.execute_script("arguments[0].click();", terminos_check)
            cerrar_btn = driver.find_element(By.XPATH, "//button[text()='Cerrar']")
            driver.execute_script("arguments[0].click();", cerrar_btn)
            print(f"{C_GR}[+] Términos y condiciones aceptados.")
        except TimeoutException:
            print(f"{C_YE}[!] No se encontró el modal de términos (puede que ya no exista o la página cambió).")

        dni_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'txtNroDocumento')))
        dni_input.send_keys(dni)

        print(f"\n{C_YE}--> ACCIÓN REQUERIDA <_--")
        print(f"{C_WH}Por favor, resuelva el CAPTCHA en la ventana de Chrome y haga clic en 'Buscar'.")
        print(f"{C_WH}El script esperará hasta 2 minutos por los resultados...")

        WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.ID, 'divTabla')))

        print(f"\n{C_GR}[+] ¡Resultados encontrados! Extrayendo datos...")
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        data_table = soup.find('table', id='datatable')
        data = {}
        if data_table:
            rows = data_table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if len(cells) == 2:
                    key = cells[0].text.strip().replace(':', '')
                    value = cells[1].text.strip()
                    if key:
                        data[key] = value

        print(f"\n {C_WH}========== {C_GR}INFORMACIÓN DE LICENCIA (Fuente: MTC){C_WH} ==========")
        if data:
            for key, value in data.items():
                print(f" {C_WH}{key:<25}:{C_GR} {value}")
        else:
            print(f"{C_RE}No se pudieron extraer los datos. La estructura de la página puede haber cambiado.")

    except TimeoutException:
        print(f"{C_RE}\nError: El tiempo de espera se agotó. Posibles causas:")
        print(f"{C_YE}  - No se resolvió el CAPTCHA, el DNI no tiene licencia o no arrojó resultados.")
    except Exception as e:
        print(f"{C_RE}\nOcurrió un error inesperado: {e}")
        if driver:
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html', encoding='utf-8') as f:
                f.write(driver.page_source)
                print(f"{C_YE}[!] Se ha guardado el estado de la página para depuración en: {f.name}")
    finally:
        if driver:
            driver.quit()
            print(f"\n{C_WH}[*] Navegador cerrado.")
