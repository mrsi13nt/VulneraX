import subprocess
import requests
import os
import platform
import sys
import time
import colorama
from termcolor import colored

# Initialize colorama for cross-platform colored output
colorama.init()

home_dir = os.path.expanduser('~')
keys = {
    'hunter': '',
    'shodan': '',
    'pwnd': '',
    'emailrep': '',
    'pipl': '',
    'clearbit': ''
}
key = {
    'socialsearch': ''
}

platforms = ['Twitter', 'Facebook', 'Instagram', 'LinkedIn']


current_user = os.getlogin()
os_name = platform.system()



# check for updates
def get_latest_commit(repo_url):
    # GitHub API to get the latest commit on the main branch
    api_url = f"https://api.github.com/repos/{repo_url}/commits/main"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            latest_commit = response.json()["sha"]
            return latest_commit
        else:
            print(f"[\033[31m!\033[0m] Failed to check for updates. HTTP Status: {response.status_code}")
            return None
    except Exception as e:
        print(f"[\033[31m!\033[0m] Error checking for updates")
        return None

def get_local_commit():
    try:
        # Specify the path to your Git repository
        repo_path = f"{home_dir}/.VulneraX"  # Update this path as necessary
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
            cwd=repo_path  # Use the repo path here
        )

        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"[\033[31m!\033[0m] Error getting local commit: {e}")
        return None

def check_for_updates(repo_url):
    printt('checking updates...')
    latest_commit = get_latest_commit(repo_url)
    local_commit = get_local_commit()
    time.sleep(3)
    
    if latest_commit and local_commit and latest_commit != local_commit:
        print(colored("A new update is available!",'green'))
        choice = input(colored("Do you want to update the tool? (y/n): ",'blue')).lower()
        if choice == 'y' or choice == 'Y':
            update_tool()
        elif choice == 'n' or choice == 'N':
            printt(colored('Continuing without update...','red'))
            clear_screen()
        else:
            printt(colored("wrong answer ! \n Continuing without update...",'red'))
    elif latest_commit and local_commit and latest_commit == local_commit:
        printt(colored("You are using the latest version of the tool.",'green'))
        clear_screen()
    else:
        printt(colored("faild to identify the updates",'red'))

def update_tool():
    destination_directory = f"{home_dir}/.VulneraX"  # This is where you copied the tool

    printt(colored("Updating the tool...", 'cyan'))

    try:
        # Check if the .git directory exists in the destination
        git_directory = os.path.join(destination_directory, ".git")
        
        if not os.path.exists(git_directory):
            print(f"[\033[31m!\033[0m] Error: '.git' directory not found in {destination_directory}.")
            return

        # Change directory to the location of the tool
        os.chdir(destination_directory)
        print(f"[\033[32m+\033[0m] Changed to directory: {destination_directory}")

        # Check for uncommitted changes
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
        if result.stdout.strip():
            print(f"[\033[31m!\033[0m] Uncommitted changes detected.")
            user_choice = input(colored("Do you want to stash your changes before updating? (y/n): ", 'blue')).lower()
            if user_choice == 'y':
                # Stash changes before updating
                subprocess.run(['git', 'stash'], check=True)
                print(f"[\033[32m+\033[0m] Changes stashed.")

                # Perform a git pull to get the latest updates
                subprocess.run(['git', 'pull'], check=True)
                print(f"[\033[32m+\033[0m] Pulled the latest changes successfully.")

                # Reapply stashed changes
                subprocess.run(['git', 'stash', 'pop'], check=True)
                print(f"[\033[32m+\033[0m] Reapplied your changes.")
            else:
                print(f"[\033[31m!\033[0m] Please commit or stash your changes before updating.")
                return
        else:
            # No local changes, proceed with the update
            subprocess.run(['git', 'pull'], check=True)
            print(f"[\033[32m+\033[0m] Pulled the latest changes successfully.")

        # Install/update requirements if any
        subprocess.run('pip install -r requirements.txt --break-system-packages', shell=True, check=True)

        # Re-run setup (if required)
        subprocess.run('sudo python3 setup.py', shell=True)

        print("[\033[32m+\033[0m] Update successful. Please restart the tool.")

    except subprocess.CalledProcessError as e:
        print(f"[\033[31m!\033[0m] Error during update: {e}")
    except Exception as e:
        print(f"[\033[31m!\033[0m] Unexpected error: {e}")


# open the file
def conf():
    if os_name == "Windows":
        subprocess.run(f'start notepad C:\\Users\\{current_user}\\.VulneraX\\src\\configs.py',shell=True)
    elif os_name == "Darwin":
        subprocess.run(f'open /Users/{current_user}/.VulneraX/src/configs.py',shell=True)
    elif os_name == "Linux":
        subprocess.run(f'mousepad /home/{current_user}/.VulneraX/src/configs.py', shell=True)
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
essential_tools = "aircrack-ng"

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

def clear_screen():
    os_name = platform.system()
    if os_name == "Windows":
        subprocess.run('cls',shell=True)
    elif os_name == "Darwin":
        subprocess.run('clear',shell=True)
    elif os_name == "Linux":
        subprocess.run('clear',shell=True)
    else:
        print("Unknown operating system: ", os_name)

def printt(text, delay=0.05):
    """Simulate a typing effect for the given text."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()  # Move to the next line after the text is typed


