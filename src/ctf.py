import nmap
import ipaddress
from src.modules import ssh,https,http,ftp,smtp

port_min = 0
port_max = 65535

def ctf(ip):
    # port scanning
    while True:
        # If we enter an invalid ip address the try except block will go to the except block and say you entered an invalid ip address.
        try:
            ip_address_obj = ipaddress.ip_address(ip)
            # The following line will only execute if the ip is valid.
            print(f'full scanning for this machine {ip} ...')
            break
        except:
            print("You entered an invalid ip address")
            ip = input('enter your IP address: ')
    nm = nmap.PortScanner()
    for port in range(port_min, port_max):
        try:
            # The result is quite interesting to look at. You may want to inspect the dictionary it returns. 
            # It contains what was sent to the command line in addition to the port status we're after. 
            # For in nmap for port 80 and ip 10.0.0.2 you'd run: nmap -oX - -p 89 -sV 10.0.0.2
            result = nm.scan(ip, str(port))
            # print(result)
            # We extract the port status from the returned object
            port_status = (result['scan'][ip]['tcp'][port]['state'])
            print(f"Port {port} is {port_status}")
            if port == '80' and port_status == 'open':
                print('it\' website have HTTP connection')
                print('trying to exploit it...')
                http(ip)
            if port == '443' and port_status == 'open':
                print('it\'s website have HTTPS connection')
                print('trying to exploit it...')
                https(ip)
            if port == '22' and port_status == 'open':
                print('we got SSH connection')
                print('trying to exploit it...')
                ssh(ip,port)
            if port == '2222' and port_status == 'open':
                print('we got SSH connection')
                print('trying to exploit it...')
                ssh(ip,port)
            if port == '21' and port_status == 'open':
                print('we got FTP connection')
                print('trying to exploit it...')
                ftp(ip)
            if port == '25' or port == '2525' or port == '465' or port == '587' and port_status == 'open':
                print('we got SMTP connection')
                print('trying to exploit it...')
                smtp(ip)
        except:
            # We cannot scan some ports and this ensures the program doesn't crash when we try to scan them.
            print(f"Cannot scan port {port}.")