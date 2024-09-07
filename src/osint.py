import whois
import requests
from src.configs import keys

def lookup_domain(domain):
    try:
        domain_info = whois.whois(domain)
        print(f"Domain: {domain}")
        print(f"Registrar: {domain_info.registrar}")
        print(f"Creation Date: {domain_info.creation_date}")
        print(f"Expiration Date: {domain_info.expiration_date}")
        print(f"Nameservers: {domain_info.name_servers}")
    except Exception as e:
        print(f"Error: {e}")

def social_media(username):
    print(f"Searching for social media accounts with username: {username}")
    # You can use APIs or scraping to search for social media accounts.
    # For example, search for usernames on platforms like Twitter, Facebook, Instagram, etc.

def search_email(email):
    # For this example, we will simply print the email.
    # 
    print(f"Searching for email: {email}")
    # hunter.io
    if keys.get('hunter') == '':
        print("[!] no hunter.io API key entered")
    else:
        response = requests.get(f"https://api.hunter.io/v2/email-finder?email={email}&api_key={keys.get('hunter')}")
        print(response.json())
    # shodan
    if keys.get('shodan') == '':
        print("[!] no shodan API key entered")
    else:
        # response = requests.get(f"https://api.hunter.io/v2/email-finder?email={email}&api_key={keys.get('hunter')}")
        print(response.json())
    # HaveIBeenPwnd
    if keys.get('pwnd') == '':
        print("[!] no HaveIBeenPwnd API key entered")
    else:
        # response = requests.get(f"https://api.hunter.io/v2/email-finder?email={email}&api_key={keys.get('hunter')}")
        print(response.json())

def lookup_ip(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        data = response.json()
        print(f"IP Address: {ip}")
        print(f"Location: {data.get('city')}, {data.get('region')}, {data.get('country')}")
        print(f"ISP: {data.get('org')}")
        print(f"Coordinates: {data.get('loc')}")
    except Exception as e:
        print(f"Error: {e}")