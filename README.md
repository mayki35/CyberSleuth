# CyberSleuth Improved

Una completa herramienta OSINT (Open Source Intelligence) de línea de comandos, escrita en Python. Diseñada para ser versátil y potente, se especializa en la recopilación de información de fuentes abiertas, con un fuerte enfoque en servicios peruanos, además de incluir utilidades de análisis de red y metadatos de archivos.

## Características Principales

### 🔎 Búsqueda de Información General
- **Información de IP**: Rastrea detalles geográficos y de red de una dirección IP.
- **Información de Celular**: Obtiene datos del operador y la región de un número de teléfono.
- **Búsqueda por Nombre de Usuario**: Verifica la existencia de un nombre de usuario en más de 20 redes sociales.
- **Mostrar mi IP**: Muestra tu dirección IP pública actual.
- **Escáner de Puertos**: Realiza un escaneo básico de puertos comunes en un host.

### 🇵🇪 Módulos Específicos para Perú
- **Consulta de DNI**: Agrega información de múltiples fuentes públicas para obtener datos de un DNI.
- **Consulta de RUC**: Obtiene información de empresas a partir de su número de RUC (vía API y Selenium).
- **Consulta de Líneas Móviles**: Verifica la cantidad de líneas móviles asociadas a un DNI (OSIPTEL).
- **Consulta de Placa Vehicular**: Obtiene datos de un vehículo a través de su placa (SUNARP).
- **Consulta de Licencia de Conducir**: Revisa el estado de una licencia de conducir a partir de un DNI (MTC).

### 📁 Utilidades de Metadatos
- **Extraer Metadatos**: Analiza archivos (imágenes, PDF, audio, video) para extraer información oculta como geolocalización, software utilizado, fechas, etc. (Requiere ExifTool).
- **Modificar Metadatos**: Limpia los metadatos de los archivos soportados para proteger tu privacidad.
- **Esteganografía**: Oculta y revela mensajes secretos en imágenes PNG.

## Instalación

### Requisitos Previos
- **Python 3.8+**: Asegúrate de tener Python instalado.
- **Google Chrome**: Necesario para las funciones que utilizan Selenium (como la consulta de RUC).
- **ExifTool**: Necesario para las funciones de metadatos.
  - **Debian/Ubuntu/Kali**: `sudo apt-get install libimage-exiftool-perl`
  - **Windows**: Descargar desde [exiftool.org](https://exiftool.org/) y agregar al PATH.

### Pasos de Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/mayki35/CyberSleuth.git
   cd CyberSleuth
   ```

2. **Crear un entorno virtual (Recomendado)**:
   Esto aísla las dependencias del proyecto.
   ```bash
   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate

   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**:
   - Copia el archivo de ejemplo:
     ```bash
     cp .env.example .env
     ```
   - Edita el archivo `.env` con un editor de texto (nano, vim, notepad) y agrega tus tokens de API si los tienes. Esto es opcional para muchas funciones, pero necesario para algunas APIs específicas.

## Uso

Para iniciar la herramienta, ejecuta el siguiente comando desde la raíz del proyecto (asegúrate de tener el entorno virtual activado):

```bash
python -m cybersleuth.main
```

### Navegación
La herramienta utiliza un menú interactivo. Usa las teclas de dirección (arriba/abajo) para seleccionar una opción y `Enter` para confirmar.

### Descarga de Diccionarios
La primera vez que uses funciones que requieran diccionarios (como fuerza bruta o búsqueda de directorios), la herramienta intentará descargarlos automáticamente en la carpeta `wordlists/`.

## Solución de Problemas

- **Error de Selenium / Chrome Driver**:
  Si obtienes errores relacionados con Chrome o ChromeDriver, asegúrate de tener Google Chrome instalado y actualizado. La herramienta usa `webdriver-manager` para descargar automáticamente el driver compatible, pero necesita que el navegador esté presente.

- **Error "Module not found"**:
  Asegúrate de estar ejecutando el comando `python -m cybersleuth.main` desde el directorio raíz del proyecto (`cyber_sleuth_improvement`) y no desde dentro de la carpeta `cybersleuth`.

- **Permisos de ExifTool**:
  Si las funciones de metadatos fallan, verifica que ExifTool esté instalado correctamente y accesible desde la terminal (`exiftool -ver`).

## Estructura del Proyecto
El proyecto ha sido refactorizado para ser modular:
- `cybersleuth/`: Paquete principal.
  - `modules/`: Módulos funcionales (red, social, osint_peru, metadatos).
  - `config.py`: Configuración y manejo de variables de entorno.
  - `utils.py`: Funciones de utilidad.
  - `main.py`: Punto de entrada y menú principal.

## Créditos
Creado por mayki35.
