import time
from sys import exit
from .config import C_WH, C_GR, C_RE, C_YE, C_END
from .utils import print_banner, clear_screen
from .modules.network import get_ip_info, get_my_ip, scan_ports, lookup_mac, reverse_dns
from .modules.social import informacion_celular, informacion_por_nombre
from .modules.osint_peru import (
    consulta_RUC, consulta_DNI, consulta_RUC_selenium, 
    consulta_lineas_osiptel, consulta_placa_sunarp, consulta_licencia_mtc,
    consulta_sunedu, consulta_papeletas_sat
)
from .modules.metadata import (
    extraer_metadatos, modificar_metadatos, 
    ocultar_mensaje, revelar_mensaje
)
from .modules.dns_tools import consulta_whois, enumeracion_dns, busqueda_subdominios
from .modules.web_analysis import analizar_cabeceras, obtener_robots
from .modules.cert_transparency import buscar_crtsh
from .modules.wayback import consultar_wayback
from .modules.email_tools import verificar_email
from .modules.shodan_tools import buscar_shodan, info_host_shodan
from .modules.breach_check import verificar_brecha_email, verificar_password_pwned
from .modules.wordlist_manager import descargar_diccionarios

def en_desarrollo():
    print(f"\n{C_WH}[ {C_YE}! {C_WH}] {C_YE}Esta opción está actualmente en desarrollo.{C_END}")
    time.sleep(1.5)

options = [
    {'num': 1, 'text': 'Informacion IP', 'func': get_ip_info},
    {'num': 2, 'text': 'Informacion Celular (En desarrollo)', 'func': en_desarrollo},
    {'num': 3, 'text': 'Informacion por Nombre de Usuario', 'func': informacion_por_nombre},
    {'num': 4, 'text': 'Mostrar mi IP', 'func': get_my_ip},
    {'num': 5, 'text': 'Consulta RUC (Perú)', 'func': consulta_RUC},
    {'num': 6, 'text': 'Consulta DNI (Perú)', 'func': consulta_DNI},
    {'num': 7, 'text': 'Consulta RUC Avanzada (Manual)', 'func': consulta_RUC_selenium},
    {'num': 8, 'text': 'Consulta Líneas Móviles (En desarrollo)', 'func': en_desarrollo},
    {'num': 9, 'text': 'Escáner de Puertos Básico', 'func': scan_ports},
    {'num': 10, 'text': 'Extraer Metadatos (con ExifTool)', 'func': extraer_metadatos},
    {'num': 11, 'text': 'Consulta Placa Vehicular (En desarrollo)', 'func': en_desarrollo},
    {'num': 12, 'text': 'Consulta Licencia de Conducir (En desarrollo)', 'func': en_desarrollo},
    {'num': 13, 'text': 'Consulta Grados y Títulos (SUNEDU)', 'func': consulta_sunedu},
    {'num': 14, 'text': 'Consulta Papeletas SAT (Lima)', 'func': consulta_papeletas_sat},
    {'num': 15, 'text': 'Limpiar Metadatos (con ExifTool)', 'func': modificar_metadatos},
    {'num': 16, 'text': 'Ocultar Mensaje en Imagen (Esteganografía)', 'func': ocultar_mensaje},
    {'num': 17, 'text': 'Revelar Mensaje de Imagen (Esteganografía)', 'func': revelar_mensaje},
    {'num': 18, 'text': 'Consulta Whois (Dominio)', 'func': consulta_whois},
    {'num': 19, 'text': 'Enumeración DNS (A, MX, NS, etc.)', 'func': enumeracion_dns},
    {'num': 20, 'text': 'Búsqueda de Subdominios (Básica)', 'func': busqueda_subdominios},
    {'num': 21, 'text': 'Analizar Cabeceras HTTP (Seguridad)', 'func': analizar_cabeceras},
    {'num': 22, 'text': 'Obtener Robots.txt', 'func': obtener_robots},
    {'num': 23, 'text': 'Búsqueda de Subdominios (Certificados SSL/crt.sh)', 'func': buscar_crtsh},
    {'num': 24, 'text': 'Wayback Machine (URLs Archivadas)', 'func': consultar_wayback},
    {'num': 25, 'text': 'Verificación y Análisis de Email', 'func': verificar_email},
    {'num': 26, 'text': 'Lookup de Fabricante MAC', 'func': lookup_mac},
    {'num': 27, 'text': 'Reverse DNS (IP a Hostname)', 'func': reverse_dns},
    {'num': 28, 'text': 'Búsqueda en Shodan (Dispositivos/Cámaras)', 'func': buscar_shodan},
    {'num': 29, 'text': 'Info de Host Shodan (IP)', 'func': info_host_shodan},
    {'num': 30, 'text': 'Verificar Email en Brechas (HIBP)', 'func': verificar_brecha_email},
    {'num': 31, 'text': 'Verificar Password Pwned (Seguro)', 'func': verificar_password_pwned},
    {'num': 32, 'text': 'Descargar Diccionarios (SecLists)', 'func': descargar_diccionarios},
    {'num': 0, 'text': 'Salir', 'func': lambda: exit(f"{C_YE}¡Adiós!{C_END}")}
]

def option_text():
    # Dividir las opciones en dos columnas
    mid = (len(options) + 1) // 2
    col1 = options[:mid]
    col2 = options[mid:]

    # Construir strings de la columna izquierda para medir ancho máximo
    left_strings = [f"{C_WH}[ {C_GR}{opt['num']:^2}{C_WH} ] {C_GR}{opt['text']}" for opt in col1]
    max_left = max(len(s) for s in left_strings)
    padding = 4  # espacios entre columnas

    output = ""
    for i in range(len(col1)):
        left = left_strings[i]
        right = ""
        if i < len(col2):
            right = f"{C_WH}[ {C_GR}{col2[i]['num']:^2}{C_WH} ] {C_GR}{col2[i]['text']}"
        output += f"{left.ljust(max_left + padding)}{right}\n"
    return output

def display_main_menu():
    print_banner()
    print(f"\n\n{option_text()}")

def execute_option(opt):
    try:
        for option in options:
            if option['num'] == opt:
                option['func']()
                if opt != 0:
                    input(f'\n{C_WH}[ {C_GR}+ {C_WH}] {C_GR}Presione Enter para continuar...{C_END}')
                return
        raise ValueError('Opción no encontrada')
    except ValueError:
        print(f'\n{C_WH}[ {C_RE}! {C_WH}] {C_RE}¡Opción no válida!{C_END}')
        time.sleep(2)

def main():
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
