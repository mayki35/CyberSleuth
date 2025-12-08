import os
import shutil
import subprocess
from stegano import lsb
from ..config import C_WH, C_GR, C_RE, C_YE
from ..utils import is_option

def _check_exiftool():
    """Verifica si ExifTool está instalado y es ejecutable."""
    if shutil.which('exiftool') is None:
        print(f"\n{C_RE}[!] Error: La herramienta 'exiftool' no está instalada o no se encuentra en el PATH.")
        print(f"{C_YE}Por favor, instálala para usar las funciones de metadatos.")
        print(f"{C_WH}En Debian/Ubuntu: {C_GR}sudo apt-get install libimage-exiftool-perl")
        print(f"{C_WH}En otras plataformas, visita: {C_GR}https://exiftool.org/")
        return False
    return True

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
