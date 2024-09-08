import nmap
import ipaddress
import re
import requests
from src.configs import ask
from src.configs import printt

# Regular Expression Pattern to extract the number of ports you want to scan. 
# You have to specify <lowest_port_number>-<highest_port_number> (ex 10-100)
port_range_pattern = re.compile("([0-9]+)-([0-9]+)")

port_min = 0
port_max = 65535

# port scanner
def scan(ip):
    while True:
        # If we enter an invalid ip address the try except block will go to the except block and say you entered an invalid ip address.
        try:
            ip_address_obj = ipaddress.ip_address(ip)
            # The following line will only execute if the ip is valid.
            print("You entered a valid ip address.")
            break
        except KeyboardInterrupt:
            ask()
        except:
            print("\033[31mYou entered an invalid ip address\033[0m")
            ip = input('enter your IP address: ')
    while True:
        try:
            # You can scan 0-65535 ports. This scanner is basic and doesn't use multithreading so scanning all the ports is not advised.
            print("Please enter the range of ports you want to scan in format: <int>-<int> (ex would be 60-120)")
            port_range = input("Enter port range: ")
            # We pass the port numbers in by removing extra spaces that people sometimes enter. So if you enter 80 - 90 instead of 80-90 the program will still work.
            port_range_valid = port_range_pattern.search(port_range.replace(" ",""))
            if port_range_valid:
                # We're extracting the low end of the port scanner range the user want to scan.
                port_min = int(port_range_valid.group(1))
                # We're extracting the upper end of the port scanner range the user want to scan.
                port_max = int(port_range_valid.group(2))
                break
        except KeyboardInterrupt:
            ask()

    nm = nmap.PortScanner()
    # We're looping over all of the ports in the specified range.
    for port in range(port_min, port_max + 1):
        try:
            # The result is quite interesting to look at. You may want to inspect the dictionary it returns. 
            # It contains what was sent to the command line in addition to the port status we're after. 
            # For in nmap for port 80 and ip 10.0.0.2 you'd run: nmap -oX - -p 89 -sV 10.0.0.2
            result = nm.scan(ip, str(port))
            # Uncomment following line and look at dictionary
            # print(result)
            # We extract the port status from the returned object
            port_status = (result['scan'][ip]['tcp'][port]['state'])
            print(f"Port {port} is {port_status}")
        except KeyboardInterrupt:
            ask()
        except:
            # We cannot scan some ports and this ensures the program doesn't crash when we try to scan them.
            print(f"Cannot scan port {port}.")


# web recon
def recon(web):
    # print('starting subdomain enum...')
    
    # print('strating filter subdomains')
    
    # print('subdomain enum finished\n results saved in subdomains.txt')
    # print('starting some fuzzing... (don\'t worry it\'s safe)')
    # print('[\033[31m!\033[0m] if you want custom threads you can change it from config file search about \'threads\'')
    # requests.get('#')
    # print('s')
    printt('coming soon...')