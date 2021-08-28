import sys
import requests

response = requests.get('http://127.0.0.1/healthz')
if response.text == 'ok':
    sys.exit(0)
sys.exit(1)
