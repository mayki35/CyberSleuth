import requests
from ..config import C_WH, C_GR, C_RE, C_YE, C_CY, C_END
from ..utils import is_option

@is_option
def analizar_cabeceras():
    """
    Analiza las cabeceras HTTP de un sitio web en busca de configuraciones de seguridad.
    """
    url = input(f"\n {C_WH}Ingrese la URL (ej. https://google.com): {C_GR}").strip()
    if not url.startswith('http'):
        url = 'https://' + url

    try:
        print(f"\n{C_WH}[*] Conectando a {C_GR}{url}{C_WH}...")
        response = requests.get(url, timeout=10)
        headers = response.headers

        print(f"\n {C_WH}========== {C_GR}ANÁLISIS DE CABECERAS{C_WH} ==========")
        
        security_headers = [
            'Strict-Transport-Security',
            'X-Frame-Options',
            'X-Content-Type-Options',
            'Content-Security-Policy',
            'X-XSS-Protection',
            'Referrer-Policy',
            'Permissions-Policy'
        ]

        print(f"\n{C_CY}[ Cabeceras de Seguridad ]{C_END}")
        for header in security_headers:
            if header in headers:
                print(f" {C_GR}[OK] {C_WH}{header:<30}: {C_GR}{headers[header]}")
            else:
                print(f" {C_RE}[FALTA] {C_WH}{header}")

        print(f"\n{C_CY}[ Información del Servidor ]{C_END}")
        server_headers = ['Server', 'X-Powered-By', 'X-AspNet-Version', 'X-Generator']
        for header in server_headers:
            if header in headers:
                print(f" {C_YE}[INFO] {C_WH}{header:<30}: {C_GR}{headers[header]}")

    except requests.exceptions.RequestException as e:
        print(f"{C_RE}\nError al conectar: {e}")

@is_option
def obtener_robots():
    """
    Descarga y muestra el archivo robots.txt de un sitio.
    """
    url = input(f"\n {C_WH}Ingrese la URL (ej. https://google.com): {C_GR}").strip()
    if not url.startswith('http'):
        url = 'https://' + url
    
    robots_url = f"{url.rstrip('/')}/robots.txt"

    try:
        print(f"\n{C_WH}[*] Buscando {C_GR}{robots_url}{C_WH}...")
        response = requests.get(robots_url, timeout=10)
        
        if response.status_code == 200:
            print(f"\n {C_WH}========== {C_GR}CONTENIDO DE ROBOTS.TXT{C_WH} ==========")
            print(f"{C_GR}{response.text}")
        else:
            print(f"{C_YE}No se encontró el archivo robots.txt (Código: {response.status_code})")

    except requests.exceptions.RequestException as e:
        print(f"{C_RE}\nError al conectar: {e}")
