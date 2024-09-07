import os
import sys
import subprocess
import requests
import socket

def main():
     
    # check for network
    def check_network():
            try:
                # Try to resolve the hostname
                socket.gethostbyname("google.com")
                return True
            except socket.error:
                return False
    if not check_network():
        print("[\033[31mError\033[0m] No network connection. Please check your internet connection and try again.")
        sys.exit(1)
    print("Network connection is available. Continuing with the program...\n")

    subprocess.run('',shell=True) # requirments
    subprocess.run('mkdir /home/mrsi13nt/.VulneraX',shell=True)
    subprocess.run('mv src /home/mrsi13nt/.VulneraX/',shell=True)
    subprocess.run('sudo cp VulneraX.py /usr/bin/',shell=True)
    subprocess.run('mv VulneraX.py /home/mrsi13nt/.VulneraX/',shell=True)
    subprocess.run('rm -r *',shell=True)
    sys.exit(1)

if __name__ == '__main__':
    main()