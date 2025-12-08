import whois
import dns.resolver
from ..config import C_WH, C_GR, C_RE, C_YE, C_CY, C_END
from ..utils import is_option

@is_option
def consulta_whois():
    """
    Obtiene información de registro de un dominio (Whois).
    """
    domain = input(f"\n {C_WH}Ingrese el dominio a consultar (ej. google.com): {C_GR}").strip()
    if not domain:
        print(f"{C_RE}\nError: El dominio no puede estar vacío.")
        return

    try:
        print(f"\n{C_WH}[*] Consultando Whois para {C_GR}{domain}{C_WH}...")
        w = whois.whois(domain)
        
        print(f"\n {C_WH}========== {C_GR}INFORMACIÓN WHOIS{C_WH} ==========")
        # Mostramos los campos más relevantes
        fields = [
            ('domain_name', 'Nombre de Dominio'),
            ('registrar', 'Registrador'),
            ('whois_server', 'Servidor Whois'),
            ('creation_date', 'Fecha de Creación'),
            ('expiration_date', 'Fecha de Expiración'),
            ('updated_date', 'Última Actualización'),
            ('name_servers', 'Servidores de Nombres'),
            ('emails', 'Correos de Contacto'),
            ('org', 'Organización'),
            ('country', 'País')
        ]

        for field, label in fields:
            value = w.get(field)
            if value:
                # Manejar listas (como name_servers o emails)
                if isinstance(value, list):
                    value = ', '.join([str(v) for v in value])
                print(f" {C_WH}{label:<25}:{C_GR} {value}")
        
    except Exception as e:
        print(f"{C_RE}\nError al consultar Whois: {e}")

@is_option
def enumeracion_dns():
    """
    Consulta registros DNS comunes (A, AAAA, MX, NS, TXT, SOA).
    """
    domain = input(f"\n {C_WH}Ingrese el dominio a analizar (ej. google.com): {C_GR}").strip()
    if not domain:
        print(f"{C_RE}\nError: El dominio no puede estar vacío.")
        return

    record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA']
    
    print(f"\n {C_WH}========== {C_GR}REGISTROS DNS para {domain}{C_WH} ==========")

    for record in record_types:
        try:
            answers = dns.resolver.resolve(domain, record)
            print(f"\n {C_CY}[ {record} ]{C_END}")
            for rdata in answers:
                print(f"  {C_GR}-> {rdata.to_text()}")
        except dns.resolver.NoAnswer:
            pass # No hay registros de este tipo
        except dns.resolver.NXDOMAIN:
            print(f"{C_RE}\nError: El dominio no existe.")
            return
        except Exception as e:
            print(f"  {C_YE}No se pudo obtener registros {record}: {e}")

@is_option
def busqueda_subdominios():
    """
    Busca subdominios comunes intentando resolverlos.
    """
    domain = input(f"\n {C_WH}Ingrese el dominio base (ej. google.com): {C_GR}").strip()
    if not domain:
        return

    # Lista pequeña de subdominios comunes para demostración
    subdomains = [
        'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'ns2', 
        'test', 'dev', 'admin', 'blog', 'api', 'vpn', 'secure', 'cloud', 'email'
    ]

    print(f"\n{C_WH}[*] Iniciando búsqueda rápida de subdominios para {C_GR}{domain}{C_WH}...")
    
    found = []
    for sub in subdomains:
        hostname = f"{sub}.{domain}"
        try:
            answers = dns.resolver.resolve(hostname, 'A')
            for rdata in answers:
                print(f" {C_GR}[+] Encontrado: {C_WH}{hostname:<30} -> {C_GR}{rdata.to_text()}")
                found.append((hostname, rdata.to_text()))
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.Timeout):
            pass
        except Exception:
            pass

    if not found:
        print(f"\n{C_YE}No se encontraron subdominios comunes en esta búsqueda rápida.")
