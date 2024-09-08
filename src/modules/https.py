import requests
import os
import ssl
from urllib.request import socket
import smtplib
from email.mime.text import MIMEText
from socket import gaierror
from urllib.parse import urlparse



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


def check_https_vulnerability(ip, port, service_name, service_version):
    try:
        # Check HTTP/HTTPS connection
        url = f"http://{ip}:{port}" if port != 443 else f"https://{ip}:{port}"
        response = requests.get(url, timeout=10)
        print(f"HTTP/HTTPS Response Status Code: {response.status_code}")

        # Check for potential vulnerabilities
        check_vulnerability(response)

        # Check for known vulnerabilities using NVD and CVE
        print("Checking known vulnerabilities...")
        check_known_vulnerabilities(service_name, service_version)

    except requests.RequestException as e:
        print(f"Failed to connect to HTTP/HTTPS server: {e}")

def check_vulnerability(response):
    # Check for common HTTP/HTTPS vulnerabilities
    # Example: Check if the server is leaking sensitive information in headers
    headers = response.headers
    print("HTTP/HTTPS Headers:")
    for header, value in headers.items():
        print(f"{header}: {value}")

    if 'Server' in headers:
        server_info = headers['Server']
        print(f"Server Info: {server_info}")
        # Example vulnerability check based on server info
        if "Apache" in server_info:
            print("This server might be running an outdated version of Apache. Check for known vulnerabilities.")

def check_known_vulnerabilities(service_name, service_version):
    # Define API endpoints for NVD and CVE
    nvd_api_url = "https://services.nvd.nist.gov/rest/json/cves/1.0"
    cve_api_url = "https://cve.circl.lu/api/cve"

    # Example NVD query
    try:
        response = requests.get(f"{nvd_api_url}?keyword={service_name}+{service_version}")
        if response.status_code == 200:
            data = response.json()
            for item in data.get("result", {}).get("CVE_Items", []):
                cve_id = item.get("cve", {}).get("CVE_data_meta", {}).get("ID", "N/A")
                description = item.get("cve", {}).get("description", {}).get("description_data", [{}])[0].get("value", "No description")
                print(f"NVD CVE ID: {cve_id}")
                print(f"Description: {description}")
        else:
            print("Failed to retrieve data from NVD.")
    
    except requests.RequestException as e:
        print(f"Error querying NVD: {e}")

    # Example CVE query
    try:
        response = requests.get(f"{cve_api_url}/{service_name}/{service_version}")
        if response.status_code == 200:
            data = response.json()
            for item in data:
                cve_id = item.get("id", "N/A")
                description = item.get("summary", "No description")
                print(f"CVE ID: {cve_id}")
                print(f"Description: {description}")
        else:
            print("Failed to retrieve data from CVE.")
    
    except requests.RequestException as e:
        print(f"Error querying CVE: {e}")




def https(target,port,p,v):
    https_info(target)
    check_https_vulnerability(target,port,p,v)