import requests
import concurrent.futures
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from ..config import C_WH, C_GR, C_RE, C_YE, C_END
from ..utils import is_option

@is_option
def informacion_celular():
    """
    Obtiene información sobre un número de teléfono.
    """
    User_phone = input(
        f"\n {C_WH}Ingrese el número de teléfono objetivo {C_GR}Ej [+51987654321] {C_WH}: {C_GR}")
    default_region = "PE"

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
    for site_info in social_media:
        site_name = site_info['name']
        url = results.get(site_name, f"{C_RE}Error Desconocido{C_WH}")
        status_color = C_GR if "http" in url else C_YE if "No Encontrado" in url else C_RE
        print(f" {C_WH}[ {C_GR}+ {C_WH}] {site_name:<15} : {status_color}{url}{C_END}")
