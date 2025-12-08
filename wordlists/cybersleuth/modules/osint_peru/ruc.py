import requests
import json
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
def consulta_RUC():
    """
    Consulta la información de un RUC (Registro Único de Contribuyentes) en Perú.
    """
    ruc = input(f"\n {C_WH}Ingrese el número de RUC (11 dígitos): {C_GR}")
    if not ruc.isdigit() or len(ruc) != 11:
        print(f"{C_RE}\nError: El RUC debe contener 11 dígitos numéricos.")
        return

    print(f"\n{C_WH}[*] Consultando RUC {C_GR}{ruc}{C_WH} en la fuente oficial de SUNAT...")

    try:
        api_url = f"https://api.apis.net.pe/v1/ruc?numero={ruc}"
        response = requests.get(api_url, timeout=15)
        response.raise_for_status()
        data = response.json()

        if 'error' in data:
            print(f"{C_RE}\nError de la API: {data['error']}")
            return

        print(f"\n {C_WH}========== {C_GR}INFORMACIÓN DEL RUC (Fuente: api.apis.net.pe){C_WH} ==========")
        print(f" {C_WH}{'Razón Social':<22}:{C_GR} {data.get('nombre', 'N/A')}")
        print(f" {C_WH}{'Nombre Comercial':<22}:{C_GR} {data.get('nombreComercial', 'N/A') or 'No especificado'}")
        print(f" {C_WH}{'Estado':<22}:{C_GR} {data.get('condicion', 'N/A')}")
        print(f" {C_WH}{'Dirección':<22}:{C_GR} {data.get('direccion', 'N/A')}")
        print(f" {C_WH}{'Departamento':<22}:{C_GR} {data.get('departamento', 'N/A')}")
        print(f" {C_WH}{'Provincia':<22}:{C_GR} {data.get('provincia', 'N/A')}")
        print(f" {C_WH}{'Distrito':<22}:{C_GR} {data.get('distrito', 'N/A')}")

    except requests.exceptions.RequestException as e:
        print(f"{C_RE}\nError: No se pudo conectar con el servicio de consulta.")
        print(f"{C_RE}Detalles: {e}")
    except json.JSONDecodeError:
        print(f"{C_RE}\nError: La respuesta de la API no es válida. El RUC podría no existir.")

@is_option
def consulta_RUC_selenium():
    """
    Consulta la información de un RUC utilizando Selenium para interactuar con la página de SUNAT.
    """
    ruc = input(f"\n {C_WH}Ingrese el número de RUC (11 dígitos): {C_GR}")
    if not ruc.isdigit() or len(ruc) != 11:
        print(f"{C_RE}\nError: El RUC debe contener 11 dígitos numéricos.")
        return

    driver = get_driver()
    if not driver:
        return

    try:
        print(f"\n{C_WH}[*] Iniciando navegador para consulta avanzada...")

        url = "https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/frameCriterioBusqueda.jsp"
        driver.get(url)

        ruc_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'txtRuc'))
        )
        ruc_input.send_keys(ruc)

        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'btnAceptar'))
        )
        search_button.click()

        print(f"\n{C_WH}[*] Buscando resultados... El sitio ya no requiere CAPTCHA.")

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'list-group'))
        )

        print(f"\n{C_GR}[+] ¡Resultados encontrados! Extrayendo datos...")
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        data = {}
        results_container = soup.find('div', class_='list-group')
        if results_container:
            items = results_container.find_all('div', class_='list-group-item')
            for item in items:
                key_tag = item.find('h4', class_='list-group-item-heading')
                value_tag = item.find('p', class_='list-group-item-text')

                if key_tag and value_tag:
                    key = ' '.join(key_tag.text.split()).replace(':', '').strip()
                    value = ' '.join(value_tag.text.split()).strip()
                    if key:
                        data[key] = value

        print(f"\n {C_WH}========== {C_GR}INFORMACIÓN DEL RUC (Fuente: SUNAT - Avanzado){C_WH} ==========")
        if data:
            for key, value in data.items():
                print(f" {C_WH}{key:<25}:{C_GR} {value}")
        else:
            print(f" {C_RE}No se encontraron datos para mostrar. La estructura de la página puede haber cambiado.")

    except TimeoutException:
        print(f"{C_RE}\nError: El tiempo de espera se agotó. El RUC podría no existir o la página de SUNAT tardó demasiado en responder.")
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
