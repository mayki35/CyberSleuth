import requests
from ..config import C_WH, C_GR, C_RE, C_YE, C_END
from ..utils import is_option

@is_option
def buscar_crtsh():
    """
    Busca subdominios en los registros de Transparencia de Certificados (crt.sh).
    """
    domain = input(f"\n {C_WH}Ingrese el dominio a investigar (ej. facebook.com): {C_GR}").strip()
    if not domain:
        print(f"{C_RE}\nError: El dominio no puede estar vacío.")
        return

    print(f"\n{C_WH}[*] Consultando crt.sh para {C_GR}{domain}{C_WH} (esto puede tardar unos segundos)...")

    try:
        url = f"https://crt.sh/?q=%.{domain}&output=json"
        response = requests.get(url, timeout=20)
        
        if response.status_code != 200:
            print(f"{C_RE}Error al conectar con crt.sh (Código: {response.status_code})")
            return

        data = response.json()
        subdomains = set()
        
        for entry in data:
            name_value = entry.get('name_value')
            if name_value:
                # crt.sh puede devolver múltiples dominios por línea separados por saltos de línea
                for sub in name_value.split('\n'):
                    if '*' not in sub: # Ignorar wildcards
                        subdomains.add(sub)

        print(f"\n {C_WH}========== {C_GR}SUBDOMINIOS ENCONTRADOS (crt.sh){C_WH} ==========")
        if subdomains:
            print(f" {C_WH}Total encontrados: {C_GR}{len(subdomains)}\n")
            for sub in sorted(subdomains):
                print(f" {C_GR}[+] {C_WH}{sub}")
        else:
            print(f"{C_YE}No se encontraron subdominios en los registros de certificados.")

    except requests.exceptions.RequestException as e:
        print(f"{C_RE}\nError de conexión: {e}")
    except Exception as e:
        print(f"{C_RE}\nOcurrió un error inesperado: {e}")
