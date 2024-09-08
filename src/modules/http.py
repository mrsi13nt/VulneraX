import requests
import os


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


def http(target,p,v):
    http_info(target)
    print('coming soon...')