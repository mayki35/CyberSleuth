# IMPORT MODULE
import json
import shutil
import xml.etree.ElementTree as ET
from collections import defaultdict
import socket
import subprocess
import requests
import time
import concurrent.futures
import tempfile
import os
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from sys import stderr, exit
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from stegano import lsb
import mutagen
from PyPDF2 import PdfReader, PdfWriter
 
# Constantes para colores de la consola, haciendo el código más limpio y legible.
C_BL = '\033[30m'
C_RE = '\033[1;31m'
C_GR = '\033[1;32m'
C_YE = '\033[1;33m'
C_BLU = '\033[1;34m'
C_MAGE = '\033[1;35m'
C_CY = '\033[1;36m'
C_WH = '\033[1;37m'
C_END = '\033[0m' # Reset a color por defecto
 
# Decorador para adjuntar la función run_banner a otras funciones
def is_option(func):
    def wrapper(*args, **kwargs):
        run_banner()
        return func(*args, **kwargs)

    return wrapper


# Funciones para el menú
@is_option
def informacion_ip():
    """
    Rastrea la información de una dirección IP.
    """
    ip = input(f"{C_WH}\n Ingrese la IP objetivo: {C_GR}")
    print()
    try:
        print(f' {C_WH}============= {C_GR}MOSTRAR INFORMACIÓN DE LA DIRECCIÓN IP {C_WH}=============')
        req_api = requests.get(f"http://ipwho.is/{ip}", timeout=10)
        req_api.raise_for_status()  # Lanza una excepción para códigos de estado HTTP erróneos (4xx o 5xx)
        ip_data = req_api.json()

        if not ip_data.get("success", True):
            print(f"{C_RE}Error de la API: {ip_data.get('message', 'Dirección IP inválida')}")
            return

        time.sleep(1)
        connection_data = ip_data.get("connection", {})
        timezone_data = ip_data.get("timezone", {})
        flag_data = ip_data.get("flag", {})

        print(f"{C_WH}\n IP objetivo       :{C_GR}", ip)
        print(f"{C_WH} Tipo de IP         :{C_GR}", ip_data.get("type", "N/A"))
        print(f"{C_WH} País             :{C_GR}", ip_data.get("country", "N/A"))
        print(f"{C_WH} Código de País    :{C_GR}", ip_data.get("country_code", "N/A"))
        print(f"{C_WH} Ciudad            :{C_GR}", ip_data.get("city", "N/A"))
        print(f"{C_WH} Región          :{C_GR}", ip_data.get("region", "N/A"))
        lat = ip_data.get('latitude')
        lon = ip_data.get('longitude')
        if lat and lon:
            print(f"{C_WH} Latitud         :{C_GR}", lat)
            print(f"{C_WH} Longitud        :{C_GR}", lon)
            print(f"{C_WH} Mapa            :{C_GR}", f"https://www.google.com/maps/@{lat},{lon},8z")
        print(f"{C_WH} Código Postal     :{C_GR}", ip_data.get("postal", "N/A"))
        print(f"{C_WH} Código de Llamada :{C_GR}", ip_data.get("calling_code", "N/A"))
        print(f"{C_WH} Capital           :{C_GR}", ip_data.get("capital", "N/A"))
        print(f"{C_WH} Bandera del País  :{C_GR}", flag_data.get("emoji", "N/A"))
        print(f"{C_WH} ASN             :{C_GR}", connection_data.get("asn", "N/A"))
        print(f"{C_WH} ORG             :{C_GR}", connection_data.get("org", "N/A"))
        print(f"{C_WH} ISP             :{C_GR}", connection_data.get("isp", "N/A"))
        print(f"{C_WH} UTC             :{C_GR}", timezone_data.get("utc", "N/A"))
        print(f"{C_WH} Hora Actual       :{C_GR}", timezone_data.get("current_time", "N/A"))
    except requests.exceptions.RequestException as e:
        print(f"{C_RE}\nError: No se pudo conectar a la API. Por favor, verifique su conexión a Internet.")
        print(f"{C_RE}Detalles: {e}")


@is_option
def informacion_celular ():
    """
    Obtiene información sobre un número de teléfono.
    """
    User_phone = input(
        f"\n {C_WH}Ingrese el número de teléfono objetivo {C_GR}Ej [+51987654321] {C_WH}: {C_GR}")
    default_region = "PE"  # País por defecto: Perú

    try:
        parsed_number = phonenumbers.parse(User_phone, default_region)
        
        if not phonenumbers.is_valid_number(parsed_number):
            print(f"{C_RE}\nError: El número de teléfono proporcionado no es válido.")
            return

        region_code = phonenumbers.region_code_for_number(parsed_number)
        jenis_provider = carrier.name_for_number(parsed_number, "en")
        location = geocoder.description_for_number(parsed_number, "id")
        timezone1 = timezone.time_zones_for_number(parsed_number)
        timezoneF = ', '.join(timezone1)

        print(f"\n {C_WH}========== {C_GR}MOSTRAR INFORMACIÓN DEL NÚMERO DE TELÉFONO {C_WH}==========")
        print(f"\n {C_WH}Ubicación             :{C_GR} {location}")
        print(f" {C_WH}Código de Región          :{C_GR} {region_code}")
        print(f" {C_WH}Zona Horaria             :{C_GR} {timezoneF}")
        print(f" {C_WH}Operador             :{C_GR} {jenis_provider or 'N/A'}")
        print(f" {C_WH}Formato Internacional :{C_GR} {phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}")
        print(f" {C_WH}Formato E.164         :{C_GR} {phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)}")
        print(f" {C_WH}Código de País         :{C_GR} {parsed_number.country_code}")
        
        number_type = phonenumbers.number_type(parsed_number)
        if number_type == phonenumbers.PhoneNumberType.MOBILE:
            print(f" {C_WH}Tipo                 :{C_GR} Este es un número de móvil")
        elif number_type == phonenumbers.PhoneNumberType.FIXED_LINE:
            print(f" {C_WH}Tipo                 :{C_GR} Este es un número de línea fija")
        else:
            print(f" {C_WH}Tipo                 :{C_GR} Este es otro tipo de número")

    except phonenumbers.phonenumberutil.NumberParseException as e:
        print(f"{C_RE}\nError: Formato de número de teléfono inválido. Por favor, incluya el código de país (ej., +51, +1).")
        print(f"{C_RE}Detalles: {e}")


@is_option
def informacion_por_nombre():
    """
    Rastrea la presencia de un nombre de usuario en varias redes sociales.
    """
    username = input(f"\n {C_WH}Ingrese el nombre de usuario: {C_GR}")
    results = {}
    social_media = [
        {"url": "https://www.facebook.com/{}", "name": "Facebook"},
        {"url": "https://www.twitter.com/{}", "name": "Twitter"},
        {"url": "https://www.instagram.com/{}", "name": "Instagram"},
        {"url": "https://www.linkedin.com/in/{}", "name": "LinkedIn"},
        {"url": "https://www.github.com/{}", "name": "GitHub"},
        {"url": "https://www.pinterest.com/{}", "name": "Pinterest"},
        {"url": "https://www.tumblr.com/{}", "name": "Tumblr"},
        {"url": "https://www.youtube.com/{}", "name": "Youtube"},
        {"url": "https://soundcloud.com/{}", "name": "SoundCloud"},
        {"url": "https://www.snapchat.com/add/{}", "name": "Snapchat"},
        {"url": "https://www.tiktok.com/@{}", "name": "TikTok"},
        {"url": "https://www.behance.net/{}", "name": "Behance"},
        {"url": "https://www.medium.com/@{}", "name": "Medium"},
        {"url": "https://www.quora.com/profile/{}", "name": "Quora"},
        {"url": "https://www.flickr.com/people/{}", "name": "Flickr"},
        {"url": "https://www.periscope.tv/{}", "name": "Periscope"},
        {"url": "https://www.twitch.tv/{}", "name": "Twitch"},
        {"url": "https://www.dribbble.com/{}", "name": "Dribbble"},
        {"url": "https://www.stumbleupon.com/stumbler/{}", "name": "StumbleUpon"},
        {"url": "https://www.ello.co/{}", "name": "Ello"},
        {"url": "https://www.producthunt.com/@{}", "name": "Product Hunt"},
        {"url": "https://www.telegram.me/{}", "name": "Telegram"},
        {"url": "https://www.weheartit.com/{}", "name": "We Heart It"}
    ]
    
    print(f"\n{C_WH}[*] Buscando el nombre de usuario '{C_GR}{username}{C_WH}' en {len(social_media)} sitios...")

    def check_username(site):
        url = site['url'].format(username)
        try:
            response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            if response.status_code == 200:
                return site['name'], url
            return site['name'], f"{C_YE}No Encontrado{C_WH}"
        except requests.exceptions.RequestException:
            return site['name'], f"{C_RE}Error (Fallo de Conexión){C_WH}"

    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        future_to_url = {executor.submit(check_username, site): site for site in social_media}
        for future in concurrent.futures.as_completed(future_to_url):
            name, url = future.result()
            results[name] = url

    print(f"\n {C_WH}========== {C_GR}MOSTRAR INFORMACIÓN DEL NOMBRE DE USUARIO {C_WH}==========")
    print()
    for site_info in social_media: # Itera sobre la lista original para mantener el orden
        site_name = site_info['name']
        url = results.get(site_name, f"{C_RE}Error Desconocido{C_WH}")
        status_color = C_GR if "http" in url else C_YE if "No Encontrado" in url else C_RE
        print(f" {C_WH}[ {C_GR}+ {C_WH}] {site_name:<15} : {status_color}{url}{C_END}")


@is_option
def showIP():
    """
    Muestra la dirección IP actual del usuario.
    """
    try:
        response = requests.get('https://api.ipify.org/', timeout=10)
        response.raise_for_status()
        show_ip = response.text

        print(f"\n {C_WH}========== {C_GR}MOSTRAR INFORMACIÓN DE TU IP {C_WH}==========")
        print(f"\n {C_WH}[{C_GR} + {C_WH}] Tu Dirección IP : {C_GR}{show_ip}")
        print(f"\n {C_WH}==============================================")
    except requests.exceptions.RequestException as e:
        print(f"{C_RE}\nError: No se pudo obtener tu dirección IP. Por favor, verifica tu conexión a Internet.")


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

    # Usando una API de terceros estable para asegurar la funcionalidad.
    try:
        api_url = f"https://api.apis.net.pe/v1/ruc?numero={ruc}"
        response = requests.get(api_url, timeout=15)
        response.raise_for_status()
        data = response.json()

        # La API devuelve una clave 'error' si algo sale mal.
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
def consulta_DNI():
    """
    Consulta la información de un DNI (Documento Nacional de Identidad) en Perú desde múltiples fuentes para mayor estabilidad y detalle.
    """
    dni = input(f"\n {C_WH}Ingrese el número de DNI (8 dígitos): {C_GR}")
    if not dni.isdigit() or len(dni) != 8:
        print(f"{C_RE}\nError: El DNI debe contener 8 dígitos numéricos.")
        return
    print(f"\n{C_WH}[*] Iniciando consulta multifuente para el DNI {C_GR}{dni}{C_WH}...")

    # Diccionario para guardar toda la información recopilada
    full_data = {
        'dni': dni,
        'nombres': 'N/A',
        'apellidoPaterno': 'N/A',
        'apellidoMaterno': 'N/A',
        'sexo': 'N/A',
        'fechaNacimiento': 'N/A',
        'digitoVerificacion': 'N/A',
        'domicilio': 'N/A'
    }

    # --- Función auxiliar para calcular el dígito de verificación del DNI ---
    def _get_code(dni_str):
        """Calcula el dígito de verificación del DNI."""
        suma = 5
        hash_multipliers = [3, 2, 7, 6, 5, 4, 3, 2]
        for i in range(8):
            suma += int(dni_str[i]) * hash_multipliers[i]
        resto = suma % 11
        digito = 11 - resto
        if digito == 11: return 0
        if digito == 10: return 1 # Algunas implementaciones usan 'K', pero el valor numérico es 1
        return digito

    full_data['digitoVerificacion'] = _get_code(dni)

    # --- Fuente 1: apis.net.pe (Fuente principal para nombres) ---
    print(f"{C_WH}[*] Consultando fuente 1 (apis.net.pe)...")
    try:
        api_url = f"https://api.apis.net.pe/v1/dni?numero={dni}"
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if 'error' not in data and data.get('nombres'):
            full_data['nombres'] = data.get('nombres')
            full_data['apellidoPaterno'] = data.get('apellidoPaterno')
            full_data['apellidoMaterno'] = data.get('apellidoMaterno')
            print(f"{C_GR}[+] Datos básicos obtenidos de la fuente 1.")
        else:
            print(f"{C_YE}[-] La fuente 1 no devolvió datos válidos.")
    except (requests.exceptions.RequestException, json.JSONDecodeError):
        print(f"{C_RE}[!] Falló la consulta a la fuente 1.")

    # --- Fuente 2: Essalud (Para fecha de nacimiento y sexo) ---
    print(f"{C_WH}[*] Consultando fuente 2 (Essalud)...")
    try:
        essalud_url = 'https://ww1.essalud.gob.pe/sisep/postulante/postulante/postulante_obtenerDatosPostulante.htm'
        response = requests.get(essalud_url, params={'strDni': dni}, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get('DatosPerson'):
            person_data = data['DatosPerson'][0]
            full_data['fechaNacimiento'] = person_data.get('FechaNacimiento', 'N/A')
            full_data['sexo'] = 'MASCULINO' if person_data.get('Sexo') == '1' else 'FEMENINO' if person_data.get('Sexo') == '2' else 'N/A'
            print(f"{C_GR}[+] Datos demográficos obtenidos de la fuente 2.")
        else:
            print(f"{C_YE}[-] La fuente 2 no devolvió datos válidos.")
    except (requests.exceptions.RequestException, json.JSONDecodeError):
        print(f"{C_RE}[!] Falló la consulta a la fuente 2.")

    # --- Fuente 3: reniec.cloud (Fuente de respaldo para nombres) ---
    # Solo se consulta si la primera fuente falló en obtener los nombres.
    if full_data['nombres'] == 'N/A':
        print(f"{C_WH}[*] Consultando fuente 3 (reniec.cloud) como respaldo...")
        try:
            reniec_url = f"https://api.reniec.cloud/dni/{dni}"
            response = requests.get(reniec_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data.get('nombres'):
                full_data['nombres'] = data.get('nombres')
                full_data['apellidoPaterno'] = data.get('apellido_paterno')
                full_data['apellidoMaterno'] = data.get('apellido_materno')
                print(f"{C_GR}[+] Datos básicos obtenidos de la fuente 3.")
            else:
                print(f"{C_YE}[-] La fuente 3 no devolvió datos válidos.")
        except (requests.exceptions.RequestException, json.JSONDecodeError):
            print(f"{C_RE}[!] Falló la consulta a la fuente 3.")

    # --- Fuente 4: facturacionsunat.com (Fuente de respaldo para varios datos) ---
    # Se consulta si aún faltan datos clave.
    if full_data['nombres'] == 'N/A' or full_data['fechaNacimiento'] == 'N/A':
        print(f"{C_WH}[*] Consultando fuente 4 (facturacionsunat.com) como respaldo...")
        try:
            sunat_url = 'http://www.facturacionsunat.com/vfpsws/vfpsconsbsapi.php'
            params = {'dni': dni, 'token': '87290E49D50B519', 'format': 'json'}
            response = requests.get(sunat_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data.get('nombres'):
                if full_data['nombres'] == 'N/A':
                    full_data['nombres'] = data.get('nombres', 'N/A')
                    full_data['apellidoPaterno'] = data.get('ape_paterno', 'N/A')
                    full_data['apellidoMaterno'] = data.get('ape_materno', 'N/A')
                if full_data['fechaNacimiento'] == 'N/A':
                    full_data['fechaNacimiento'] = data.get('feNacimiento', 'N/A')
                full_data['domicilio'] = data.get('domicilio', 'N/A')
                print(f"{C_GR}[+] Datos adicionales obtenidos de la fuente 4.")
            else:
                print(f"{C_YE}[-] La fuente 4 no devolvió datos válidos.")
        except (requests.exceptions.RequestException, json.JSONDecodeError):
            print(f"{C_RE}[!] Falló la consulta a la fuente 4.")

    # --- Fuente 5: dniruc.apisperu.com (Fuente de respaldo final) ---
    # Se consulta si aún faltan los nombres.
    if full_data['nombres'] == 'N/A':
        print(f"{C_WH}[*] Consultando fuente 5 (dniruc.apisperu.com) como respaldo final...")
        try:
            # NOTA: El token de esta API es de 2021 y puede estar expirado.
            apisperu_url = f"https://dniruc.apisperu.com/api/v1/dni/{dni}?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImdyYWR5Mzl1X24yOTFpQG5hZnhvLmNvbSJ9.cl5KQzsXaRuLuwEUWNJDLX_Zh2R_HkBsn9_YEP4keio"
            response = requests.get(apisperu_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data.get('success') is not False and data.get('nombres'):
                full_data['nombres'] = data.get('nombres', 'N/A')
                full_data['apellidoPaterno'] = data.get('apellidoPaterno', 'N/A')
                full_data['apellidoMaterno'] = data.get('apellidoMaterno', 'N/A')
                print(f"{C_GR}[+] Datos básicos obtenidos de la fuente 5.")
            else:
                print(f"{C_YE}[-] La fuente 5 no devolvió datos válidos.")
        except (requests.exceptions.RequestException, json.JSONDecodeError):
            print(f"{C_RE}[!] Falló la consulta a la fuente 5.")

    # --- Fuente 6: api.dniruc.com (Fuente de respaldo final) ---
    if full_data['nombres'] == 'N/A':
        print(f"{C_WH}[*] Consultando fuente 6 (api.dniruc.com) como respaldo final...")
        try:
            dniruc_url = f"https://api.dniruc.com/api/v1/dni/{dni}?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImFkbWluQGdtYWlsLmNvbSJ9.8_zO-HCo3n2iW1a4w2x2Xv2ss2otS0G22f2x2Jd2Qf4"
            response = requests.get(dniruc_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data.get('success') is True and data.get('nombres'):
                full_data['nombres'] = data.get('nombres', 'N/A')
                full_data['apellidoPaterno'] = data.get('apellidoPaterno', 'N/A')
                full_data['apellidoMaterno'] = data.get('apellidoMaterno', 'N/A')
                print(f"{C_GR}[+] Datos básicos obtenidos de la fuente 6.")
            else:
                print(f"{C_YE}[-] La fuente 6 no devolvió datos válidos: {data.get('message')}")
        except (requests.exceptions.RequestException, json.JSONDecodeError):
            print(f"{C_RE}[!] Falló la consulta a la fuente 6.")


    print(f"\n {C_WH}========== {C_GR}INFORMACIÓN CONSOLIDADA DEL DNI{C_WH} ==========")
    print(f" {C_WH}{'Nombres':<22}:{C_GR} {full_data.get('nombres', 'N/A')}")
    print(f" {C_WH}{'Apellido Paterno':<22}:{C_GR} {full_data.get('apellidoPaterno', 'N/A')}")
    print(f" {C_WH}{'Apellido Materno':<22}:{C_GR} {full_data.get('apellidoMaterno', 'N/A')}")
    print(f" {C_WH}{'Número de DNI':<22}:{C_GR} {full_data.get('dni', 'N/A')}")
    print(f" {C_WH}{'Dígito Verificación':<22}:{C_GR} {full_data.get('digitoVerificacion', 'N/A')}")
    print(f" {C_WH}{'Fecha de Nacimiento':<22}:{C_GR} {full_data.get('fechaNacimiento', 'N/A')}")
    print(f" {C_WH}{'Sexo':<22}:{C_GR} {full_data.get('sexo', 'N/A')}")
    print(f" {C_WH}{'Domicilio (SUNAT)':<22}:{C_GR} {full_data.get('domicilio', 'N/A')}")


@is_option
def consulta_RUC_selenium():
    """
    Consulta la información de un RUC utilizando Selenium para interactuar con la página de SUNAT.
    """
    ruc = input(f"\n {C_WH}Ingrese el número de RUC (11 dígitos): {C_GR}")
    if not ruc.isdigit() or len(ruc) != 11:
        print(f"{C_RE}\nError: El RUC debe contener 11 dígitos numéricos.")
        return

    driver = None
    try:
        print(f"\n{C_WH}[*] Iniciando navegador para consulta avanzada...")
        # Usar webdriver-manager para gestionar automáticamente el chromedriver
        service = ChromeService(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        # Opciones para una ejecución más limpia y estable
        options.add_argument("--start-maximized")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)


        driver = webdriver.Chrome(service=service, options=options)

        url = "https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/frameCriterioBusqueda.jsp"
        driver.get(url)

        # Esperar y rellenar el campo de RUC.
        ruc_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'txtRuc'))
        )
        ruc_input.send_keys(ruc)

        # Hacer clic en el botón de búsqueda.
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'btnAceptar'))
        )
        search_button.click()

        print(f"\n{C_WH}[*] Buscando resultados... El sitio ya no requiere CAPTCHA.")

        # Esperar a que aparezca el contenedor de resultados.
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'list-group'))
        )

        print(f"\n{C_GR}[+] ¡Resultados encontrados! Extrayendo datos...")
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        data = {}
        # Los datos están en una lista de divs, no en una tabla.
        # Esta lógica coincide con la estructura actual de la página de SUNAT.
        results_container = soup.find('div', class_='list-group')
        if results_container:
            # Encontrar todos los items de datos individuales.
            items = results_container.find_all('div', class_='list-group-item')
            for item in items:
                key_tag = item.find('h4', class_='list-group-item-heading')
                value_tag = item.find('p', class_='list-group-item-text')

                if key_tag and value_tag:
                    # Limpiar el texto y guardarlo.
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
            # Guardar el HTML de la página para depuración
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html', encoding='utf-8') as f:
                f.write(driver.page_source)
                print(f"{C_YE}[!] Se ha guardado el estado actual de la página para depuración en: {f.name}")
    finally:
        if driver:
            driver.quit()
            print(f"\n{C_WH}[*] Navegador cerrado.")

@is_option
def consulta_lineas_osiptel():
    """
    Consulta el número de líneas móviles registradas a nombre de un DNI en el servicio de OSIPTEL (Perú) utilizando Selenium.
    """
    from collections import defaultdict
    dni = input(f"\n {C_WH}Ingrese el número de DNI (8 dígitos): {C_GR}")
    if not dni.isdigit() or len(dni) != 8:
        print(f"{C_RE}\nError: El DNI debe contener 8 dígitos numéricos.")
        return

    driver = None
    try:
        print(f"\n{C.WH}[*] Iniciando navegador para consulta de líneas...")
        service = ChromeService(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        # Opciones para una ejecución más limpia y estable.
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(service=service, options=options)

        url = "https://checatuslineas.osiptel.gob.pe/"
        driver.get(url)

        # Manejo del modal de política de privacidad.
        try:
            # 1. Esperar a que el contenedor del diálogo sea visible.
            dialog = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div.v-dialog--active[role='dialog']"))
            )
            print(f"{C_WH}[*] Modal de política de privacidad detectado. Intentando aceptar...")

            # 2. Encontrar el botón dentro del diálogo y hacer clic con JavaScript para mayor fiabilidad.
            accept_button = dialog.find_element(By.XPATH, ".//button[contains(., 'ACEPTAR')]")
            driver.execute_script("arguments[0].click();", accept_button)

            # 3. Esperar a que el diálogo desaparezca para confirmar que la acción fue exitosa.
            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.v-dialog--active[role='dialog']"))
            )
            print(f"{C_GR}[+] Política de privacidad aceptada correctamente.")
        except TimeoutException:
            print(f"{C_YE}[!] No se detectó el modal de política de privacidad en 30 segundos (o ya fue aceptado). Continuando...")

        # Selección del tipo de documento (DNI).
        print(f"{C_WH}[*] Seleccionando el tipo de documento (DNI)...")
        # Esperar a que el dropdown esté presente y usar un clic de JavaScript.
        doc_type_dropdown = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'document-type'))
        )
        driver.execute_script("arguments[0].click();", doc_type_dropdown)
        time.sleep(0.5) # Pausa para que se rendericen las opciones.

        # Hacer clic en la opción "DNI"
        dni_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'v-list-item-title') and text()='DNI']"))
        )
        dni_option.click()

        # Ingresar DNI y esperar acción del usuario.
        dni_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'document-number'))
        )
        dni_input.send_keys(dni)

        print(f"\n{C_YE}--> ACCIÓN REQUERIDA <_--")
        print(f"{C_WH}Se ha abierto una ventana de Chrome.")
        print(f"{C_WH}Por favor, resuelva el CAPTCHA y haga clic en el botón 'Consultar'.")
        print(f"{C_WH}El script esperará hasta 2 minutos...")
        
        # Esperar a que el usuario resuelva el CAPTCHA y aparezcan los resultados.
        WebDriverWait(driver, 120).until(
            EC.visibility_of_element_located((By.XPATH, "//th[contains(text(), 'Empresa Operadora')]"))
        )

        print(f"\n{C_GR}[+] ¡Resultados encontrados! Extrayendo datos...")
        soup = BeautifulSoup(driver.page_source, 'lxml')

        # Lógica de scraping para la estructura de la tabla.
        results_table = soup.find('div', class_='v-data-table__wrapper').find('table')
        company_counts = defaultdict(int)
        if results_table:
            rows = results_table.find('tbody').find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                # El nombre de la empresa está en la tercera columna.
                if len(cells) >= 3:
                    company_name = cells[2].text.strip()
                    if company_name:
                        company_counts[company_name] += 1

        print(f"\n {C_WH}========== {C_GR}LÍNEAS MÓVILES REGISTRADAS (Fuente: OSIPTEL){C_WH} ==========")
        if company_counts:
            total_lines = 0
            # Ordenar por nombre de compañía para una salida consistente.
            for company, count in sorted(company_counts.items()):
                print(f" {C_WH}{company:<30}:{C_GR} {count} línea(s)")
                total_lines += count
            print(f" {C_WH}{'-'*42}")
            print(f" {C_WH}{'TOTAL':<30}:{C_GR} {total_lines} línea(s)")
        else:
            print(f" {C_RE}No se encontraron líneas registradas para el DNI proporcionado.")

        print(f"\n{C_YE}[AVISO IMPORTANTE]{C_WH}")
        print(f"El servicio de OSIPTEL muestra los números de teléfono de forma CENSURADA por razones de privacidad y seguridad.")
        print(f"Este script muestra la cantidad de líneas por operador, que es la información pública disponible.")
        print(f"No es técnicamente posible 'descubrir' los números completos a través de esta consulta.")


    except TimeoutException:
        print(f"{C_RE}\nError: El tiempo de espera se agotó después de 2 minutos.")
        print(f"{C_YE}Posibles causas:")
        print(f"{C_YE}  - No se resolvió el CAPTCHA o no se hizo clic en 'Consultar' a tiempo.")
        print(f"{C_YE}  - El DNI consultado no arrojó resultados (no tiene líneas).")
        print(f"{C_YE}  - La estructura de la página de OSIPTEL ha cambiado.")
    except Exception as e:
        print(f"{C_RE}\nOcurrió un error inesperado durante la consulta con Selenium: {e}")
        if driver:
            # Guardar el HTML de la página para depuración
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html', encoding='utf-8') as f:
                f.write(driver.page_source)
                print(f"{C_YE}[!] Se ha guardado el estado actual de la página para depuración en: {f.name}")

    finally:
        if driver:
            driver.quit()
            print(f"\n{C_WH}[*] Navegador cerrado.")

@is_option
def escaner_puertos():
    """
    Escanea los puertos más comunes de una dirección IP o dominio.
    """
    target = input(f"\n {C_WH}Ingrese la IP o dominio a escanear: {C_GR}").strip()
    try:
        target_ip = socket.gethostbyname(target)
        print(f"\n{C_WH}[*] Escaneando {C_GR}{target}{C_WH} ({C_GR}{target_ip}{C_WH})...")
    except socket.gaierror:
        print(f"{C_RE}\nError: No se pudo resolver el nombre de host. Verifique el dominio o la IP.")
        return

    # Selección de tipo de escaneo.
    print(f"\n{C_WH}Seleccione el tipo de escaneo:")
    print(f" {C_GR}[1]{C_WH} Escaneo Rápido (Top 25 puertos)")
    print(f" {C_GR}[2]{C_WH} Escaneo Común (Top 1000 puertos de Nmap)")
    print(f" {C_GR}[3]{C_WH} Rango Personalizado (ej. 80-100)")
    choice = input(f"\n {C_WH}Opción: {C_GR}")

    ports_to_scan = []
    if choice == '1':
        # Puertos más comunes para un escaneo rápido.
        ports_to_scan = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080, 8443]
    elif choice == '2':
        # Puertos más comunes según Nmap (lista abreviada).
        ports_to_scan = [7,9,13,21,22,23,25,26,37,53,79,80,81,88,106,110,111,113,119,135,139,143,144,179,199,389,427,443,444,445,465,513,514,515,543,544,548,554,587,631,646,873,990,993,995,1025,1026,1027,1028,1029,1110,1433,1720,1723,1755,1900,2000,2001,2049,2121,2717,3000,3128,3306,3389,3986,4899,5000,5009,5051,5060,5101,5190,5357,5432,5631,5666,5800,5900,6000,6001,6002,6003,6004,6005,6006,6007,6008,6009,6346,6646,7070,8000,8008,8009,8080,8081,8443,8888,9100,9999,10000,32768,49152,49153,49154,49155,49156,49157] # Lista abreviada
    elif choice == '3':
        range_str = input(f" {C_WH}Ingrese el rango (ej. 80-100): {C_GR}")
        try:
            start, end = map(int, range_str.split('-'))
            ports_to_scan = range(start, end + 1)
        except ValueError:
            print(f"{C_RE}Formato de rango inválido.")
            return
    else:
        print(f"{C_RE}Opción no válida.")
        return

    open_ports_info = []

    def scan_port_with_banner(port):
        """Escanea un puerto y trata de obtener el banner si está abierto."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5) # Timeout agresivo para escaneos rápidos.
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            banner = ""
            try:
                # Intentar recibir el banner del servicio.
                sock.settimeout(2) # Más tiempo para recibir el banner.
                banner_bytes = sock.recv(1024)
                banner = banner_bytes.decode('utf-8', errors='ignore').strip()
            except (socket.timeout, ConnectionResetError):
                banner = "N/A (Timeout/Reset)"
            except Exception:
                banner = "N/A (Error al leer)"
            finally:
                sock.close()
            return (port, banner)
        return None

    print(f"\n{C_WH}[*] Iniciando escaneo en {len(list(ports_to_scan))} puertos...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        future_to_port = {executor.submit(scan_port_with_banner, port): port for port in ports_to_scan}
        for future in concurrent.futures.as_completed(future_to_port):
            info = future.result()
            if info:
                open_ports_info.append(info)

    print(f"\n {C_WH}========== {C_GR}RESULTADOS DEL ESCANEO DE PUERTOS{C_WH} ==========")
    if open_ports_info:
        # Mapeo de puertos a servicios conocidos.
        known_services = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 80: "HTTP",
            110: "POP3", 143: "IMAP", 443: "HTTPS", 3306: "MySQL", 3389: "RDP",
            5432: "PostgreSQL", 5900: "VNC", 8080: "HTTP-Proxy", 8443: "HTTPS-Alt"
        }
        print(f"{C_GR}Puertos abiertos encontrados en {target_ip}:\n")
        # Encabezados de la tabla de resultados.
        print(f" {C_CY}{'PUERTO':<10} {'ESTADO':<10} {'SERVICIO':<15} {'BANNER'}{C_END}")
        print(f" {C_CY}{'------':<10} {'------':<10} {'--------':<15} {'------'}{C_END}")

        for port, banner in sorted(open_ports_info):
            service = known_services.get(port, "Desconocido")
            banner_display = f"({banner})" if banner else ""
            print(f" {C_WH}{port:<10} {C_GR}{'ABIERTO':<10} {C_WH}{service:<15} {C_YE}{banner_display}{C_END}")
    else:
        print(f"{C_YE}No se encontraron puertos abiertos en el rango seleccionado para {target_ip}.")

@is_option
def extraer_metadatos():
    """
    Extrae metadatos de cualquier archivo usando ExifTool.
    """
    if not _check_exiftool():
        return

    file_path = input(f"\n {C_WH}Ingrese la ruta del archivo a analizar: {C_GR}")

    if not os.path.exists(file_path):
        print(f"{C_RE}\nError: El archivo no se encuentra en la ruta especificada.")
        return
    
    try:
        print(f"\n{C_WH}[*] Ejecutando ExifTool sobre: {C_GR}{os.path.basename(file_path)}{C_WH}")
        process = subprocess.run(['exiftool', file_path], capture_output=True, text=True, check=True)
        
        output = process.stdout
        print(f"\n {C_WH}========== {C_GR}METADATOS (Fuente: ExifTool){C_WH} ==========")
        if not output.strip():
            print(f"{C_YE}No se encontraron metadatos en este archivo.")
            return

        for line in output.strip().split('\n'):
            parts = line.split(':', 1)
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()
                print(f" {C_WH}{key:<35}:{C_GR} {value}")

    except FileNotFoundError:
        # Este caso ya es manejado por _check_exiftool, pero es una buena práctica mantenerlo.
        print(f"{C_RE}Error: 'exiftool' no está instalado o no se encuentra en el PATH del sistema.")
    except subprocess.CalledProcessError as e:
        print(f"{C_RE}ExifTool devolvió un error: {e.stderr}")
    except Exception as e:
        print(f"{C_RE}Ocurrió un error inesperado: {e}")

@is_option
def modificar_metadatos():
    """
    Elimina todos los metadatos de un archivo usando ExifTool, creando una copia limpia.
    """
    if not _check_exiftool():
        return

    in_path = input(f"\n {C_WH}Ingrese la ruta del archivo a limpiar: {C_GR}")
    if not os.path.exists(in_path):
        print(f"{C_RE}\nError: El archivo de entrada no existe.")
        return

    out_path = input(f" {C_WH}Ingrese la ruta para guardar el archivo limpio (ej. /ruta/archivo_limpio.jpg): {C_GR}")
    if not out_path:
        print(f"{C_RE}\nError: Debe especificar una ruta de salida.")
        return
    
    try:
        print(f"\n{C_WH}[*] Limpiando metadatos de {C_GR}{os.path.basename(in_path)}{C_WH} con ExifTool...")
        # Comando para ExifTool:
        # -all=   : Elimina todos los metadatos.
        # -o ...  : Especifica el archivo de salida, preservando el original.
        process = subprocess.run(
            ['exiftool', '-all=', '-o', out_path, in_path],
            capture_output=True, text=True, check=True
        )
        print(f"{C_GR}{process.stdout.strip()}")
        print(f"\n{C_GR}[+] ¡Éxito! Se ha creado una copia limpia en '{out_path}'.")
        print(f"{C_YE}El archivo original '{in_path}' no ha sido modificado.")

    except FileNotFoundError:
        print(f"{C_RE}Error: 'exiftool' no está instalado o no se encuentra en el PATH del sistema.")
    except subprocess.CalledProcessError as e:
        print(f"{C_RE}ExifTool devolvió un error: {e.stderr}")
    except Exception as e:
        print(f"{C_RE}Ocurrió un error inesperado: {e}")

@is_option
def consulta_placa_sunarp():
    """
    Consulta información de una placa vehicular en SUNARP (Perú) usando Selenium.
    """
    placa = input(f"\n {C_WH}Ingrese el número de placa (ej. ABC-123): {C_GR}").upper()
    if not placa:
        print(f"{C_RE}\nError: Debe ingresar un número de placa.")
        return

    driver = None
    try:
        print(f"\n{C_WH}[*] Iniciando navegador para consulta vehicular en SUNARP...")
        service = ChromeService(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(service=service, options=options)

        driver.get("https://www.sunarp.gob.pe/ConsultaVehicular/")

        placa_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'txtPlaca')))
        placa_input.send_keys(placa)

        print(f"\n{C_YE}--> ACCIÓN REQUERIDA <_--")
        print(f"{C_WH}Por favor, resuelva el CAPTCHA en la ventana de Chrome y haga clic en 'Realizar Búsqueda'.")
        print(f"{C_WH}El script esperará hasta 2 minutos por los resultados...")

        WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Placa') and contains(@class, 'titulo')]")))

        print(f"\n{C_GR}[+] ¡Resultados encontrados! Extrayendo datos...")
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        data_divs = soup.find_all('div', class_='row')
        data = {}
        for div in data_divs:
            label_tag = div.find('div', class_='col-sm-3')
            value_tag = div.find('div', class_='col-sm-9')
            if label_tag and value_tag:
                key = label_tag.text.strip().replace(':', '')
                value = value_tag.text.strip()
                if key:
                    data[key] = value

        print(f"\n {C_WH}========== {C_GR}INFORMACIÓN VEHICULAR (Fuente: SUNARP){C_WH} ==========")
        if data:
            for key, value in data.items():
                print(f" {C_WH}{key:<20}:{C_GR} {value}")
        else:
            print(f"{C_RE}No se pudieron extraer los datos. La estructura de la página puede haber cambiado.")

    except TimeoutException:
        print(f"{C_RE}\nError: El tiempo de espera se agotó. Posibles causas:")
        print(f"{C_YE}  - No se resolvió el CAPTCHA o la placa no arrojó resultados.")
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

@is_option
def consulta_licencia_mtc():
    """
    Consulta información de una licencia de conducir en el MTC (Perú) usando Selenium.
    """
    dni = input(f"\n {C_WH}Ingrese el número de DNI (8 dígitos): {C_GR}")
    if not dni.isdigit() or len(dni) != 8:
        print(f"{C_RE}\nError: El DNI debe contener 8 dígitos numéricos.")
        return

    driver = None
    try:
        print(f"\n{C_WH}[*] Iniciando navegador para consulta de licencia en MTC...")
        service = ChromeService(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(service=service, options=options)

        driver.get("https://licencias.mtc.gob.pe/")

        # Manejo del modal de términos y condiciones.
        try:
            terminos_check = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'chkTerminos')))
            driver.execute_script("arguments[0].click();", terminos_check)
            cerrar_btn = driver.find_element(By.XPATH, "//button[text()='Cerrar']")
            driver.execute_script("arguments[0].click();", cerrar_btn)
            print(f"{C_GR}[+] Términos y condiciones aceptados.")
        except TimeoutException:
            print(f"{C_YE}[!] No se encontró el modal de términos (puede que ya no exista o la página cambió).")

        dni_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'txtNroDocumento')))
        dni_input.send_keys(dni)

        print(f"\n{C_YE}--> ACCIÓN REQUERIDA <_--")
        print(f"{C_WH}Por favor, resuelva el CAPTCHA en la ventana de Chrome y haga clic en 'Buscar'.")
        print(f"{C_WH}El script esperará hasta 2 minutos por los resultados...")

        WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.ID, 'divTabla')))

        print(f"\n{C_GR}[+] ¡Resultados encontrados! Extrayendo datos...")
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        data_table = soup.find('table', id='datatable')
        data = {}
        if data_table:
            rows = data_table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if len(cells) == 2:
                    key = cells[0].text.strip().replace(':', '')
                    value = cells[1].text.strip()
                    if key:
                        data[key] = value

        print(f"\n {C_WH}========== {C_GR}INFORMACIÓN DE LICENCIA (Fuente: MTC){C_WH} ==========")
        if data:
            for key, value in data.items():
                print(f" {C_WH}{key:<25}:{C_GR} {value}")
        else:
            print(f"{C_RE}No se pudieron extraer los datos. La estructura de la página puede haber cambiado.")

    except TimeoutException:
        print(f"{C_RE}\nError: El tiempo de espera se agotó. Posibles causas:")
        print(f"{C_YE}  - No se resolvió el CAPTCHA, el DNI no tiene licencia o no arrojó resultados.")
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

@is_option
def ocultar_mensaje():
    """
    Oculta un mensaje de texto en una imagen PNG usando esteganografía LSB.
    """
    in_path = input(f"\n {C_WH}Ingrese la ruta de la imagen de entrada (.png): {C_GR}")
    if not os.path.exists(in_path) or not in_path.lower().endswith('.png'):
        print(f"{C_RE}\nError: El archivo no existe o no es un archivo PNG.")
        return

    out_path = input(f" {C_WH}Ingrese la ruta para guardar la nueva imagen (ej. /ruta/imagen_secreta.png): {C_GR}")
    if not out_path.lower().endswith('.png'):
        print(f"{C_RE}\nError: La ruta de salida debe ser un archivo .png.")
        return

    secret_message = input(f" {C_WH}Ingrese el mensaje secreto a ocultar: {C_GR}")
    if not secret_message:
        print(f"{C_RE}\nError: El mensaje no puede estar vacío.")
        return

    try:
        print(f"\n{C_WH}[*] Ocultando mensaje en la imagen...")
        secret_image = lsb.hide(in_path, secret_message)
        secret_image.save(out_path)
        print(f"{C_GR}[+] ¡Mensaje ocultado con éxito!")
        print(f"{C_WH}La nueva imagen se ha guardado en: {C_GR}{out_path}")
    except Exception as e:
        print(f"{C_RE}\nOcurrió un error durante el proceso de ocultación: {e}")
        print(f"{C_YE}Esto puede ocurrir si el mensaje es demasiado grande para la imagen.")

@is_option
def revelar_mensaje():
    """
    Revela un mensaje oculto en una imagen PNG.
    """
    in_path = input(f"\n {C_WH}Ingrese la ruta de la imagen que contiene el mensaje (.png): {C_GR}")
    if not os.path.exists(in_path) or not in_path.lower().endswith('.png'):
        print(f"{C_RE}\nError: El archivo no existe o no es un archivo PNG.")
        return

    try:
        print(f"\n{C_WH}[*] Buscando mensaje oculto en la imagen...")
        clear_message = lsb.reveal(in_path)

        if clear_message:
            print(f"\n {C_WH}========== {C_GR}MENSAJE REVELADO{C_WH} ==========")
            print(f" {C_GR}{clear_message}")
        else:
            print(f"{C_YE}No se encontró ningún mensaje oculto en esta imagen.")

    except Exception as e:
        print(f"{C_RE}\nOcurrió un error al intentar revelar el mensaje: {e}")

def _check_exiftool():
    """Verifica si ExifTool está instalado y es ejecutable."""
    if shutil.which('exiftool') is None:
        print(f"\n{C_RE}[!] Error: La herramienta 'exiftool' no está instalada o no se encuentra en el PATH.")
        print(f"{C_YE}Por favor, instálala para usar las funciones de metadatos.")
        print(f"{C_WH}En Debian/Ubuntu: {C_GR}sudo apt-get install libimage-exiftool-perl")
        print(f"{C_WH}En otras plataformas, visita: {C_GR}https://exiftool.org/")
        return False
    return True

# Opciones del menú
options = [
    {
        'num': 1,
        'text': 'informacion ip',
        'func': informacion_ip
    },
    {
        'num': 2,
        'text': 'informacion celular',
        'func': informacion_celular

    },
    {
        'num': 3,
        'text': 'informacion por nombre',
        'func': informacion_por_nombre
    },
    {
        'num': 4,
        'text': 'showIP',
        'func': showIP
    },
    {
        'num': 5,
        'text': 'Consulta RUC (Perú)',
        'func': consulta_RUC
    },
    {
        'num': 6,
        'text': 'Consulta DNI (Perú)',
        'func': consulta_DNI
    },
    {
        'num': 7,
        'text': 'Consulta RUC Avanzada (Manual)',
        'func': consulta_RUC_selenium
    },
    {
        'num': 8,
        'text': 'Consulta Líneas Móviles (Perú)',
        'func': consulta_lineas_osiptel
    },
    {
        'num': 9,
        'text': 'Escáner de Puertos Básico',
        'func': escaner_puertos
    },
    {
        'num': 10,
        'text': 'Extraer Metadatos (con ExifTool)',
        'func': extraer_metadatos
    },
    {
        'num': 11,
        'text': 'Consulta Placa Vehicular (SUNARP)',
        'func': consulta_placa_sunarp
    },
    {
        'num': 12,
        'text': 'Consulta Licencia de Conducir (MTC)',
        'func': consulta_licencia_mtc
    },
    {
        'num': 13,
        'text': 'Limpiar Metadatos (con ExifTool)',
        'func': modificar_metadatos
    },
    {
        'num': 14,
        'text': 'Ocultar Mensaje en Imagen (Esteganografía)',
        'func': ocultar_mensaje
    },
    {
        'num': 15,
        'text': 'Revelar Mensaje de Imagen (Esteganografía)',
        'func': revelar_mensaje
    },
    {
        'num': 0,
        'text': 'Salir',
        'func': lambda: exit(f"{C_YE}¡Adiós!{C_END}")
    }
]


def clear():
    """
    Limpia la pantalla de la consola.
    """
    # para windows
    if os.name == 'nt':
        _ = os.system('cls')
    # para mac y linux
    else:
        _ = os.system('clear')


def call_option(opt):
    """
    Llama a la función correspondiente a la opción seleccionada.
    """
    for option in options:
        if option['num'] == opt:
            option['func']()
            return
    raise ValueError('Opción no encontrada')


def execute_option(opt):
    """
    Ejecuta la opción seleccionada y maneja posibles errores.
    """
    try:
        call_option(opt)
        if opt != 0: # No es necesario esperar si el usuario elige salir
            input(f'\n{C_WH}[ {C_GR}+ {C_WH}] {C_GR}Presione Enter para continuar...{C_END}')
    except ValueError:
        print(f'\n{C_WH}[ {C_RE}! {C_WH}] {C_RE}¡Opción no válida!{C_END}')
        time.sleep(2)


def option_text():
    """
    Genera el texto del menú de opciones.
    """
    text = ''
    for opt in options:
        text += f'{C_WH}[ {C_GR}{opt["num"]}{C_WH} ] {C_GR}{opt["text"]}\n'
    return text


def display_main_menu():
    """
    Muestra el menú principal.
    """
    # BANNER TOOLS
    clear()
    # Banner para "CyberSleuth" con colores
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


    stderr.writelines(f"\n\n\n{option_text()}")


def run_banner():
    """
    Muestra el banner de la herramienta.
    """
    clear()
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


def main():
    """
    Función principal del programa.
    """
    while True:
        display_main_menu()
        try:
            opt = int(input(f"{C_WH}\n [ + ] {C_GR}Seleccione una opción: {C_WH}"))
            execute_option(opt)
        except ValueError:
            print(f'\n{C_WH}[ {C_RE}! {C_WH}] {C_RE}Por favor, ingrese un número.{C_END}')
            time.sleep(2)
        except KeyboardInterrupt:
            print(f'\n\n{C_WH}[ {C_RE}! {C_WH}] {C_RE}Programa interrumpido por el usuario.{C_END}')
            exit()


if __name__ == '__main__':
    main()
