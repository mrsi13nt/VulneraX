import sys
import platform
import subprocess
import time
import colorama
from termcolor import colored
from logo import priv,non_priv
import shutil
import os


os_name = platform.system()
username = os.getlogin()
role = os.getuid()


colorama.init()



os_info_id = []
os_info_vc = []
os_info_il = []
# this to detect what Linux using
def detect_linux_distro():
    try:
        # Check for popular Linux distros
        if os.path.exists('/etc/os-release'):
            with open('/etc/os-release') as f:
                release_info = f.readlines()
                for line in release_info:
                    if line.startswith('ID'):
                        distro = line.split('=')[1].strip()
                        os_info_id.append(distro)
                    if line.startswith('VERSION_CODENAME'):
                        distro1 = line.split('=')[1].strip()
                        os_info_vc.append(distro1)
                    if line.startswith('ID_LIKE'):
                        distro2 = line.split('=')[1].strip()
                        os_info_il.append(distro2)
        else:
            print("Unable to detect Linux distribution.")
    except Exception as e:
        print(f"An error occurred: {e}")





# this for detect what OS is using
def detect_os():
    
    if os_name == "Windows":
        return True
    elif os_name == "Darwin":
        return True
    elif os_name == "Linux":
        detect_linux_distro()
    else:
        print("Unknown operating system: ", os_name)
        return False


def scanner_local():
    print(colored("[+] Initializing",'blue'))
    print('----------------------')
    # scanner for root priv
    if role == 0:
        print(priv)
        print('')
    # scanner for non root
    else:
        print(non_priv)
        print('')
        print(colored(" Notes: ",'blue'))
        print('-------------------------')
        print('* Some tests will be skipped (as they require root permissions)')
        print('* Some tests might fail silently or give different results')
        print('')
    detect_os()
    if detect_os == False:
        print('- Detecting OS...                                           [ \033[31mFAILD\033[0m ]')
        sys.exit(1)
    else:
        print('- Detecting OS...                                           [ \033[32mDONE\033[0m ]')
        time.sleep(2)
        
    if os_name == 'Linux':
        print('- Checking profiles...                                      [ \033[32mDONE\033[0m ]')
    elif os_name == 'Windows':
        print('- Checking profiles...                                      [ \033[32mDONE\033[0m ]')
    elif os_name == "Darwin":
        print('- Checking profiles...                                      [ \033[32mDONE\033[0m ]')
    else:
        print(colored("Error please try again...",'red'))
        sys.exit(1)
    print('')
    print('---------------------------------------------------')
    print(f'Operating system:          {os_name}')
    print(f'Operating system name:     {os_info_vc[0]}')
    print(f'Operating system version:  {os_info_id[0]}')
    print(f'Hardware platform:         {os.uname().machine}')
    print(f'Kernel version:            {os.uname().release}')
    print(f'Hostname:                  {os.uname().nodename}')
    print('---------------------------------------------------')
    # for debian OS
    if os_info_il[0] == 'debian':
        debian()
    print('other scanning coming soon... ')
        




def debian():
    binaries = ["/bin", "/sbin", "/usr/bin", "/usr/sbin"]
    print('hello')
    print('[+] ' + colored('scanning Debian','yellow'))
    print('--------------------------')
    print('- Checking for system binaries that are required by Debian Tests...')
    for binary in binaries:
        print(f"    - Checking {binary}".ljust(60) + check_binary(binary))
        print("\n- Authentication:")
        print("    - PAM (Pluggable Authentication Modules):")
        print(f"      - libpam-tmpdir".ljust(60) + check_package("libpam-tmpdir"))
        print("\n- File System Checks:")
        print("    - DM-Crypt, Cryptsetup & Cryptmount:")
        print(f"      - Checking / on /dev/sda5".ljust(60) + check_encryption("/dev/sda5"))
        print("\n- Software:")
        software_list = ["apt-listbugs", "apt-listchanges", "needrestart", "fail2ban"]
        for software in software_list:
            print(f"    - {software}".ljust(60) + check_package(software))





# Helper function to run shell commands
def run_command(command):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return str(e)
    

# Check if the binary exists in the system
def check_binary(binary_name):
    if shutil.which(binary_name):
        return "[ FOUND ]"
    else:
        return "[ NOT FOUND ]"
    
# Check if a package is installed using dpkg (for Debian-based systems)
def check_package(package_name):
    cmd = f"dpkg -l | grep -i {package_name}"
    result = run_command(cmd)
    if package_name in result:
        return "[ Installed ]"
    else:
        return "[ Not Installed ]"

# Check if a partition is encrypted using lsblk or cryptsetup
def check_encryption(partition):
    cmd = f"lsblk -o NAME,MOUNTPOINT,FSTYPE | grep {partition}"
    result = run_command(cmd)
    if 'crypt' in result:
        return "[ ENCRYPTED ]"
    else:
        return "[ NOT ENCRYPTED ]"


def scanner_remote():
    print('coming soon...')

if __name__ == '__main__':
    scanner_local()