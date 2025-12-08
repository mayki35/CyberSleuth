import os
import time
from sys import stderr
from .config import C_CY, C_WH, C_GR, C_YE, C_RE, C_END

def clear_screen():
    """
    Clears the console screen.
    """
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def print_banner():
    """
    Prints the tool banner.
    """
    clear_screen()
    stderr.writelines(f"""{C_CY}
 
 ░█████╗░██╗░░░██╗██████╗░███████╗██████╗░    ░██████╗██╗░░░░░███████╗██╗░░░██╗████████╗██╗░░██╗
 ██╔══██╗╚██╗░██╔╝██╔══██╗██╔════╝██╔══██╗░░░░██╔════╝██║░░░░░██╔════╝██║░░░██║╚══██╔══╝██║░░██║
 ██║░░╚═╝░╚████╔╝░██████╦╝█████╗░░██████╔╝░░░░╚█████╗░██║░░░░░█████╗░░██║░░░██║░░░██║░░░███████║
 ██║░░██╗░░╚██╔╝░░██╔══██╗██╔══╝░░██╔══██╗░░░░░╚═══██╗██║░░░░░██╔══╝░░██║░░░██║░░░██║░░░██╔══██║
 ╚█████╔╝░░░██║░░░██████╦╝███████╗██║░░██║░░░░██████╔╝███████╗███████╗╚██████╔╝░░░██║░░░██║░░██║
 ░╚════╝░░░░╚═╝░░░╚═════╝░╚══════╝╚═╝░░╚═╝░░░░╚═════╝░╚══════╝╚══════╝░╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝
 {C_WH}
                 [ + ]  Una herramienta de investigación {C_GR}OSINT{C_WH}  [ + ]
     {C_YE}No me responzabilizo de nada, utiliza esta herramienta a tu responsabilidad :v{C_WH}
                             {C_YE}Creado por: mayki35{C_WH}
     """)

def print_run_banner():
    """
    Prints the small running banner.
    """
    clear_screen()
    time.sleep(1)
    stderr.writelines(f"""{C_WH}
 
 ───▄▄▄▄▄▄─────▄▄▄▄▄▄
 ─▄█▓▓▓▓▓▓█▄─▄█▓▓▓▓▓▓█▄
 ▐█▓▓▒▒▒▒▒▓▓█▓▓▒▒▒▒▒▓▓█▌
 █▓▓▒▒░╔╗╔═╦═╦═╦═╗░▒▒▓▓█
 █▓▓▒▒░║╠╣╬╠╗║╔╣╩╣░▒▒▓▓█
 ▐█▓▓▒▒╚═╩═╝╚═╝╚═╝▒▒▓▓█▌
 ─▀█▓▓▒▒░░░░░░░░░▒▒▓▓█▀
 ───▀█▓▓▒▒░░░░░▒▒▓▓█▀
 ─────▀█▓▓▒▒░▒▒▓▓█▀
 ──────▀█▓▓▒▓▓█▀
 ────────▀█▓█▀
 ──────────▀
 
 {C_WH}| {C_GR}CyberSleuth- IP ADDRESS {C_WH}|
 {C_WH}|  {C_GR}https://t.me/mayki36   {C_WH}|
 {C_END}""")
    time.sleep(0.5)


from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import SessionNotCreatedException

def get_driver():
    """
    Initializes and returns a Chrome WebDriver with robust error handling.
    Attempts to use webdriver_manager, and handles version mismatches.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Try to use the installed browser binary if found (e.g. /usr/bin/chromium)
    # This helps if webdriver_manager doesn't auto-detect the binary path correctly
    if os.path.exists("/usr/bin/chromium"):
        options.binary_location = "/usr/bin/chromium"
    elif os.path.exists("/usr/bin/google-chrome"):
        options.binary_location = "/usr/bin/google-chrome"

    try:
        # First try: Standard install
        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)
    except SessionNotCreatedException as e:
        print(f"{C_YE}[!] Error de versión de ChromeDriver: {e}")
        print(f"{C_WH}[*] Intentando forzar la descarga de una versión compatible...")
        try:
            # Attempt to parse the actual browser version from the error message
            import re
            error_msg = str(e)
            # Look for "Current browser version is X.X.X.X"
            match = re.search(r"Current browser version is (\d+\.\d+\.\d+\.\d+)", error_msg)
            if match:
                detected_version = match.group(1)
                print(f"{C_WH}[*] Versión del navegador detectada: {detected_version}")
                print(f"{C_WH}[*] Intentando instalar ChromeDriver versión {detected_version}...")
                service = ChromeService(ChromeDriverManager(driver_version=detected_version).install())
                return webdriver.Chrome(service=service, options=options)
            else:
                # Fallback if regex fails, try a generally recent version or just fail gracefully
                print(f"{C_YE}[!] No se pudo detectar la versión exacta del error.")
                # Try a known recent stable version as a last ditch effort?
                # Or just re-raise.
                raise e
            
        except Exception as e2:
             print(f"{C_RE}[!] No se pudo iniciar el driver automáticamente: {e2}")
             print(f"{C_YE}[!] Intente actualizar su navegador Chrome o instalar 'chromium-driver' manualmente.")
             return None
    except Exception as e:
        print(f"{C_RE}[!] Error al iniciar WebDriver: {e}")
        return None

def is_option(func):
    """Decorator to show banner before function execution."""
    def wrapper(*args, **kwargs):
        print_run_banner()
        return func(*args, **kwargs)
    return wrapper
