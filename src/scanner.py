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




# this to detect what Linux using
def detect_linux_distro():
    try:
        # Check for popular Linux distros
        if os.path.exists('/etc/os-release'):
            with open('/etc/os-release') as f:
                release_info = f.readlines()
                for line in release_info:
                    if line.startswith('PRETTY_NAME'):
                        distro = line.split('=')[1].strip().replace('"', '')
                        print(f"Linux Distribution: {distro}")
                        break
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
        return True
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

def scanner_remote():
    print('coming soon...')

if __name__ == '__main__':
    scanner_local()