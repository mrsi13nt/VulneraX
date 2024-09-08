import nmap
import ipaddress
from src.modules.others import *
from src.modules.http import *
from src.modules.https import *
from src.modules.smtp import *
from src.modules.ssh import *
from src.modules.ftp import *
import threading

port_min = 0
port_max = 65535

def ctf_other(ip):
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
    services = []
    def scan_port():
        for port in range(port_min, port_max):
            try:
                # The result is quite interesting to look at. You may want to inspect the dictionary it returns. 
                # It contains what was sent to the command line in addition to the port status we're after. 
                # For in nmap for port 80 and ip 10.0.0.2 you'd run: nmap -oX - -p 89 -sV 10.0.0.2
                result = nm.scan(ip, str(port), "-sV")
                # print(result)
                # We extract the port status from the returned object
                port_status = (result['scan'][ip]['tcp'][port]['state'])
                service_version = (result['scan'][ip]['tcp'][port].get('version', 'Unknown'))
                service_product = (result['scan'][ip]['tcp'][port].get('product', 'Unknown'))
                service_name = result['scan'][ip]['tcp'][port].get('name', 'Unknown')
                print(f"Port {port} is {port_status}")
                if port == '80' and port_status == 'open':
                    print('[\033[32m+\033[0m] it\' website have HTTP connection')
                    print('trying to exploit it...')
                    http(ip,service_product,service_version)
                if port == '443' and port_status == 'open':
                    print('[\033[32m+\033[0m] it\'s website have HTTPS connection')
                    print('trying to exploit it...')
                    https(ip,service_product,service_version)
                if port == '22' and port_status == 'open':
                    print('[\033[32m+\033[0m] we got SSH connection')
                    print('trying to exploit it...')
                    ssh(ip,port)
                if port == '2222' and port_status == 'open':
                    print('[\033[32m+\033[0m] we got SSH connection')
                    print('trying to exploit it...')
                    ssh(ip,port)
                if port == '21' and port_status == 'open':
                    print('[\033[32m+\033[0m] we got FTP connection')
                    print('trying to exploit it...')
                    ftp(ip)
                if port_status == 'open' and port != ['21','2222','22','443','80']:
                    print(f"Port {port} is {port_status}. Detected service: {service_name}, Product: {service_product}, Version: {service_version}")
                    services.append({
                        'port': port,
                        'name': service_name,
                        'product': service_product,
                        'version': service_version
                    })
            except Exception as e:
                print(f"[\033[31m!\033[0m] Error scanning port {port}: {e}")
    threads = []
    for port in range(port_min, port_max):
        t = threading.Thread(target=scan_port, args=(port,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
        
    return services
    # Main function to perform the entire process
def ctf(ip):
    # Step 1: Scan the target IP for services
    services = ctf_other(ip)

    # Step 2: Search for CVEs and Exploits for each service
    for service in services:
        service_name = service.get('name')
        service_product = service.get('product')
        service_version = service.get('version')
        port = service.get('port')

        if service_product and service_version:
            print(f"[*] Searching for {service_name} ({service_product} {service_version}) on port {port}...")

            # Search for CVEs
            cves = search_cve(service_product, service_version)
            if cves:
                print(f"[\033[32m+\033[0m] Found CVEs for {service_product} {service_version}:")
                for cve in cves:
                    print(f"    {cve['cve_id']}: {cve['description']}")
            else:
                print(f"[\033[31m-\033[0m] No CVEs found for {service_product} {service_version}")

            # Search for Exploits
            exploits = search_exploit(service_product, service_version)
            if exploits:
                print(f"[\033[32m+\033[0m] Found Exploits for {service_product} {service_version}:")
                for exploit in exploits:
                    print(f"    {exploit}")
                    # Optionally try to exploit
                    run_exploit(exploit, service_name, service_version, ip, port)
            else:
                print(f"[\033[31m-\033[0m] No exploits found for {service_product} {service_version}")
        else:
            print(f"[\033[31m-\033[0m] No version information for {service_name} on port {port}")