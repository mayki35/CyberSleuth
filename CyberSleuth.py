#!/usr/bin/python
# << CODE BY HUNX04
# << MAU RECODE ??? IZIN DULU LAH,  MINIMAL TAG AKUN GITHUB MIMIN YANG MENGARAH KE AKUN INI, LEBIH GAMPANG SI PAKE FORK
# << KALAU DI ATAS TIDAK DI IKUTI MAKA AKAN MENDAPATKAN DOSA KARENA MIMIN GAK IKHLAS
# “Wahai orang-orang yang beriman! Janganlah kamu saling memakan harta sesamamu dengan jalan yang batil,” (QS. An Nisaa': 29). Rasulullah SAW juga melarang umatnya untuk mengambil hak orang lain tanpa izin.

# IMPORT MODULE

import json
import requests
import time
import concurrent.futures
import tempfile
import os
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from sys import stderr, exit
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

# Clase para gestionar los colores de la consola, haciendo el código más limpio.
class Colors:
    BL = '\033[30m'
    RE = '\033[1;31m'
    GR = '\033[1;32m'
    YE = '\033[1;33m'
    BLU = '\033[1;34m'
    MAGE = '\033[1;35m'
    CY = '\033[1;36m'
    WH = '\033[1;37m'

C = Colors # Alias corto para facilitar su uso

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
    ip = input(f"{C.WH}\n Ingrese la IP objetivo: {C.GR}")
    print()
    try:
        print(f' {C.WH}============= {C.GR}MOSTRAR INFORMACIÓN DE LA DIRECCIÓN IP {C.WH}=============')
        req_api = requests.get(f"http://ipwho.is/{ip}", timeout=10)
        req_api.raise_for_status()  # Lanza una excepción para códigos de estado HTTP erróneos (4xx o 5xx)
        ip_data = req_api.json()

        if not ip_data.get("success", True):
            print(f"{C.RE}Error de la API: {ip_data.get('message', 'Dirección IP inválida')}")
            return

        time.sleep(1)
        connection_data = ip_data.get("connection", {})
        timezone_data = ip_data.get("timezone", {})
        flag_data = ip_data.get("flag", {})

        print(f"{C.WH}\n IP objetivo       :{C.GR}", ip)
        print(f"{C.WH} Tipo de IP         :{C.GR}", ip_data.get("type", "N/A"))
        print(f"{C.WH} País             :{C.GR}", ip_data.get("country", "N/A"))
        print(f"{C.WH} Código de País    :{C.GR}", ip_data.get("country_code", "N/A"))
        print(f"{C.WH} Ciudad            :{C.GR}", ip_data.get("city", "N/A"))
        print(f"{C.WH} Región          :{C.GR}", ip_data.get("region", "N/A"))
        lat = ip_data.get('latitude')
        lon = ip_data.get('longitude')
        if lat and lon:
            print(f"{C.WH} Latitud         :{C.GR}", lat)
            print(f"{C.WH} Longitud        :{C.GR}", lon)
            print(f"{C.WH} Mapa            :{C.GR}", f"https://www.google.com/maps/@{lat},{lon},8z")
        print(f"{C.WH} Código Postal     :{C.GR}", ip_data.get("postal", "N/A"))
        print(f"{C.WH} Código de Llamada :{C.GR}", ip_data.get("calling_code", "N/A"))
        print(f"{C.WH} Capital           :{C.GR}", ip_data.get("capital", "N/A"))
        print(f"{C.WH} Bandera del País  :{C.GR}", flag_data.get("emoji", "N/A"))
        print(f"{C.WH} ASN             :{C.GR}", connection_data.get("asn", "N/A"))
        print(f"{C.WH} ORG             :{C.GR}", connection_data.get("org", "N/A"))
        print(f"{C.WH} ISP             :{C.GR}", connection_data.get("isp", "N/A"))
        print(f"{C.WH} UTC             :{C.GR}", timezone_data.get("utc", "N/A"))
        print(f"{C.WH} Hora Actual       :{C.GR}", timezone_data.get("current_time", "N/A"))
    except requests.exceptions.RequestException as e:
        print(f"{C.RE}\nError: No se pudo conectar a la API. Por favor, verifique su conexión a Internet.")
        print(f"{C.RE}Detalles: {e}")


@is_option
def informacion_celular ():
    """
    Obtiene información sobre un número de teléfono.
    """
    User_phone = input(
        f"\n {C.WH}Ingrese el número de teléfono objetivo {C.GR}Ej [+6281xxxxxxxxx] {C.WH}: {C.GR}")
    default_region = "ID"  # País por defecto: Indonesia

    try:
        parsed_number = phonenumbers.parse(User_phone, default_region)
        
        if not phonenumbers.is_valid_number(parsed_number):
            print(f"{C.RE}\nError: El número de teléfono proporcionado no es válido.")
            return

        region_code = phonenumbers.region_code_for_number(parsed_number)
        jenis_provider = carrier.name_for_number(parsed_number, "en")
        location = geocoder.description_for_number(parsed_number, "id")
        timezone1 = timezone.time_zones_for_number(parsed_number)
        timezoneF = ', '.join(timezone1)

        print(f"\n {C.WH}========== {C.GR}MOSTRAR INFORMACIÓN DEL NÚMERO DE TELÉFONO {C.WH}==========")
        print(f"\n {C.WH}Ubicación             :{C.GR} {location}")
        print(f" {C.WH}Código de Región          :{C.GR} {region_code}")
        print(f" {C.WH}Zona Horaria             :{C.GR} {timezoneF}")
        print(f" {C.WH}Operador             :{C.GR} {jenis_provider or 'N/A'}")
        print(f" {C.WH}Formato Internacional :{C.GR} {phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}")
        print(f" {C.WH}Formato E.164         :{C.GR} {phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)}")
        print(f" {C.WH}Código de País         :{C.GR} {parsed_number.country_code}")
        
        number_type = phonenumbers.number_type(parsed_number)
        if number_type == phonenumbers.PhoneNumberType.MOBILE:
            print(f" {C.WH}Tipo                 :{C.GR} Este es un número de móvil")
        elif number_type == phonenumbers.PhoneNumberType.FIXED_LINE:
            print(f" {C.WH}Tipo                 :{C.GR} Este es un número de línea fija")
        else:
            print(f" {C.WH}Tipo                 :{C.GR} Este es otro tipo de número")

    except phonenumbers.phonenumberutil.NumberParseException as e:
        print(f"{C.RE}\nError: Formato de número de teléfono inválido. Por favor, incluya el código de país (ej., +1, +62).")
        print(f"{C.RE}Detalles: {e}")


@is_option
def informacion_por_nombre():
    """
    Rastrea la presencia de un nombre de usuario en varias redes sociales.
    """
    username = input(f"\n {C.WH}Ingrese el nombre de usuario: {C.GR}")
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
    
    print(f"\n{C.WH}[*] Buscando el nombre de usuario '{C.GR}{username}{C.WH}' en {len(social_media)} sitios...")

    def check_username(site):
        url = site['url'].format(username)
        try:
            response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            if response.status_code == 200:
                return site['name'], url
            return site['name'], f"{C.YE}No Encontrado{C.WH}"
        except requests.exceptions.RequestException:
            return site['name'], f"{C.RE}Error (Fallo de Conexión){C.WH}"

    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        future_to_url = {executor.submit(check_username, site): site for site in social_media}
        for future in concurrent.futures.as_completed(future_to_url):
            name, url = future.result()
            results[name] = url

    print(f"\n {C.WH}========== {C.GR}MOSTRAR INFORMACIÓN DEL NOMBRE DE USUARIO {C.WH}==========")
    print()
    for site_info in social_media: # Itera sobre la lista original para mantener el orden
        site_name = site_info['name']
        url = results.get(site_name, f"{C.RE}Error Desconocido{C.WH}")
        status_color = C.GR if "http" in url else C.YE if "No Encontrado" in url else C.RE
        print(f" {C.WH}[ {C.GR}+ {C.WH}] {site_name:<15} : {status_color}{url}")


@is_option
def showIP():
    """
    Muestra la dirección IP actual del usuario.
    """
    try:
        response = requests.get('https://api.ipify.org/', timeout=10)
        response.raise_for_status()
        show_ip = response.text

        print(f"\n {C.WH}========== {C.GR}MOSTRAR INFORMACIÓN DE TU IP {C.WH}==========")
        print(f"\n {C.WH}[{C.GR} + {C.WH}] Tu Dirección IP : {C.GR}{show_ip}")
        print(f"\n {C.WH}==============================================")
    except requests.exceptions.RequestException as e:
        print(f"{C.RE}\nError: No se pudo obtener tu dirección IP. Por favor, verifica tu conexión a Internet.")


@is_option
def consulta_RUC():
    """
    Consulta la información de un RUC (Registro Único de Contribuyentes) en Perú.
    """
    ruc = input(f"\n {C.WH}Ingrese el número de RUC (11 dígitos): {C.GR}")
    if not ruc.isdigit() or len(ruc) != 11:
        print(f"{C.RE}\nError: El RUC debe contener 11 dígitos numéricos.")
        return

    print(f"\n{C.WH}[*] Consultando RUC {C.GR}{ruc}{C.WH} en la fuente oficial de SUNAT...")

    # Reverting to the stable third-party API to ensure functionality
    try:
        api_url = f"https://api.apis.net.pe/v1/ruc?numero={ruc}"
        response = requests.get(api_url, timeout=15)
        response.raise_for_status()
        data = response.json()

        # The API returns a key 'error' if something goes wrong
        if 'error' in data:
            print(f"{C.RE}\nError de la API: {data['error']}")
            return

        print(f"\n {C.WH}========== {C.GR}INFORMACIÓN DEL RUC (Fuente: api.apis.net.pe){C.WH} ==========")
        print(f" {C.WH}{'Razón Social':<22}:{C.GR} {data.get('nombre', 'N/A')}")
        print(f" {C.WH}{'Nombre Comercial':<22}:{C.GR} {data.get('nombreComercial', 'N/A') or 'No especificado'}")
        print(f" {C.WH}{'Estado':<22}:{C.GR} {data.get('condicion', 'N/A')}")
        print(f" {C.WH}{'Dirección':<22}:{C.GR} {data.get('direccion', 'N/A')}")
        print(f" {C.WH}{'Departamento':<22}:{C.GR} {data.get('departamento', 'N/A')}")
        print(f" {C.WH}{'Provincia':<22}:{C.GR} {data.get('provincia', 'N/A')}")
        print(f" {C.WH}{'Distrito':<22}:{C.GR} {data.get('distrito', 'N/A')}")

    except requests.exceptions.RequestException as e:
        print(f"{C.RE}\nError: No se pudo conectar con el servicio de consulta.")
        print(f"{C.RE}Detalles: {e}")
    except json.JSONDecodeError:
        print(f"{C.RE}\nError: La respuesta de la API no es válida. El RUC podría no existir.")


@is_option
def consulta_DNI():
    """
    Consulta la información de un DNI (Documento Nacional de Identidad) en Perú desde múltiples fuentes para mayor estabilidad y detalle.
    """
    dni = input(f"\n {C.WH}Ingrese el número de DNI (8 dígitos): {C.GR}")
    if not dni.isdigit() or len(dni) != 8:
        print(f"{C.RE}\nError: El DNI debe contener 8 dígitos numéricos.")
        return
    print(f"\n{C.WH}[*] Iniciando consulta multifuente para el DNI {C.GR}{dni}{C.WH}...")

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
    print(f"{C.WH}[*] Consultando fuente 1 (apis.net.pe)...")
    try:
        api_url = f"https://api.apis.net.pe/v1/dni?numero={dni}"
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if 'error' not in data and data.get('nombres'):
            full_data['nombres'] = data.get('nombres')
            full_data['apellidoPaterno'] = data.get('apellidoPaterno')
            full_data['apellidoMaterno'] = data.get('apellidoMaterno')
            print(f"{C.GR}[+] Datos básicos obtenidos de la fuente 1.")
        else:
            print(f"{C.YE}[-] La fuente 1 no devolvió datos válidos.")
    except (requests.exceptions.RequestException, json.JSONDecodeError):
        print(f"{C.RE}[!] Falló la consulta a la fuente 1.")

    # --- Fuente 2: Essalud (Para fecha de nacimiento y sexo) ---
    print(f"{C.WH}[*] Consultando fuente 2 (Essalud)...")
    try:
        essalud_url = 'https://ww1.essalud.gob.pe/sisep/postulante/postulante/postulante_obtenerDatosPostulante.htm'
        response = requests.get(essalud_url, params={'strDni': dni}, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get('DatosPerson'):
            person_data = data['DatosPerson'][0]
            full_data['fechaNacimiento'] = person_data.get('FechaNacimiento', 'N/A')
            full_data['sexo'] = 'MASCULINO' if person_data.get('Sexo') == '1' else 'FEMENINO' if person_data.get('Sexo') == '2' else 'N/A'
            print(f"{C.GR}[+] Datos demográficos obtenidos de la fuente 2.")
        else:
            print(f"{C.YE}[-] La fuente 2 no devolvió datos válidos.")
    except (requests.exceptions.RequestException, json.JSONDecodeError):
        print(f"{C.RE}[!] Falló la consulta a la fuente 2.")

    # --- Fuente 3: reniec.cloud (Fuente de respaldo para nombres) ---
    # Solo se consulta si la primera fuente falló en obtener los nombres.
    if full_data['nombres'] == 'N/A':
        print(f"{C.WH}[*] Consultando fuente 3 (reniec.cloud) como respaldo...")
        try:
            reniec_url = f"https://api.reniec.cloud/dni/{dni}"
            response = requests.get(reniec_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data.get('nombres'):
                full_data['nombres'] = data.get('nombres', 'N/A')
                full_data['apellidoPaterno'] = data.get('apellido_paterno', 'N/A')
                full_data['apellidoMaterno'] = data.get('apellido_materno', 'N/A')
                print(f"{C.GR}[+] Datos básicos obtenidos de la fuente 3.")
            else:
                print(f"{C.YE}[-] La fuente 3 no devolvió datos válidos.")
        except (requests.exceptions.RequestException, json.JSONDecodeError):
            print(f"{C.RE}[!] Falló la consulta a la fuente 3.")

    # --- Fuente 4: facturacionsunat.com (Fuente de respaldo para varios datos) ---
    # Se consulta si aún faltan datos clave.
    if full_data['nombres'] == 'N/A' or full_data['fechaNacimiento'] == 'N/A':
        print(f"{C.WH}[*] Consultando fuente 4 (facturacionsunat.com) como respaldo...")
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
                print(f"{C.GR}[+] Datos adicionales obtenidos de la fuente 4.")
            else:
                print(f"{C.YE}[-] La fuente 4 no devolvió datos válidos.")
        except (requests.exceptions.RequestException, json.JSONDecodeError):
            print(f"{C.RE}[!] Falló la consulta a la fuente 4.")

    # --- Fuente 5: dniruc.apisperu.com (Fuente de respaldo final) ---
    # Se consulta si aún faltan los nombres.
    if full_data['nombres'] == 'N/A':
        print(f"{C.WH}[*] Consultando fuente 5 (dniruc.apisperu.com) como respaldo final...")
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
                print(f"{C.GR}[+] Datos básicos obtenidos de la fuente 5.")
            else:
                print(f"{C.YE}[-] La fuente 5 no devolvió datos válidos.")
        except (requests.exceptions.RequestException, json.JSONDecodeError):
            print(f"{C.RE}[!] Falló la consulta a la fuente 5.")

    print(f"\n {C.WH}========== {C.GR}INFORMACIÓN CONSOLIDADA DEL DNI{C.WH} ==========")
    print(f" {C.WH}{'Nombres':<22}:{C.GR} {full_data.get('nombres', 'N/A')}")
    print(f" {C.WH}{'Apellido Paterno':<22}:{C.GR} {full_data.get('apellidoPaterno', 'N/A')}")
    print(f" {C.WH}{'Apellido Materno':<22}:{C.GR} {full_data.get('apellidoMaterno', 'N/A')}")
    print(f" {C.WH}{'Número de DNI':<22}:{C.GR} {full_data.get('dni', 'N/A')}")
    print(f" {C.WH}{'Dígito Verificación':<22}:{C.GR} {full_data.get('digitoVerificacion', 'N/A')}")
    print(f" {C.WH}{'Fecha de Nacimiento':<22}:{C.GR} {full_data.get('fechaNacimiento', 'N/A')}")
    print(f" {C.WH}{'Sexo':<22}:{C.GR} {full_data.get('sexo', 'N/A')}")
    print(f" {C.WH}{'Domicilio (SUNAT)':<22}:{C.GR} {full_data.get('domicilio', 'N/A')}")


@is_option
def consulta_RUC_selenium():
    """
    Consulta la información de un RUC utilizando Selenium para interactuar con la página de SUNAT.
    """
    ruc = input(f"\n {C.WH}Ingrese el número de RUC (11 dígitos): {C.GR}")
    if not ruc.isdigit() or len(ruc) != 11:
        print(f"{C.RE}\nError: El RUC debe contener 11 dígitos numéricos.")
        return

    driver = None
    try:
        print(f"\n{C.WH}[*] Iniciando navegador para consulta avanzada...")
        # Selenium Manager will automatically handle the chromedriver
        # This simpler configuration is more stable on Windows
        service = ChromeService()
        options = webdriver.ChromeOptions()
        # This option hides the "Chrome is being controlled by automated test software" bar
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        driver = webdriver.Chrome(service=service, options=options)

        url = "https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/frameCriterioBusqueda.jsp"
        driver.get(url)

        # Wait for the RUC input field and enter the number
        ruc_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'txtRuc'))
        )
        ruc_input.send_keys(ruc)

        # Click the search button
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'btnAceptar'))
        )
        search_button.click()

        print(f"\n{C.WH}[*] Buscando resultados... El sitio ya no requiere CAPTCHA.")

        # Wait for the results table to appear. We wait for the main container.
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'list-group'))
        )

        print(f"\n{C.GR}[+] ¡Resultados encontrados! Extrayendo datos...")
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        data = {}
        # The data is now in a list of divs, not a table. This logic is updated
        # to match the current structure of the SUNAT results page.
        results_container = soup.find('div', class_='list-group')
        if results_container:
            # Find all individual data items within the container
            items = results_container.find_all('div', class_='list-group-item')
            for item in items:
                key_tag = item.find('h4', class_='list-group-item-heading')
                value_tag = item.find('p', class_='list-group-item-text')

                if key_tag and value_tag:
                    # Clean up the text and store it
                    key = ' '.join(key_tag.text.split()).replace(':', '').strip()
                    value = ' '.join(value_tag.text.split()).strip()
                    if key:
                        data[key] = value

        print(f"\n {C.WH}========== {C.GR}INFORMACIÓN DEL RUC (Fuente: SUNAT - Avanzado){C.WH} ==========")
        if data:
            for key, value in data.items():
                print(f" {C.WH}{key:<25}:{C.GR} {value}")
        else:
            print(f" {C.RE}No se encontraron datos para mostrar. La estructura de la página puede haber cambiado.")

    except Exception as e:
        print(f"{C.RE}\nOcurrió un error durante la consulta con Selenium: {e}")
    finally:
        if driver:
            driver.quit()
            print(f"\n{C.WH}[*] Navegador cerrado.")

@is_option
def consulta_lineas_osiptel():
    """
    Consulta el número de líneas móviles registradas a nombre de un DNI en el servicio de OSIPTEL (Perú) utilizando Selenium.
    """
    from collections import defaultdict
    dni = input(f"\n {C.WH}Ingrese el número de DNI (8 dígitos): {C.GR}")
    if not dni.isdigit() or len(dni) != 8:
        print(f"{C.RE}\nError: El DNI debe contener 8 dígitos numéricos.")
        return

    driver = None
    try:
        print(f"\n{C.WH}[*] Iniciando navegador para consulta de líneas...")
        service = ChromeService()
        options = webdriver.ChromeOptions()
        # Applying your suggestions for a cleaner and more stable run:
        # 1. Suppress non-essential logging to reduce console noise.
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # 2. Disable extensions and the "controlled by automation" bar.
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(service=service, options=options)

        # The URL for the OSIPTEL service has been updated.
        url = "https://checatuslineas.osiptel.gob.pe/"
        driver.get(url)

        # Robustly handle the privacy policy modal, which is the primary source of failure.
        try:
            # 1. Wait for the dialog container to be visible. This is more stable.
            # Increased timeout to 30 seconds for slower connections.
            dialog = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div.v-dialog--active[role='dialog']"))
            )
            print(f"{C.WH}[*] Modal de política de privacidad detectado. Intentando aceptar...")

            # 2. Find the button within the dialog and click it using JavaScript for reliability.
            accept_button = dialog.find_element(By.XPATH, ".//button[contains(., 'ACEPTAR')]")
            driver.execute_script("arguments[0].click();", accept_button)

            # 3. Wait for the dialog to disappear to confirm the action was successful.
            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.v-dialog--active[role='dialog']"))
            )
            print(f"{C.GR}[+] Política de privacidad aceptada correctamente.")
        except TimeoutException:
            print(f"{C.YE}[!] No se detectó el modal de política de privacidad en 30 segundos (o ya fue aceptado), continuando...")

        # Select the document type (DNI).
        print(f"{C.WH}[*] Seleccionando el tipo de documento (DNI)...")
        # We wait for the dropdown to be present and use a more reliable JavaScript click.
        doc_type_dropdown = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'document-type'))
        )
        driver.execute_script("arguments[0].click();", doc_type_dropdown)
        time.sleep(0.5) # Brief pause for the dropdown options to render.

        dni_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'v-list-item-title') and text()='DNI']"))
        )
        dni_option.click()

        # Input DNI
        dni_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'document-number'))
        )
        dni_input.send_keys(dni)

        print(f"\n{C.YE}--> ACCIÓN REQUERIDA <--")
        print(f"{C.WH}Se ha abierto una ventana de Chrome.")
        print(f"{C.WH}Por favor, resuelva el CAPTCHA y haga clic en el botón 'Consultar'.")
        print(f"{C.WH}El script esperará hasta 2 minutos...")
        
        # Wait for the user to solve the CAPTCHA and for the results table to appear.
        # We now wait for the table header to be visible, which is a more reliable indicator that the results have loaded.
        WebDriverWait(driver, 120).until(
            EC.visibility_of_element_located((By.XPATH, "//th[contains(text(), 'Empresa Operadora')]"))
        )

        print(f"\n{C.GR}[+] ¡Resultados encontrados! Extrayendo datos...")
        soup = BeautifulSoup(driver.page_source, 'lxml')

        # Updated scraping logic to correctly identify the company and count lines.
        results_table = soup.find('div', class_='v-data-table__wrapper').find('table')
        company_counts = defaultdict(int)
        if results_table:
            rows = results_table.find('tbody').find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                # The company name is in the third column ("Empresa Operadora")
                if len(cells) >= 3:
                    company_name = cells[2].text.strip()
                    if company_name:
                        company_counts[company_name] += 1

        print(f"\n {C.WH}========== {C.GR}LÍNEAS MÓVILES REGISTRADAS (Fuente: OSIPTEL){C.WH} ==========")
        if company_counts:
            total_lines = 0
            # Sort by company name for consistent output
            for company, count in sorted(company_counts.items()):
                print(f" {C.WH}{company:<30}:{C.GR} {count} línea(s)")
                total_lines += count
            print(f" {C.WH}{'-'*35}")
            print(f" {C.WH}{'TOTAL':<30}:{C.GR} {total_lines} línea(s)")
        else:
            print(f" {C.RE}No se encontraron líneas registradas para el DNI proporcionado.")

        print(f"\n{C.YE}[AVISO IMPORTANTE]")
        print(f"{C.WH}El servicio de OSIPTEL muestra los números de teléfono de forma CENSURADA por razones de privacidad y seguridad.")
        print(f"{C.WH}Este script muestra la cantidad de líneas por operador, que es la información pública disponible.")
        print(f"{C.WH}No es técnicamente posible 'descubrir' los números completos a través de esta consulta.")


    except TimeoutException:
        print(f"{C.RE}\nError: El tiempo de espera se agotó después de 2 minutos.")
        print(f"{C.YE}Posibles causas:")
        print(f"{C.YE}  - No se resolvió el CAPTCHA o no se hizo clic en 'Consultar' a tiempo.")
        print(f"{C.YE}  - El DNI consultado no arrojó resultados (no tiene líneas).")
        print(f"{C.YE}  - La estructura de la página de OSIPTEL ha cambiado.")
    except Exception as e:
        print(f"{C.RE}\nOcurrió un error durante la consulta con Selenium: {e}")
        # As you suggested, save the page source for debugging on failure.
        if driver:
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html', encoding='utf-8') as f:
                f.write(driver.page_source)
                print(f"{C.YE}[!] Se ha guardado el estado actual de la página para depuración en: {f.name}")

    finally:
        if driver:
            driver.quit()
            print(f"\n{C.WH}[*] Navegador cerrado.")

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
        'num': 0,
        'text': 'Salir',
        'func': lambda: exit(f"{C.YE}¡Adiós!{C.WH}")
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
            input(f'\n{C.WH}[ {C.GR}+ {C.WH}] {C.GR}Presione Enter para continuar')
    except ValueError:
        print(f'\n{C.WH}[ {C.RE}! {C.WH}] {C.RE}¡Opción no válida!')
        time.sleep(2)


def option_text():
    """
    Genera el texto del menú de opciones.
    """
    text = ''
    for opt in options:
        text += f'{C.WH}[ {opt["num"]} ] {C.GR}{opt["text"]}\n'
    return text


def display_main_menu():
    """
    Muestra el menú principal.
    """
    # BANNER TOOLS
    clear()
    # Banner para "CyberSleuth"
    stderr.writelines(f"""{C.CY}

░█████╗░██╗░░░██╗██████╗░███████╗██████╗░    ░██████╗██╗░░░░░███████╗██╗░░░██╗████████╗██╗░░██╗
██╔══██╗╚██╗░██╔╝██╔══██╗██╔════╝██╔══██╗░░░░██╔════╝██║░░░░░██╔════╝██║░░░██║╚══██╔══╝██║░░██║
██║░░╚═╝░╚████╔╝░██████╦╝█████╗░░██████╔╝░░░░╚█████╗░██║░░░░░█████╗░░██║░░░██║░░░██║░░░███████║
██║░░██╗░░╚██╔╝░░██╔══██╗██╔══╝░░██╔══██╗░░░░░╚═══██╗██║░░░░░██╔══╝░░██║░░░██║░░░██║░░░██╔══██║
╚█████╔╝░░░██║░░░██████╦╝███████╗██║░░██║░░░░██████╔╝███████╗███████╗╚██████╔╝░░░██║░░░██║░░██║
░╚════╝░░░░╚═╝░░░╚═════╝░╚══════╝╚═╝░░╚═╝░░░░╚═════╝░╚══════╝╚══════╝░╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝
{C.WH}
              [ + ]  Una herramienta de investigación {C.GR}OSINT{C.WH}  [ + ]
    """)


    stderr.writelines(f"\n\n\n{option_text()}")


def run_banner():
    """
    Muestra el banner de la herramienta.
    """
    clear()
    time.sleep(1)
    stderr.writelines(f"""{C.WH}

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

{C.WH}| {C.GR}CyberSleuth- IP ADDRESS {C.WH}|
{C.WH}|  {C.GR}https://t.me/mayki36   {C.WH}|
""")
    time.sleep(0.5)


def main():
    """
    Función principal del programa.
    """
    while True:
        display_main_menu()
        try:
            opt = int(input(f"{C.WH}\n [ + ] {C.GR}Seleccione una opción: {C.WH}"))
            execute_option(opt)
        except ValueError:
            print(f'\n{C.WH}[ {C.RE}! {C.WH}] {C.RE}Por favor, ingrese un número.')
            time.sleep(2)
        except KeyboardInterrupt:
            print(f'\n\n{C.WH}[ {C.RE}! {C.WH}] {C.RE}Programa interrumpido por el usuario.')
            exit()


if __name__ == '__main__':
    main()
