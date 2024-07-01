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




if __name__ == '__main__':
    main()