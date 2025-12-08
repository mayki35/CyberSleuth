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
def consulta_papeletas_sat():
    """
    Consulta papeletas pendientes en el SAT de Lima usando Selenium.
    """
    print(f"\n{C_WH}Seleccione el tipo de búsqueda:")
    print(f" {C_WH}1. Por Placa")
    print(f" {C_WH}2. Por DNI")
    opcion = input(f"\n {C_WH}Ingrese una opción (1/2): {C_GR}")

    criterio = ""
    valor = ""

    if opcion == '1':
        criterio = "placa"
        valor = input(f"\n {C_WH}Ingrese el número de placa (ej. ABC-123): {C_GR}").upper().replace("-", "")
    elif opcion == '2':
        criterio = "dni"
        valor = input(f"\n {C_WH}Ingrese el número de DNI (8 dígitos): {C_GR}")
        if not valor.isdigit() or len(valor) != 8:
            print(f"{C_RE}\nError: El DNI debe contener 8 dígitos numéricos.")
            return
    else:
        print(f"{C_RE}\nOpción no válida.")
        return

    driver = get_driver()
    if not driver:
        return

    try:
        print(f"\n{C_WH}[*] Iniciando navegador para consulta en SAT Lima...")

        # URL directa a la consulta de papeletas si es posible, o navegar desde home
        driver.get("https://www.sat.gob.pe/Websitev9")
        
        # Intentar ubicar el widget de consulta rápida en el home o ir a la página específica
        # La URL de consulta suele ser dinámica o estar en un frame.
        # Vamos a intentar ir a una URL más específica si existe, o navegar.
        # Basado en investigación, la URL de virtual sat es compleja.
        # Intentaremos buscar el enlace "Consultas en Línea" -> "Papeletas"
        
        print(f"{C_WH}[*] Navegando a la sección de papeletas...")
        driver.get("https://www.sat.gob.pe/VirtualSAT/modulos/Papeletas.aspx") # URL hipotética basada en patrones comunes, si falla, usaremos navegación

        # Si la URL directa falla, intentamos navegar desde el home
        if "Papeletas" not in driver.title and "SAT" in driver.title:
             driver.get("https://www.sat.gob.pe/websitev9/Consultas/Papeletas")

        # Esperar a que cargue algún input de búsqueda
        # Asumiremos que hay radio buttons o un select para el tipo de búsqueda
        
        print(f"\n{C_YE}--> ACCIÓN REQUERIDA <_--")
        print(f"{C_WH}El script ha abierto la página del SAT.")
        print(f"{C_WH}Por favor, seleccione la opción de búsqueda '{criterio.upper()}', ingrese '{valor}'")
        print(f"{C_WH}Resuelva el CAPTCHA si lo hay y presione BUSCAR.")
        print(f"{C_WH}El script esperará hasta 3 minutos para detectar resultados...")

        # Esperar a que aparezca una tabla de deuda o mensaje de no deuda
        WebDriverWait(driver, 180).until(
            EC.presence_of_element_located((By.TAG_NAME, 'table'))
        )

        print(f"\n{C_GR}[+] ¡Tabla detectada! Extrayendo datos...")
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        # Buscar tablas que parezcan contener resultados
        tables = soup.find_all('table')
        
        print(f"\n {C_WH}========== {C_GR}PAPELETAS / DEUDA (Fuente: SAT Lima){C_WH} ==========")
        
        found_data = False
        for table in tables:
            # Heurística simple: si tiene "Papeleta" o "Infracción" en el texto
            if "Papeleta" in table.text or "Infracción" in table.text or "Deuda" in table.text:
                found_data = True
                rows = table.find_all('tr')
                # Intentar parsear cabeceras
                headers = []
                if rows:
                    headers = [th.text.strip() for th in rows[0].find_all(['th', 'td'])] # A veces usan td para headers
                
                for row in rows[1:]:
                    cells = row.find_all('td')
                    if len(cells) > 1:
                        print(f"\n {C_WH}--- Registro ---{C_GR}")
                        for i, cell in enumerate(cells):
                            header_text = headers[i] if i < len(headers) else f"Columna {i}"
                            print(f" {C_WH}{header_text:<25}:{C_GR} {cell.text.strip()}")
        
        if not found_data:
            print(f"{C_YE}No se detectaron tablas de deuda obvias. Puede que no tenga papeletas o la estructura sea diferente.")
            print(f"{C_WH}Revise la ventana del navegador para confirmar.")

    except TimeoutException:
        print(f"{C_RE}\nError: El tiempo de espera se agotó.")
        print(f"{C_YE}  - Posiblemente no se realizó la búsqueda o no se cargaron los resultados a tiempo.")
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
