import requests
import json
from ...config import C_WH, C_GR, C_RE, C_YE, SUNAT_TOKEN, APISPERU_TOKEN, DNIRUC_TOKEN
from ...utils import is_option

@is_option
def consulta_DNI():
    """
    Consulta la información de un DNI (Documento Nacional de Identidad) en Perú.
    """
    dni = input(f"\n {C_WH}Ingrese el número de DNI (8 dígitos): {C_GR}")
    if not dni.isdigit() or len(dni) != 8:
        print(f"{C_RE}\nError: El DNI debe contener 8 dígitos numéricos.")
        return
    print(f"\n{C_WH}[*] Iniciando consulta multifuente para el DNI {C_GR}{dni}{C_WH}...")

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

    def _get_code(dni_str):
        suma = 5
        hash_multipliers = [3, 2, 7, 6, 5, 4, 3, 2]
        for i in range(8):
            suma += int(dni_str[i]) * hash_multipliers[i]
        resto = suma % 11
        digito = 11 - resto
        if digito == 11: return 0
        if digito == 10: return 1
        return digito

    full_data['digitoVerificacion'] = _get_code(dni)

    # Fuente 1
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

    # Fuente 2
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

    # Fuente 3
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

    # Fuente 4
    if full_data['nombres'] == 'N/A' or full_data['fechaNacimiento'] == 'N/A':
        print(f"{C_WH}[*] Consultando fuente 4 (facturacionsunat.com) como respaldo...")
        try:
            sunat_url = 'http://www.facturacionsunat.com/vfpsws/vfpsconsbsapi.php'
            params = {'dni': dni, 'token': SUNAT_TOKEN, 'format': 'json'}
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

    # Fuente 5
    if full_data['nombres'] == 'N/A' and APISPERU_TOKEN:
        print(f"{C_WH}[*] Consultando fuente 5 (dniruc.apisperu.com) como respaldo final...")
        try:
            apisperu_url = f"https://dniruc.apisperu.com/api/v1/dni/{dni}?token={APISPERU_TOKEN}"
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

    # Fuente 6
    if full_data['nombres'] == 'N/A' and DNIRUC_TOKEN:
        print(f"{C_WH}[*] Consultando fuente 6 (api.dniruc.com) como respaldo final...")
        try:
            dniruc_url = f"https://api.dniruc.com/api/v1/dni/{dni}?token={DNIRUC_TOKEN}"
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
