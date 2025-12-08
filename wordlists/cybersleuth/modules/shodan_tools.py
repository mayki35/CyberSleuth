import shodan
from ..config import C_WH, C_GR, C_RE, C_YE, C_END, SHODAN_API_KEY
from ..utils import is_option

def _get_api():
    if not SHODAN_API_KEY:
        print(f"{C_RE}\nError: No se ha configurado la API Key de Shodan en el archivo .env")
        return None
    try:
        return shodan.Shodan(SHODAN_API_KEY)
    except Exception as e:
        print(f"{C_RE}Error al inicializar Shodan: {e}")
        return None

@is_option
def buscar_shodan():
    """
    Busca dispositivos en Shodan usando una consulta (dork).
    """
    api = _get_api()
    if not api: return

    query = input(f"\n {C_WH}Ingrese el término de búsqueda (ej. 'webcam', 'apache', 'port:21'): {C_GR}").strip()
    if not query: return

    print(f"\n{C_WH}[*] Buscando en Shodan: {C_GR}{query}{C_WH}...")

    try:
        results = api.search(query)
        print(f"\n {C_WH}========== {C_GR}RESULTADOS SHODAN ({results['total']}){C_WH} ==========")
        
        # Mostrar los primeros 10 resultados
        for result in results['matches'][:10]:
            ip = result['ip_str']
            port = result['port']
            org = result.get('org', 'n/a')
            location = result.get('location', {})
            country = location.get('country_name', 'n/a')
            
            print(f" {C_GR}[+] {C_WH}{ip}:{port:<5} {C_YE}| {org:<20} | {country}")
            
        if results['total'] > 10:
            print(f"\n{C_YE}... se muestran los primeros 10 resultados.")

    except shodan.APIError as e:
        print(f"{C_RE}Error de la API de Shodan: {e}")

@is_option
def info_host_shodan():
    """
    Obtiene información detallada de una IP en Shodan.
    """
    api = _get_api()
    if not api: return

    ip = input(f"\n {C_WH}Ingrese la IP a investigar: {C_GR}").strip()
    if not ip: return

    print(f"\n{C_WH}[*] Consultando información del host {C_GR}{ip}{C_WH}...")

    try:
        host = api.host(ip)
        
        print(f"\n {C_WH}========== {C_GR}INFORMACIÓN DEL HOST (Shodan){C_WH} ==========")
        print(f" {C_WH}IP                 :{C_GR} {host['ip_str']}")
        print(f" {C_WH}Organización       :{C_GR} {host.get('org', 'n/a')}")
        print(f" {C_WH}Sistema Operativo  :{C_GR} {host.get('os', 'n/a')}")
        print(f" {C_WH}Puertos            :{C_GR} {host.get('ports', [])}")
        print(f" {C_WH}Vulnerabilidades   :{C_RE} {host.get('vulns', [])}")

    except shodan.APIError as e:
        print(f"{C_RE}Error de la API de Shodan (o IP no encontrada): {e}")
