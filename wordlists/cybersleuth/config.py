import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base Directory (Project Root)
# cybersleuth/config.py -> cybersleuth/ -> project_root/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Colors
C_BL = '\033[30m'
C_RE = '\033[1;31m'
C_GR = '\033[1;32m'
C_YE = '\033[1;33m'
C_BLU = '\033[1;34m'
C_MAGE = '\033[1;35m'
C_CY = '\033[1;36m'
C_WH = '\033[1;37m'
C_END = '\033[0m'

# API Tokens
SUNAT_TOKEN = os.getenv('SUNAT_TOKEN', '87290E49D50B519') # Default from original code, should be changed
APISPERU_TOKEN = os.getenv('APISPERU_TOKEN')
DNIRUC_TOKEN = os.getenv('DNIRUC_TOKEN')
SHODAN_API_KEY = os.getenv('SHODAN_API_KEY')
ONYPHE_API_KEY = os.getenv('ONYPHE_API_KEY')
