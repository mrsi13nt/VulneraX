# VulneraX

**VulneraX** is an all-in-one cybersecurity toolkit designed to assist penetration testers and security researchers in gathering information, conducting vulnerability assessments, and performing web, wireless, and OSINT attacks. The tool integrates multiple features, including port scanning, OSINT lookups, XSS and SQL injection scanning, wireless pentesting, and more, all under a simple CLI interface.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Available Commands](#available-commands)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Information Gathering:**
  - Port scanning
  - Website reconnaissance
- **OSINT:**
  - Domain and IP lookup
  - Email and social media search
- **Web Attacks:**
  - XSS scanning
  - SQL Injection scanning
  - Full web vulnerability scanning (including API key leaks, JS leaks, etc.)
- **Wireless Pentesting:**
  - Wi-Fi and Bluetooth pentesting
- **Vulnerability Assessment:**
  - Local and remote system vulnerability scanning
- **CTF Mode:**
  - Fast and clear information gathering for Capture The Flag competitions
- **Others:**
  - Configuration management
  - Wordlist maker
  - Tool installer (Top 50 cybersecurity tools)

---

## Installation

To install **VulneraX**, follow the steps below:

1. Clone the repository:
    ```bash
    git clone https://github.com/mrsi13nt/VulneraX
    cd VulneraX
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the tool:
    ```bash
    python vulneraX.py
    ```

---

## Usage

Use the following syntax to run **VulneraX**:
```bash
python vulneraX.py [options] arg
