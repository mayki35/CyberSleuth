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
def consulta_sunedu():
    """
    Consulta grados y títulos en SUNEDU (Perú) usando Selenium.
    """
    dni = input(f"\n {C_WH}Ingrese el número de DNI (8 dígitos): {C_GR}")
    if not dni.isdigit() or len(dni) != 8:
        print(f"{C_RE}\nError: El DNI debe contener 8 dígitos numéricos.")
        return

    driver = get_driver()
    if not driver:
        return

    try:
        print(f"\n{C_WH}[*] Iniciando navegador para consulta en SUNEDU...")

        driver.get("https://enlinea.sunedu.gob.pe/")

        # Navegar a la sección de verificación de grados
        try:
            verificar_link = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Verifica si estás inscrito en el Registro Nacional de Grados y Títulos')]"))
            )
            verificar_link.click()
        except TimeoutException:
             print(f"{C_YE}[!] No se encontró el enlace directo. Intentando navegar directamente a la URL de búsqueda...")
             driver.get("https://enlinea.sunedu.gob.pe/registro-nacional-grados-titulos")

        # Esperar a que cargue el formulario
        dni_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'nroDocumento')))
        dni_input.send_keys(dni)

        print(f"\n{C_YE}--> ACCIÓN REQUERIDA <_--")
        print(f"{C_WH}Por favor, ingrese el código de seguridad (CAPTCHA) en la ventana de Chrome y haga clic en 'Buscar'.")
        print(f"{C_WH}El script esperará hasta 3 minutos por los resultados...")

        # Esperar a que aparezca la tabla de resultados o un mensaje de no encontrado
        # La tabla suele tener una clase o ID específico. Inspeccionando visualmente o asumiendo estructura estándar.
        # Asumiremos que aparece una tabla con resultados.
        WebDriverWait(driver, 180).until(
            EC.presence_of_element_located((By.TAG_NAME, 'table'))
        )

        print(f"\n{C_GR}[+] ¡Resultados encontrados! Extrayendo datos...")
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        tables = soup.find_all('table')
        
        print(f"\n {C_WH}========== {C_GR}GRADOS Y TÍTULOS (Fuente: SUNEDU){C_WH} ==========")
        
        found_data = False
        for table in tables:
            rows = table.find_all('tr')
            if len(rows) > 1: # Header + data
                found_data = True
                # Asumiendo que la primera fila son cabeceras
                headers = [th.text.strip() for th in rows[0].find_all('th')]
                
                for row in rows[1:]:
                    cells = row.find_all('td')
                    if cells:
                        print(f"\n {C_WH}--- Registro ---{C_GR}")
                        for i, cell in enumerate(cells):
                            if i < len(headers):
                                print(f" {C_WH}{headers[i]:<30}:{C_GR} {cell.text.strip()}")
                            else:
                                print(f" {C_WH}{'Dato Extra':<30}:{C_GR} {cell.text.strip()}")

        if not found_data:
             print(f"{C_YE}Se detectó una tabla pero no parece contener datos de grados. Verifique manualmente.")

    except TimeoutException:
        print(f"{C_RE}\nError: El tiempo de espera se agotó. Posibles causas:")
        print(f"{C_YE}  - No se resolvió el CAPTCHA a tiempo.")
        print(f"{C_YE}  - No se encontraron grados/títulos para el DNI.")
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
