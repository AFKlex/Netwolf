import requests 
import socket

def hostname_resolves(domain):
    try:
        ip = socket.gethostbyname(domain)
        return 1
    except: 
        return 0

domain = "shit.kaufbeuren.de"

if hostname_resolves(domain):
    r = requests.get(f"https://{domain}") 
    print(r.status_code)

