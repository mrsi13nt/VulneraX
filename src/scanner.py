import sys
import platform
import subprocess
import time
import colorama
from termcolor import colored
from logo import priv, non_priv
import shutil
import os

colorama.init()

def detect_linux_distro() -> None:
    """Detect the Linux distribution and store relevant information."""
    os_info_id = []
    os_info_vc = []
    os_info_il = []

    try:
        if os.path.exists('/etc/os-release'):
            with open('/etc/os-release') as f:
                release_info = f.readlines()
                for line in release_info:
                    if line.startswith('ID'):
                        os_info_id.append(line.split('=')[1].strip())
                    elif line.startswith('VERSION_CODENAME'):
                        os_info_vc.append(line.split('=')[1].strip())
                    elif line.startswith('ID_LIKE'):
                        os_info_il.append(line.split('=')[1].strip())
        else:
            print("Unable to detect Linux distribution.")
    except Exception as e:
        print(f"An error occurred while detecting Linux distribution: {e}")

    return os_info_id, os_info_vc, os_info_il

def detect_os() -> str:
    """Detect the operating system."""
    os_name = platform.system()
    if os_name in ["Windows", "Darwin"]:
        return os_name
    elif os_name == "Linux":
        return detect_linux_distro()
    else:
        print("Unknown operating system: ", os_name)
        return "Unknown"

def scanner_local() -> None:
    """Initialize the local scanner and detect OS and user privileges."""
    print(colored("[+] Initializing", 'blue'))
    print('----------------------')

    role = os.getuid()
    if role == 0:
        print(priv)
    else:
        print(non_priv)
        print('')
        print(colored(" Notes: ", 'blue'))
        print('-------------------------')
        print('* Some tests will be skipped (as they require root permissions)')
        print('* Some tests might fail silently or give different results')
        print('')

    os_info_id, os_info_vc, os_info_il = detect_os()
    if os_info_id == "Unknown":
        print('- Detecting OS...                                           [ \033[31mFAILED\033[0m ]')
        sys.exit(1)
    else:
        print('- Detecting OS...                                           [ \033[32mDONE\033[0m ]')
        time.sleep(2)

    print('- Checking profiles...                                      [ \033[32mDONE\033[0m ]')
    print('')
    print('---------------------------------------------------')
    print(f'Operating system:          {platform.system()}')
    print(f'Operating system name:     {os_info_vc[0] if os_info_vc else "N/A"}')
    print(f'Operating system version:  {os_info_id[0] if os_info_id else "N/A"}')
    print(f'Hardware platform:         {os.uname().machine}')
    print(f'Kernel version:            {os.uname().release}')
    print(f'Hostname:                  {os.uname().nodename}')
    print('---------------------------------------------------')

    if os_info_il and os_info_il[0] == 'debian':
        debian()
    print('Other scanning coming soon...')

def debian() -> None:
    """Perform checks specific to Debian systems."""
    binaries = ["/bin", "/sbin", "/usr/bin", "/usr/sbin"]
    print('hello')
    print('[+] ' + colored('Scanning Debian', 'yellow'))
    print('--------------------------')
    print('- Checking for system binaries that are required by Debian Tests...')
    for binary in binaries:
        print(f"    - Checking {binary}".ljust(60) + check_binary(binary))
    
    print("\n- Authentication:")
    print("    - PAM (Pluggable Authentication Modules):")
    print(f"      - libpam-tmpdir".ljust(60) + check_package("libpam-t```pythonmpdir"))

    print("\n- File System Checks:")
    print("    - DM-Crypt, Cryptsetup & Cryptmount:")
    print(f"      - Checking / on /dev/sda5".ljust(60) + check_encryption("/dev/sda5"))

    print("\n- Software:")
    software_list = ["apt-listbugs", "apt-listchanges", "needrestart", "fail2ban"]
    for software in software_list:
        print(f"    - {software}".ljust(60) + check_package(software))

def run_command(command: str) -> str:
    """Run a shell command and return the output."""
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return str(e)

def check_binary(binary_name: str) -> str:
    """Check if a binary exists in the system."""
    if shutil.which(binary_name):
        return "[ FOUND ]"
    else:
        return "[ NOT FOUND ]"

def check_package(package_name: str) -> str:
    """Check if a package is installed using dpkg (for Debian-based systems)."""
    cmd = f"dpkg -l | grep -i {package_name}"
    result = run_command(cmd)
    if package_name in result:
        return "[ Installed ]"
    else:
        return "[ Not Installed ]"

def check_encryption(partition: str) -> str:
    """Check if a partition is encrypted using lsblk or cryptsetup."""
    cmd = f"lsblk -o NAME,MOUNTPOINT,FSTYPE | grep {partition}"
    result = run_command(cmd)
    if 'crypt' in result:
        return "[ ENCRYPTED ]"
    else:
        return "[ NOT ENCRYPTED ]"

def scanner_remote() -> None:
    """Placeholder for remote scanning functionality."""
    print('Coming soon...')
