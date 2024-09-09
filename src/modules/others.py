import subprocess
import xml.etree.ElementTree as ET
import requests
import re
from src.configs import printt


# Function to query NVD API for CVEs
def search_cve(service, version):
    cve_list = []
    nvd_url = f"https://services.nvd.nist.gov/rest/json/cves/1.0?keyword={service}%20{version}"
    response = requests.get(nvd_url)
    
    if response.status_code == 200:
        data = response.json()
        for item in data['result']['CVE_Items']:
            cve_id = item['cve']['CVE_data_meta']['ID']
            description = item['cve']['description']['description_data'][0]['value']
            cve_list.append({'cve_id': cve_id, 'description': description})
    else:
        print(f"[\033[31m!\033[0m] Failed to retrieve CVEs for {service} {version}")
    
    return cve_list


# Function to search for exploits using Exploit-DB
def search_exploit(service, version):
    """Searches for exploits related to a service and version."""
    exploits = []
    exploit_db_url = f"https://www.exploit-db.com/search?q={service}+{version}"
    response = requests.get(exploit_db_url)

    if response.status_code == 200:
        results = re.findall(r'/exploits/\d+', response.text)
        for result in results:
            exploits.append(f"https://www.exploit-db.com{result}")
    else:
        print(f"[\033[31m!\033[0m] Failed to retrieve exploits for {service} {version}")

    return exploits


# Function to attempt to exploit the service
def run_exploit(exploit_url, service, version, target_ip, port):
    """Runs the exploit against the target IP."""
    print(f"[\033[32m+\033[0m] Attempting to exploit {service} {version} on {target_ip}:{port} using {exploit_url}")
    
    # Example of running a Metasploit exploit command, replace with real usage
    msf_command = f"msfconsole -q -x 'use {exploit_url}; set RHOSTS {target_ip}; set RPORT {port}; run; exit'"
    subprocess.run(msf_command, shell=True)


