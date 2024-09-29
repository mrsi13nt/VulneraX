import subprocess
import os
import platform

def run_command(command):
    """Run a command in the shell and handle errors."""
    try:
        print(f"Running: {command}")
        subprocess.run(command, shell=True, check=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing: {command}")
        print(e)

def detect_os():
    """Detect the Linux distribution."""
    try:
        distro = platform.linux_distribution()[0].lower()
    except AttributeError:
        # For Python 3.8+, use the alternative method to detect the distro
        try:
            with open("/etc/os-release") as f:
                distro_info = f.read()
            if "ubuntu" in distro_info.lower():
                return "ubuntu"
            elif "debian" in distro_info.lower():
                return "debian"
            elif "centos" in distro_info.lower():
                return "centos"
            elif "fedora" in distro_info.lower():
                return "fedora"
            elif "arch" in distro_info.lower():
                return "arch"
        except FileNotFoundError:
            return "unknown"
    return distro

def install_tools_debian():
    """Install tools for Debian-based systems."""
    current_user = os.getenv("USER")
    
    commands = [
        "sudo apt-get update -y",
        "sudo apt-get upgrade -y",
        "sudo apt install golang-go -y",
        
        # ProjectDiscovery tools
        "go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest",
        f"sudo cp /home/{current_user}/go/bin/httpx /usr/bin",

        "go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest",
        f"sudo cp /home/{current_user}/go/bin/naabu /usr/bin",

        "go install -v github.com/tomnomnom/assetfinder@latest",
        f"sudo cp /home/{current_user}/go/bin/assetfinder /usr/bin",

        # Additional tools
        "sudo apt install nmap -y",
        "sudo apt install sqlmap -y",
        "sudo apt install gobuster -y",
    ]
    
    for command in commands:
        run_command(command)

def install_tools_centos():
    """Install tools for CentOS-based systems."""
    current_user = os.getenv("USER")
    
    commands = [
        "sudo yum update -y",
        "sudo yum upgrade -y",
        "sudo yum install golang -y",

        # ProjectDiscovery tools
        "go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest",
        f"sudo cp /home/{current_user}/go/bin/httpx /usr/bin",

        "go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest",
        f"sudo cp /home/{current_user}/go/bin/naabu /usr/bin",

        "go install -v github.com/tomnomnom/assetfinder@latest",
        f"sudo cp /home/{current_user}/go/bin/assetfinder /usr/bin",

        # Additional tools
        "sudo yum install nmap -y",
        "sudo yum install sqlmap -y",
        "sudo yum install gobuster -y",
    ]

    for command in commands:
        run_command(command)

def install_tools_fedora():
    """Install tools for Fedora-based systems."""
    current_user = os.getenv("USER")
    
    commands = [
        "sudo dnf update -y",
        "sudo dnf upgrade -y",
        "sudo dnf install golang -y",

        # ProjectDiscovery tools
        "go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest",
        f"sudo cp /home/{current_user}/go/bin/httpx /usr/bin",

        "go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest",
        f"sudo cp /home/{current_user}/go/bin/naabu /usr/bin",

        "go install -v github.com/tomnomnom/assetfinder@latest",
        f"sudo cp /home/{current_user}/go/bin/assetfinder /usr/bin",

        # Additional tools
        "sudo dnf install nmap -y",
        "sudo dnf install sqlmap -y",
        "sudo dnf install gobuster -y",
    ]

    for command in commands:
        run_command(command)

def install_tools_arch():
    """Install tools for Arch Linux."""
    current_user = os.getenv("USER")
    
    commands = [
        "sudo pacman -Syu --noconfirm",
        "sudo pacman -S go --noconfirm",

        # ProjectDiscovery tools
        "go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest",
        f"sudo cp /home/{current_user}/go/bin/httpx /usr/bin",

        "go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest",
        f"sudo cp /home/{current_user}/go/bin/naabu /usr/bin",

        "go install -v github.com/tomnomnom/assetfinder@latest",
        f"sudo cp /home/{current_user}/go/bin/assetfinder /usr/bin",

        # Additional tools
        "sudo pacman -S nmap --noconfirm",
        "sudo pacman -S sqlmap --noconfirm",
        "sudo pacman -S gobuster --noconfirm",
    ]

    for command in commands:
        run_command(command)

def tools():
    os_type = detect_os()

    if os_type == "debian" or os_type == "ubuntu":
        print("Debian or Ubuntu detected. Installing tools for Debian-based systems.")
        install_tools_debian()
    elif os_type == "centos":
        print("CentOS detected. Installing tools for CentOS-based systems.")
        install_tools_centos()
    elif os_type == "fedora":
        print("Fedora detected. Installing tools for Fedora-based systems.")
        install_tools_fedora()
    elif os_type == "arch":
        print("Arch Linux detected. Installing tools for Arch Linux.")
        install_tools_arch()
    else:
        print("Unsupported Linux distribution. Exiting...")

