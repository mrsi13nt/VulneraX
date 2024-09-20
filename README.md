

# VulneraX

VulneraX is a comprehensive cybersecurity tool designed to help professionals with information gathering, OSINT, vulnerability assessment, and web attack detection. It includes multiple modules for scanning, searching, and testing a wide range of vulnerabilities such as XSS, SQL injection, and much more. 

## Features
- **Information Gathering**: Scan ports, gather OSINT data, and search for specific information like IP addresses, domains, or emails.
- **OSINT (Open Source Intelligence)**: Search for IP addresses, people, social media accounts, emails, and domains.
- **Vulnerability Assessment**: Scan websites for vulnerabilities such as XSS, SQL injection, and perform a full web scan.
- **Web Attacks**: Detect common vulnerabilities in web applications, including SQL Injection (SQLi) and Cross-Site Scripting (XSS).
- **CTF Mode**: Engage in Capture the Flag exercises with custom modes and clear guidance.
- **Tool Installer**: Install the top 50 cybersecurity tools with a single command.
- **Wordlist Maker**: Generate custom wordlists for brute-force attacks.

## Usage


usage: vulnerax [options] arg


### Arguments

#### Information Gathering
- `-p [ip addr]` : Port scanning for a specific IP address.

#### OSINT
- `-ip [ip]` : Search for information related to a specific IP address.
- `-s [name]` : Search for a person by name.
- `-e [email]` : Search for a specific email address.
- `-d [domain]` : Search for domain-related information.

#### Vulnerability Assessment
- `-u [url]` : Enter the URL of the website you want to scan.
- `--xss` : Scan for Cross-Site Scripting (XSS) vulnerabilities.
- `--sql` : Scan for SQL Injection vulnerabilities.
- `--full` : Perform a full web scan, including XSS, SQLi, API key scanning, JS leaks, and more.

#### Others
- `--ctf [ip addr]` : CTF mode for enhanced focus during Capture The Flag exercises.
- `-I` : Install the top 50 cybersecurity tools.
- `-w` : Create a wordlist for brute-force attacks.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/vulnerax.git
   cd vulnerax
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Example Usage

### Port Scanning
```bash
python vulnerax.py -p 192.168.1.1
```

### OSINT (IP search)
```bash
python vulnerax.py -ip 8.8.8.8
```

### Web Attacks (Full scan)
```bash
python vulnerax.py -u http://example.com --full
```

### Install Top Cybersecurity Tools
```bash
python vulnerax.py -I
```

## Contributing
Contributions are welcome! If you have any ideas, issues, or improvements, feel free to open an issue or a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.


### Key Sections:
1. **Introduction**: Gives an overview of the tool.
2. **Features**: Lists the capabilities of VulneraX.
3. **Usage**: Provides the syntax for using the tool and explanations for each command.
4. **Installation**: Explains how to set up the tool.
5. **Example Usage**: Offers sample commands for users to try.
6. **Contributing**: Encourages contributions to the project.
7. **License**: Mentions the license under which the tool is distributed.
