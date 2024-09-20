import os
import sys
import subprocess
import requests
import socket
import platform
import shutil
from src.configs import printt


essential_tools = "aircrack-ng"

def check_tool(tool_name):
    """Check if a tool is installed."""
    try:
        subprocess.run([tool_name, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def install_tool(tool_name):
    """Install a tool using apt-get."""
    print(f"Installing {tool_name}...")
    subprocess.run('sudo apt install kali-tools-wireless', shell=True)

def check_and_install_tools(tools, category):
    """Check and install tools from a given list."""
    print(f"{category} checking...")
    if check_tool(tools):
        print(f"{tools} .... \033[32mOK\033[0m")
    else:
        print(f"{tools} .... \033[31mNot found\033[0m")
        install_tool(tools)






current_user = os.getlogin()
current_directory = os.getcwd()
# Get the current user's home directory
home_directory = os.path.expanduser('~')
desktop_directory = os.path.join(home_directory, '.local/share/applications')
desktop_file_path = os.path.join(desktop_directory, 'VulneraX.desktop')
os.makedirs(desktop_directory, exist_ok=True)

# Template for the .desktop file
desktop_template = f'''
    [Desktop Entry]
    Name=Black candle
    Exec=bash -c "python3 {home_directory}/.VulneraX/VulneraX.py; bash -i"
    Terminal=true
    Icon={home_directory}/.VulneraX/src/img/logo.png
    Type=Application
    Categories=01-Information-Gathering;Utility;
'''

# Linux

def linux():
    check_and_install_tools(essential_tools, "Essential tools")
    subprocess.run('pip install -r requirements.txt',shell=True) # requirments
    subprocess.run(f'mkdir /home/{current_user}/.VulneraX',shell=True)
    subprocess.run(f'mv src /home/{current_user}/.VulneraX/',shell=True)
    subprocess.run('sudo cp VulneraX.py /usr/bin/',shell=True)
    subprocess.run('sudo cp -r src /usr/bin/',shell=True)
    subprocess.run(f'mv VulneraX.py /home/{current_user}/.VulneraX/',shell=True)
    subprocess.run(f'sudo ln -sf {home_directory}/.VulneraX/VulneraX.py /usr/bin/VulneraX', shell=True, check=True)
    # the modified .desktop file
    with open(desktop_file_path, 'w') as desktop_file:
        desktop_file.write(desktop_template)

    # set permission on the .desktop file
    os.chmod(desktop_file_path, 0o755)
    subprocess.run('sudo update-desktop-database', shell=True, check=True)
    subprocess.run('rm -r *',shell=True)
    sys.exit(1)

# macOS

def macOS():
    # Install required Python packages
    subprocess.run('pip install -r requirements.txt', shell=True)  # requirements

    # Create a hidden directory for VulneraX in the user's home directory
    subprocess.run(f'mkdir /Users/{current_user}/.VulneraX', shell=True)

    # Move the 'src' folder to the hidden .VulneraX directory
    subprocess.run(f'mv src /Users/{current_user}/.VulneraX/', shell=True)

    # Copy VulneraX.py to /usr/local/bin (the typical location for executables in macOS)
    subprocess.run('sudo cp VulneraX.py /usr/local/bin/', shell=True)

    # Move VulneraX.py to the hidden .VulneraX directory
    subprocess.run(f'mv VulneraX.py /Users/{current_user}/.VulneraX/', shell=True)

    # Remove all files in the current directory
    subprocess.run('rm -r *', shell=True)

    # Exit the program
    sys.exit(1)

# Windows
def windows():
    # Install required Python packages
    subprocess.run('pip install -r requirements.txt', shell=True)

    # Create a hidden directory for VulneraX in the user's home directory
    # Windows uses %USERPROFILE% or os.environ['USERPROFILE'] to get the user's home directory
    vulnerax_dir = f"C:\\Users\\{current_user}\\.VulneraX"
    
    if not os.path.exists(vulnerax_dir):
        os.makedirs(vulnerax_dir)

    # Move the 'src' folder to the hidden .VulneraX directory
    src_dir = os.path.join(os.getcwd(), 'src')
    shutil.move(src_dir, vulnerax_dir)

    # Copy VulneraX.py to a directory in the PATH (e.g., C:\Windows\System32 or user-defined directory)
    # It's better to use a user-defined directory rather than System32 due to permission issues
    vulnerax_exe = os.path.join(vulnerax_dir, 'VulneraX.py')
    shutil.copy(vulnerax_exe, f"C:\\Users\\{current_user}\\AppData\\Local\\Programs\\VulneraX\\")

    # Move VulneraX.py to the hidden .VulneraX directory (if necessary)
    shutil.move('VulneraX.py', vulnerax_dir)

    # Remove all files in the current directory
    for file in os.listdir(os.getcwd()):
        if os.path.isfile(file) or os.path.isdir(file):
            try:
                if os.path.isfile(file):
                    os.remove(file)
                else:
                    shutil.rmtree(file)
            except Exception as e:
                print(f"[\033[31m!\033[0m] Error while deleting {file}: {e}")

    # Exit the program
    sys.exit(1)




os_name = platform.system()

def detect_os():
    
    if os_name == "Windows":
        windows()
    elif os_name == "Darwin":
        macOS()
    elif os_name == "Linux":
        linux()
    else:
        print("Unknown operating system: ", os_name)

# def detect_linux_distro():
#     try:
#         # Check for popular Linux distros
#         if os.path.exists('/etc/os-release'):
#             with open('/etc/os-release') as f:
#                 release_info = f.readlines()
#                 for line in release_info:
#                     if line.startswith('PRETTY_NAME'):
#                         distro = line.split('=')[1].strip().replace('"', '')
#                         print(f"Linux Distribution: {distro}")
#                         break
#         else:
#             print("Unable to detect Linux distribution.")
#     except Exception as e:
#         print(f"An error occurred: {e}")







def main():
     print('start setup..')
    # check for network
    # def check_network():
    #         try:
    #             # Try to resolve the hostname
    #             socket.gethostbyname("google.com")
    #             return True
    #         except socket.error:
    #             return False
    # if not check_network():
    #     printt("[\033[31mError\033[0m] No network connection. Please check your internet connection and try again.")
    #     sys.exit(1)
    # printt("[\033[32m+\033[0m] Network connection is available. Continuing with the program...\n")

if __name__ == '__main__':
    main()
    detect_os()