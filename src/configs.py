import subprocess
import requests
import os
import platform
import sys



keys = {
    'hunter': '',
    'shodan': '',
    'pwnd': '',
    'emailrep': '',
    'pipl': '',
    'clearbit': '',
    'socialsearch': ''
}


platforms = ['Twitter', 'Facebook', 'Instagram', 'LinkedIn']


current_user = os.getlogin()
os_name = platform.system()



# check for updates
def get_latest_commit():
    # GitHub API to get the latest commit on the main branch
    api_url = "https://api.github.com/repos/mrsi13nt/VulneraX/commits/main"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            latest_commit = response.json()["sha"]
            return latest_commit
        else:
            print(f"Failed to check for updates. HTTP Status: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error checking for updates: {str(e)}")
        return None

def get_local_commit():
    try:
        result = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error getting local commit: {e}")
        return None

def check_for_updates(repo_url):
    latest_commit = get_latest_commit(repo_url)
    local_commit = get_local_commit()
    
    if latest_commit and local_commit and latest_commit != local_commit:
        print("A new update is available!")
        choice = input("Do you want to update the tool? (y/n): ").lower()
        if choice == 'y':
            update_tool()
        else:
            print("Continuing without update...")
    else:
        print("You are using the latest version of the tool.")

def update_tool():
    print("Updating the tool...")
    try:
        # Pull the latest changes from the repository
        subprocess.run(["git", "pull"], check=True)
        subprocess.run('python3 setup.py',shell=True)
        print("Update successful. Please restart the tool.")
    except subprocess.CalledProcessError as e:
        print(f"Error during update: {e}")


# open the file
def conf():
    if os_name == "Windows":
        subprocess.run('mousepad ',shell=True)
    elif os_name == "Darwin":
        subprocess.run('mousepad',shell=True)
    elif os_name == "Linux":
        subprocess.run(f'mousepad /home/{current_user}/mytools/VulneraX/src/configs.py', shell=True)
    else:
        print("Unknown operating system: ", os_name)






# List of common XSS payloads
xss_payloads = [
    "<script>alert('XSS')</script>",
    "'\"><script>alert('XSS')</script>",
    "\"><svg/onload=alert('XSS')>",
]



# List of payloads to test for SQL Injection
sql_payloads = [
    "' OR '1'='1",
    "' OR '1'='1' --",
    "' OR '1'='1' #",
    '" OR "1"="1',
    '" OR "1"="1" --',
    '" OR "1"="1" #',
    "' UNION SELECT NULL, NULL, NULL --",
    '" UNION SELECT NULL, NULL, NULL --'
]







# List of essential and optional tools
essential_tools = [
    "iw", "awk", "airmon-ng", "airodump-ng", "aircrack-ng",
    "xterm", "ip", "lspci", "ps"
]

optional_tools = [
    "bettercap", "ettercap", "dnsmasq", "hostapd-wpe", "beef-xss",
    "aireplay-ng", "bully", "nft", "pixiewps", "dhcpd", "asleap",
    "packetforge-ng", "hashcat", "wpaclean", "hostapd", "tcpdump",
    "etterlog", "tshark", "mdk4", "wash", "hcxdumptool",
    "reaver", "hcxpcapngtool", "john", "crunch", "lighttpd",
    "openssl"
]



def ask():
    q = input('do you want to exit? (y/n) > ')
    if q == ['Y','y','']:
        print('\n bye bye !')
        sys.exit(1)
    else:
        pass