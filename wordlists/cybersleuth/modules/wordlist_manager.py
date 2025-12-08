import os
import requests
from ..config import C_WH, C_GR, C_RE, C_YE, C_END, BASE_DIR
from ..utils import is_option

WORDLISTS_DIR = os.path.join(BASE_DIR, 'wordlists')

# URLs de diccionarios populares (SecLists)
WORDLIST_URLS = {
    'rockyou_top_100k.txt': 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10k-most-common.txt',
    'common_users.txt': 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Usernames/top-usernames-shortlist.txt',
    'directory_list_medium.txt': 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/common.txt',
    'subdomains_top1million.txt': 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/subdomains-top1million-5000.txt'
}

@is_option
def descargar_diccionarios():
    """
    Descarga diccionarios populares de SecLists.
    """
    if not os.path.exists(WORDLISTS_DIR):
        os.makedirs(WORDLISTS_DIR)

    print(f"\n {C_WH}========== {C_GR}GESTOR DE DICCIONARIOS{C_WH} ==========")
    print(f" {C_WH}Los archivos se guardarán en la carpeta: {C_GR}{WORDLISTS_DIR}/")

    for name, url in WORDLIST_URLS.items():
        path = os.path.join(WORDLISTS_DIR, name)
        
        if os.path.exists(path):
            print(f" {C_GR}[OK] {C_WH}{name} ya existe.")
            continue

        print(f" {C_YE}[..] {C_WH}Descargando {name}...")
        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            with open(path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f" {C_GR}[OK] {C_WH}Descarga completada.")
        except Exception as e:
            print(f" {C_RE}[X] {C_WH}Error al descargar {name}: {e}")

    print(f"\n{C_GR}¡Proceso finalizado!")
