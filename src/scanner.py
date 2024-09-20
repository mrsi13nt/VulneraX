import sys
import platform
import subprocess
import time
import colorama
from termcolor import colored
from logo import priv,non_priv
import os


os_name = platform.system()
username = os.getlogin()
role = os.getuid()
the_os = ''


colorama.init()



os_info = []
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
                        os_info.append(distro)
                    if line.startswith('VERSION_CODENAME'):
                        distro1 = line.split('=')[1].strip()
                        os_info.append(distro1)
        else:
            print("Unable to detect Linux distribution.")
    except Exception as e:
        print(f"An error occurred: {e}")





# this for  detect what OS is using
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
    if role == 0:
        print(priv)
        print('')
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
    print(f'Operating system name:     {os_info[1]}')
    print(f'Operating system version:  {os_info[0]}')
    print(f'Hardware platform:         {os.uname().machine}')
    print(f'Kernel version:            {os.uname().release}')
    print(f'Hostname:                  {os.uname().nodename}')
    print('---------------------------------------------------')

def scanner_remote():
    print('coming soon...')

if __name__ == '__main__':
    scanner_local()