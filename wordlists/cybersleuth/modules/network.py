import socket
import requests
import time
import concurrent.futures
from ..config import C_WH, C_GR, C_RE, C_CY, C_YE, C_END
from ..utils import is_option

@is_option
def get_ip_info():
    """
    Rastrea la información de una dirección IP.
    """
    ip = input(f"{C_WH}\n Ingrese la IP objetivo: {C_GR}")
    print()
    try:
        print(f' {C_WH}============= {C_GR}MOSTRAR INFORMACIÓN DE LA DIRECCIÓN IP {C_WH}=============')
        req_api = requests.get(f"http://ipwho.is/{ip}", timeout=10)
        req_api.raise_for_status()
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
def get_my_ip():
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
def scan_ports():
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
        ports_to_scan = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080, 8443]
    elif choice == '2':
        ports_to_scan = [7,9,13,21,22,23,25,26,37,53,79,80,81,88,106,110,111,113,119,135,139,143,144,179,199,389,427,443,444,445,465,513,514,515,543,544,548,554,587,631,646,873,990,993,995,1025,1026,1027,1028,1029,1110,1433,1720,1723,1755,1900,2000,2001,2049,2121,2717,3000,3128,3306,3389,3986,4899,5000,5009,5051,5060,5101,5190,5357,5432,5631,5666,5800,5900,6000,6001,6002,6003,6004,6005,6006,6007,6008,6009,6346,6646,7070,8000,8008,8009,8080,8081,8443,8888,9100,9999,10000,32768,49152,49153,49154,49155,49156,49157]
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
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            banner = ""
            try:
                sock.settimeout(2)
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
        known_services = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 80: "HTTP",
            110: "POP3", 143: "IMAP", 443: "HTTPS", 3306: "MySQL", 3389: "RDP",
            5432: "PostgreSQL", 5900: "VNC", 8080: "HTTP-Proxy", 8443: "HTTPS-Alt"
        }
        print(f"{C_GR}Puertos abiertos encontrados en {target_ip}:\n")
        print(f" {C_CY}{'PUERTO':<10} {'ESTADO':<10} {'SERVICIO':<15} {'BANNER'}{C_END}")
        print(f" {C_CY}{'------':<10} {'------':<10} {'--------':<15} {'------'}{C_END}")

        for port, banner in sorted(open_ports_info):
            service = known_services.get(port, "Desconocido")
            banner_display = f"({banner})" if banner else ""
            print(f" {C_WH}{port:<10} {C_GR}{'ABIERTO':<10} {C_WH}{service:<15} {C_YE}{banner_display}{C_END}")
    else:
        print(f"{C_YE}No se encontraron puertos abiertos en el rango seleccionado para {target_ip}.")

@is_option
def lookup_mac():
    """
    Busca el fabricante de una dirección MAC.
    """
    mac = input(f"\n {C_WH}Ingrese la dirección MAC (ej. 00:11:22:33:44:55): {C_GR}").strip()
    if not mac:
        return

    print(f"\n{C_WH}[*] Consultando fabricante para {C_GR}{mac}{C_WH}...")
    try:
        url = f"https://api.macvendors.com/{mac}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print(f"\n {C_WH}========== {C_GR}INFORMACIÓN MAC{C_WH} ==========")
            print(f" {C_WH}MAC Address        :{C_GR} {mac}")
            print(f" {C_WH}Fabricante         :{C_GR} {response.text}")
        else:
            print(f"{C_YE}No se encontró información para esta MAC (o límite de API excedido).")
    except requests.exceptions.RequestException as e:
        print(f"{C_RE}\nError de conexión: {e}")

@is_option
def reverse_dns():
    """
    Realiza una búsqueda inversa de DNS (IP a Hostname).
    """
    ip = input(f"\n {C_WH}Ingrese la dirección IP: {C_GR}").strip()
    if not ip:
        return

    print(f"\n{C_WH}[*] Resolviendo nombre de host para {C_GR}{ip}{C_WH}...")
    try:
        hostname, alias, addresslist = socket.gethostbyaddr(ip)
        print(f"\n {C_WH}========== {C_GR}REVERSE DNS{C_WH} ==========")
        print(f" {C_WH}IP                 :{C_GR} {ip}")
        print(f" {C_WH}Hostname           :{C_GR} {hostname}")
    except socket.herror:
        print(f"{C_YE}No se pudo resolver el nombre de host para esta IP.")
    except Exception as e:
        print(f"{C_RE}Error: {e}")
