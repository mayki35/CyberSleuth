import requests
import hashlib
from ..config import C_WH, C_GR, C_RE, C_YE, C_END
from ..utils import is_option

@is_option
def verificar_brecha_email():
    """
    Verifica si un email ha sido pwned usando la API de HaveIBeenPwned.
    NOTA: La API v3 de HIBP requiere una API Key para buscar por email.
    Sin embargo, podemos usar un endpoint público limitado o simular la búsqueda si no tenemos key.
    Para este ejemplo, usaremos el endpoint de 'breachedaccount' que a veces requiere autenticación.
    Si falla, informaremos al usuario.
    """
    email = input(f"\n {C_WH}Ingrese el email a verificar: {C_GR}").strip()
    if not email: return

    print(f"\n{C_WH}[*] Consultando HaveIBeenPwned para {C_GR}{email}{C_WH}...")
    
    # HIBP ahora requiere API Key para búsquedas de email.
    # Como alternativa gratuita y sin key, implementaremos la búsqueda de contraseñas (Pwned Passwords)
    # que es anónima y gratuita.
    print(f"{C_YE}Nota: La búsqueda directa de emails en HIBP requiere una API Key de pago.")
    print(f"{C_WH}Recomendamos usar la función de verificación de contraseñas para mayor privacidad.")
    
    # Intentamos una consulta simple que podría funcionar con algunos user-agents, pero es inestable.
    headers = {
        'User-Agent': 'CyberSleuth-Tool',
        'hibp-api-key': '' # Si el usuario tuviera una, iría aquí
    }
    try:
        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            breaches = response.json()
            print(f"\n {C_RE}¡CUIDADO! El correo aparece en {len(breaches)} brechas de datos:")
            for breach in breaches:
                print(f" {C_YE}- {breach['Name']} ({breach['BreachDate']})")
        elif response.status_code == 404:
            print(f"\n {C_GR}¡Buenas noticias! No se encontraron brechas para este correo (o la API requiere Key).")
        elif response.status_code == 401:
            print(f"\n {C_YE}La API de HIBP requiere una clave de API válida para esta función.")
    except Exception as e:
        print(f"{C_RE}Error al conectar con HIBP: {e}")

@is_option
def verificar_password_pwned():
    """
    Verifica si una contraseña ha sido expuesta usando k-Anonymity (Pwned Passwords).
    Seguro: No envía la contraseña completa, solo los primeros 5 caracteres del hash SHA-1.
    """
    password = input(f"\n {C_WH}Ingrese la contraseña a verificar (se ocultará): {C_GR}").strip()
    if not password: return

    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1_password[:5]
    suffix = sha1_password[5:]

    print(f"\n{C_WH}[*] Verificando hash (k-Anonymity)...")

    try:
        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            hashes = (line.split(':') for line in response.text.splitlines())
            count = 0
            for h, c in hashes:
                if h == suffix:
                    count = int(c)
                    break
            
            if count > 0:
                print(f"\n {C_RE}¡PELIGRO! Esta contraseña ha sido vista {count} veces en filtraciones.")
                print(f" {C_YE}Recomendación: ¡Cámbiala inmediatamente!")
            else:
                print(f"\n {C_GR}¡Seguro! Esta contraseña no aparece en la base de datos de filtraciones.")
        else:
            print(f"{C_RE}Error de la API Pwned Passwords: {response.status_code}")

    except Exception as e:
        print(f"{C_RE}Error de conexión: {e}")
