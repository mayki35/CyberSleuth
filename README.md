# CyberSleuth
es una completa herramienta OSINT (Open Source Intelligence) de línea de comandos, escrita en Python. Diseñada para ser versátil y potente, se especializa en la recopilación de información de fuentes abiertas, con un fuerte enfoque en servicios peruanos, además de incluir utilidades de análisis de red y metadatos de archivos.

<a href="https://github.com/mayki35"><img src="https://github.com/mayki35.png" width="300" height="300" alt="mayki36"/></a>

---

## Características Principales

CyberSleuth ofrece una amplia gama de módulos para la investigación:

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
- **Extraer Metadatos**: Analiza archivos (imágenes, PDF, audio, video) para extraer información oculta como geolocalización, software utilizado, fechas, etc.
- **Modificar Metadatos**: Limpia los metadatos de los archivos soportados para proteger tu privacidad, creando una copia limpia del archivo.

---

## Instalación

### En Linux
```
git clone https://github.com/mayki35/CyberSleuth.git
```
```
cd CyberSleuth
```
```
sudo su
```
```
python -m venv venv
```
```
source ./venv/bin/activate
```
```
pip install -r requirements.txt
```
```
python CyberSleuth.py
```
### Instalation en Windows
```
cd GhostTrack
```
```
python -m venv venv
```
```
.\venv\Scripts\activate
```
```
pip install -r requirements.txt
```
```
python CyberSleuth.py
```
