import requests
from ..config import C_WH, C_GR, C_RE, C_YE, C_END
from ..utils import is_option

@is_option
def consultar_wayback():
    """
    Busca URLs archivadas en Wayback Machine.
    """
    domain = input(f"\n {C_WH}Ingrese el dominio a buscar (ej. example.com): {C_GR}").strip()
    if not domain:
        return

    limit = input(f" {C_WH}Límite de resultados (Enter para 50): {C_GR}").strip()
    if not limit.isdigit():
        limit = 50
    else:
        limit = int(limit)

    print(f"\n{C_WH}[*] Consultando Wayback Machine para {C_GR}{domain}{C_WH}...")

    try:
        # Usamos la API CDX de Wayback Machine
        url = f"http://web.archive.org/cdx/search/cdx?url=*.{domain}/*&output=json&fl=original&collapse=urlkey&limit={limit}"
        response = requests.get(url, timeout=20)
        
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                print(f"\n {C_WH}========== {C_GR}ARCHIVOS ENCONTRADOS (Wayback){C_WH} ==========")
                # La primera fila suele ser el encabezado ['original']
                for row in data[1:]:
                    print(f" {C_GR}[+] {C_WH}{row[0]}")
                
                if len(data) > limit:
                     print(f"\n{C_YE}... y más resultados (limitado a {limit})")
            else:
                print(f"{C_YE}No se encontraron registros archivados.")
        else:
            print(f"{C_RE}Error al consultar Wayback Machine (Código: {response.status_code})")

    except requests.exceptions.RequestException as e:
        print(f"{C_RE}\nError de conexión: {e}")
