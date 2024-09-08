import requests
from src.configs import printt


def banner_grab_http(ip):
    # Grab the HTTP banner to check the version
    try:
        response = requests.get(f"http://{ip}")
        server = response.headers.get('Server')
        print(f"HTTP Server Banner: {server}")
        return server
    except Exception as e:
        print(f"Failed to grab HTTP banner: {e}")
        return None

def brute_force_directories(ip, wordlist_file):
    # Try to brute-force common directories
    print(f"Brute-forcing directories on http://{ip}...")
    with open(wordlist_file, 'r') as f:
        directories = [line.strip() for line in f]
    
    for directory in directories:
        url = f"http://{ip}/{directory}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"Found directory: {url}")
        except Exception as e:
            print(f"Error testing directory {directory}: {e}")

def brute_force_http_auth(ip, username_file, password_file):
    # Brute-force HTTP Basic Authentication
    print(f"Starting brute-force attack on HTTP basic auth at http://{ip}...")
    with open(username_file, 'r') as uf, open(password_file, 'r') as pf:
        usernames = [line.strip() for line in uf]
        passwords = [line.strip() for line in pf]

    for username in usernames:
        for password in passwords:
            try:
                print(f"Trying {username}:{password}...")
                response = requests.get(f"http://{ip}", auth=(username, password))
                if response.status_code == 200:
                    print(f"Login successful with {username}:{password}")
                    return True
            except Exception as e:
                print(f"Error occurred during brute-force attempt: {e}")
                return False
    print("Brute-force attack finished, no valid credentials found.")
    return False

def http_info(ip):
    # Gather IP and scan for HTTP vulnerabilities
    
    if True:
        # Grab the HTTP banner
        banner_grab_http(ip)
        
        # Directory brute-forcing
        wordlist_file = 'common_dirs.txt'
        brute_force_directories(ip, wordlist_file)
        
        # Brute force login attempt (if basic auth is enabled)
        username_file = 'usernames.txt'
        password_file = 'passwords.txt'
        brute_force_http_auth(ip, username_file, password_file)
    else:
        print("HTTP service not detected or port 80 is closed.")



def check_http_vulnerability(ip, port, service_name, service_version):
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



def http(target,port,p,v):
    http_info(target)
    check_http_vulnerability(target,port,p,v)