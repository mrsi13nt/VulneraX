import os
import sys
import subprocess
import platform
import shutil
import colorama
import time



def printt(text, delay=0.05):
    """Simulate a typing effect for the given text."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()  # Move to the next line after the text is typed


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
    printt(f"Installing {tool_name}...")
    subprocess.run('sudo apt install kali-tools-wireless -y', shell=True)
    subprocess.run('sudo apt install reaver -y')

def check_and_install_tools(tools, category):
    """Check and install tools from a given list."""
    print(f"/033[1;32;40m {category} checking...")
    if check_tool(tools):
        print(f"{tools} .... \033[32mOK\033[0m")
    else:
        print(f"{tools} .... \033[31mNot found\033[0m")
        install_tool(tools)






current_user = os.getlogin()
current_directory = os.getcwd()
# Get the current user's home directory
home_directory = os.path.expanduser('~')
desktop_directory = '/usr/share/kali-menu/applications'
desktop_directory2 = f'{home_directory}/.local/share/applications/'
desktop_file_path = os.path.join(desktop_directory, 'VulneraX.desktop')
desktop_file_path2 = os.path.join(desktop_directory, 'VulneraX.desktop')
os.makedirs(desktop_directory, exist_ok=True)
os.makedirs(desktop_directory2, exist_ok=True)

# Template for the .desktop file
desktop_template = f'''
    [Desktop Entry]
    Name=VulneraX
    Exec=bash -c "python3 {home_directory}/.VulneraX/VulneraX.py; bash -i"
    Terminal=true
    Icon={home_directory}/.VulneraX/src/img/logo.png
    Type=Application
    Categories=01-info-gathering;02-vulnerability-analysis;
'''

# Linux

def linux():
    destination_directory = f"{home_directory}/.VulneraX"
    try:
        # If the destination directory exists, remove it
        if os.path.exists(destination_directory):
            print(f"Removing existing directory: {destination_directory}")
            shutil.rmtree(destination_directory)
        subprocess.run('pip3 install -r requirements.txt --break-system-packages',shell=True) # requirments
        subprocess.run(f'mkdir -p {home_directory}/.VulneraX',shell=True)
        print(f"Copying files from {current_directory} to {destination_directory}...")
        # Copy files from current directory to the destination (this includes .git)
        shutil.copytree(current_directory, destination_directory,dirs_exist_ok=True)

        # Set executable permissions on the main script
        subprocess.run(['sudo', 'chmod', '+x', f'{destination_directory}/VulneraX.py'], check=True)
        
        # Create a symbolic link to run the tool from anywhere
        subprocess.run(f'sudo ln -sf {destination_directory}/VulneraX.py /usr/bin/VulneraX', shell=True, check=True)
        
        # Detect the Linux distro and install necessary tools
        detect_kalilinux_distro()
            
        # the modified .desktop file
        with open(desktop_file_path, 'w') as desktop_file:
            desktop_file.write(desktop_template)

        # Set permission on the .desktop file
        os.chmod(desktop_file_path, 0o755)

        # the modified .desktop file
        with open(desktop_file_path2, 'w') as desktop_file:
            desktop_file.write(desktop_template)

        # Set permission on the .desktop file
        os.chmod(desktop_file_path2, 0o755)
        subprocess.run('sudo update-desktop-database', shell=True, check=True)
        if len(os_info) >= 2 and (os_info[-2] == 'kali' or os_info[-1] == 'kali'):
            printt('it\'s kali linux')
            check_and_install_tools(essential_tools, "Essential tools")
            
            # the modified .desktop file
            with open(desktop_file_path, 'w') as desktop_file:
                desktop_file.write(desktop_template)

            # Set permission on the .desktop file
            os.chmod(desktop_file_path, 0o755)
            subprocess.run('sudo update-desktop-database', shell=True, check=True)
            
            # Clean up the current directory (if needed)
            #subprocess.run('rm -r *', shell=True)
            sys.exit(1)

        elif os_info[-2] == 'ubuntu':
            check_and_install_tools(essential_tools, "Essential tools")
            #subprocess.run('rm -r *', shell=True)
            sys.exit(1)
        
        if os_info[-1] == 'arch':
            subprocess.run('sudo pacman -S wireless_tools', shell=True)

    except Exception as e:
        print(f"An error occurred during setup: {e}")
# macOS

def macOS():
    # Install required Python packages
    subprocess.run('pip install -r requirements.txt', shell=True)  # requirements

    # Create a hidden directory for VulneraX in the user's home directory
    subprocess.run(f'mkdir /Users/{current_user}/.VulneraX', shell=True)

    # Move the 'src' folder to the hidden .VulneraX directory
    subprocess.run(f'mv src /Users/{current_user}/.VulneraX/', shell=True)

    # Move VulneraX.py to the hidden .VulneraX directory
    subprocess.run(f'mv VulneraX.py /Users/{current_user}/.VulneraX/', shell=True)

    # create shortcut
    subprocess.run(f'sudo ln -sf /Users/{current_user}/.VulneraX/VulneraX.py /usr/local/bin/VulneraX', shell=True, check=True)

    # Remove all files in the current directory
    subprocess.run('rm -r *', shell=True)

    # Exit the program
    sys.exit(1)

# Windows
def windows():
    import winshell
    # Create directory for VulneraX in the user's home directory
    vulneraX_directory = os.path.join(home_directory, 'VulneraX')
    os.makedirs(vulneraX_directory, exist_ok=True)

    # Install required Python packages
    subprocess.run('pip install -r requirements.txt', shell=True)

    # Move source files to the VulneraX directory
    try:
        shutil.move('src', vulneraX_directory)
        shutil.move('VulneraX.py', vulneraX_directory)
    except Exception as e:
        print(f"[\033[31m!\033[0m] Error moving files: {e}")
        sys.exit(1)

    # Create a batch file for running the tool
    batch_file_path = os.path.join(home_directory, 'VulneraX.bat')
    batch_template = f'''
    @echo off
    python "{vulneraX_directory}\\VulneraX.py"
    pause
    '''
    
    # Write the batch file
    try:
        with open(batch_file_path, 'w') as batch_file:
            batch_file.write(batch_template)
    except Exception as e:
        print(f"[\033[31m!\033[0m] Error creating batch file: {e}")
        sys.exit(1)

    # Optional: Create a shortcut on the desktop
    desktop_directory = os.path.join(home_directory, 'Desktop')
    shortcut_path = os.path.join(desktop_directory, 'VulneraX.lnk')

    create_shortcut(batch_file_path, shortcut_path, vulneraX_directory)

    # Print completion message
    print(f'Setup complete. You can run VulneraX from the desktop or by executing the batch file located at {batch_file_path}.')

    # Clean up current directory
    cleanup_current_directory()

def create_shortcut(target, shortcut_path, working_directory):
    import winshell
    try:
        with winshell.shortcut(shortcut_path) as shortcut:
            shortcut.path = target
            shortcut.working_directory = working_directory
            shortcut.description = "VulneraX Tool"
            shortcut.icon_location = os.path.join(working_directory, "src", "img", "logo.ico")
    except Exception as e:
        print(f"[\033[31m!\033[0m] Error creating shortcut: {e}")

def cleanup_current_directory():
    # Remove all files and directories in the current directory
    for file in os.listdir(os.getcwd()):
        file_path = os.path.join(os.getcwd(), file)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"[\033[31m!\033[0m] Error while deleting {file_path}: {e}")
    
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
os_info = []
def detect_kalilinux_distro():
    try:
        # Check for popular Linux distros
        if os.path.exists('/etc/os-release'):
            with open('/etc/os-release') as f:
                release_info = f.readlines()
                for line in release_info:
                    if line.startswith('ID'):
                        distro = line.split('=')[1].strip()
                        os_info.append(distro)
                    if line.startswith('ID_LIKE'):
                        distro2 = line.split('=')[1].strip()
                        os_info.append(distro2)
        else:
            print("Unable to detect Linux distribution.")
    except Exception as e:
        print(f"An error occurred: {e}")







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