import platform
import subprocess
import time
import colorama
from termcolor import colored
import shutil
import os
import sys

# Initialize colorama
colorama.init()

# Global variables for OS info
os_info_id = []
os_info_vc = []
os_info_il = []

# Detect Linux distribution
def detect_linux_distro():
    try:
        if os.path.exists('/etc/os-release'):
            with open('/etc/os-release') as f:
                release_info = f.readlines()
                for line in release_info:
                    if line.startswith('ID'):
                        os_info_id.append(line.split('=')[1].strip().replace('"', ''))
                    if line.startswith('VERSION_CODENAME'):
                        os_info_vc.append(line.split('=')[1].strip().replace('"', ''))
                    if line.startswith('ID_LIKE'):
                        os_info_il.append(line.split('=')[1].strip().replace('"', ''))
        else:
            print("Unable to detect Linux distribution.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Detect operating system
def detect_os():
    os_name = platform.system()
    if os_name in ["Windows", "Darwin", "Linux"]:
        if os_name == "Linux":
            detect_linux_distro()
        return os_name
    else:
        print("Unknown operating system: ", os_name)
        return None

def run_command(command):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        print(f"Command error: {e}")
        return ""

def check_binary(binary_name):
    if shutil.which(binary_name):
        return "[ \033[32mFOUND\033[0m ]"
    else:
        return "[ \033[31mNOT FOUND\033[0m ]"

def check_package(package_name):
    cmd = f"dpkg -l | grep -i {package_name}"
    result = run_command(cmd)
    print(f"Checking package '{package_name}': {result}")  # Debug output
    if package_name in result:
        return "[ \033[32mInstalled\033[0m ]"
    else:
        return "[ \033[31mNot Installed\033[0m ]"

def check_encryption(partition):
    cmd = f"lsblk -o NAME,MOUNTPOINT,FSTYPE | grep {partition}"
    result = run_command(cmd)
    if 'crypt' in result:
        return "[ \033[32mENCRYPTED\033[0m ]"
    else:
        return "[ NOT ENCRYPTED ]"

def scanner_local():
    print(colored("[+] Initializing", 'blue'))
    print('----------------------')
    
    # Check OS
    os_name = detect_os()
    if os_name is None:
        print('- Detecting OS...                                           [ \033[31mFAILED\033[0m ]')
        sys.exit(1)
    else:
        print('- Detecting OS...                                           [ \033[32mDONE\033[0m ]')

    # Display OS Information
    print(f'Operating system: {os_name}')
    if os_name == 'Linux':
        print(f'Operating system name: {os_info_vc[0] if os_info_vc else "Unknown"}')
        print(f'Operating system version: {os_info_id[0] if os_info_id else "Unknown"}')
    
    binaries = ["/bin", "/sbin", "/usr/bin", "/usr/sbin"]
    for binary in binaries:
        print(f'- Checking {binary}:', check_binary(binary))

    # Check for packages
    software_list = ["libpam-tmpdir", "apt-listbugs", "apt-listchanges", "needrestart", "fail2ban"]
    print("\n- Software checks:")
    for software in software_list:
        print(f"    - {software}: {check_package(software)}")

    # Further checks for Debian OS
    if os_info_il and 'debian' in os_info_il[0].lower():
        print("\n[+] Scanning Debian...")
        print('Other scanning coming soon... ')
def scanner_remote():
    print('coming soon..')
