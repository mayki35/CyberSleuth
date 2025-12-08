import re
import dns.resolver
from ..config import C_WH, C_GR, C_RE, C_YE, C_END
from ..utils import is_option

@is_option
def verificar_email():
    """
    Realiza verificaciones sobre una dirección de correo electrónico.
    """
    email = input(f"\n {C_WH}Ingrese el email a verificar: {C_GR}").strip()
    if not email:
        return

    print(f"\n {C_WH}========== {C_GR}ANÁLISIS DE EMAIL{C_WH} ==========")

    # 1. Validación de Sintaxis
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(regex, email):
        print(f" {C_WH}Sintaxis           :{C_GR} Válida")
    else:
        print(f" {C_WH}Sintaxis           :{C_RE} Inválida")
        return

    domain = email.split('@')[1]

    # 2. Verificación de Registros MX
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        print(f" {C_WH}Registros MX       :{C_GR} Encontrados ({len(mx_records)})")
        for mx in mx_records:
            print(f"    {C_GR}-> {mx.exchange} (Prioridad: {mx.preference})")
    except dns.resolver.NXDOMAIN:
        print(f" {C_WH}Registros MX       :{C_RE} Dominio no existe")
        return
    except dns.resolver.NoAnswer:
        print(f" {C_WH}Registros MX       :{C_YE} No encontrados")
    except Exception as e:
        print(f" {C_WH}Registros MX       :{C_RE} Error ({e})")

    # 3. Detección de Correos Temporales (Lista básica)
    disposable_domains = [
        'tempmail.com', 'throwawaymail.com', 'mailinator.com', 'guerrillamail.com', 
        'yopmail.com', '10minutemail.com', 'sharklasers.com'
    ]
    
    if domain in disposable_domains:
        print(f" {C_WH}Tipo de Correo     :{C_RE} Temporal / Desechable (Detectado)")
    else:
        print(f" {C_WH}Tipo de Correo     :{C_GR} Probablemente legítimo (No en lista negra básica)")
