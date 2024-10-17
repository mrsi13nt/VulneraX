#!/usr/bin/env python3

import argparse
import socket
import os
import sys
from src.info_gather import recon, scan
from src.logo import logo, logo_main
from src.osint import lookup_domain, lookup_ip, search_email, social_media
from src.wordlist import wordlist
from src.configs import check_for_updates, conf, printt
from src.web import xss, check_sql_injection, full
from src.ctf import ctf
from src.wifi import wifi
from src.bluetooth import blue
from src.scanner import scanner_local, scanner_remote
from src.tools import tools


sys.dont_write_bytecode = True

# Check network connection
def check_network():
    try:
        socket.gethostbyname("google.com")
        return True
    except socket.error:
        return False

# Web Scanning Handler
def handle_web_scanning(args):
    if args.url:
        if args.xss:
            xss(args.url)
        elif args.sqli:
            check_sql_injection(args.url, parameters=None)
        elif args.full:
            full(args.url)
        else:
            printt('[\033[31m!\033[0m] Please specify scanning type (--xss, --sql, or --full)')
            sys.exit(1)

# OSINT Handling
def handle_osint(args):
    if args.ip:
        lookup_ip(args.ip)
    if args.email:
        search_email(args.email)
    if args.social:
        social_media(args.social)
    if args.domain:
        lookup_domain(args.domain)

# Wireless Pentesting Handler
def handle_wireless(args):
    if args.wifi:
        wifi()
    if args.bluetooth:
        blue()

# Vulnerability Assessment Handler
def handle_scanner(args):
    if args.local:
        scanner_local()
    if args.remote:
        scanner_remote()

# CTF Mode Handler
def handle_ctf(args):
    if args.ctf:
        ctf(args.ctf)

# Tool Installation Handler
def handle_tools(args):
    if args.tools:
        tools()

# Wordlist Generation Handler
def handle_wordlist(args):
    if args.wordlist:
        wordlist()

def edit_config(args):
    if args.config:
        conf()

# Main function
def main():
    parser = argparse.ArgumentParser(prog='VulneraX',
                    description=logo, formatter_class=argparse.RawTextHelpFormatter,
                    usage='%(prog)s [options] arg')

    # Information Gathering
    info = parser.add_argument_group('Information Gathering')
    info.add_argument('-p', action='store', metavar='ip addr', dest='port', help='Port scanning only (like nmap)')
    info.add_argument('-r', action='store', metavar='website', dest='recon', help='Website reconnaissance')

    # OSINT
    osint = parser.add_argument_group('OSINT')
    osint.add_argument('-ip', action='store', dest='ip', metavar='ip', help='Search for IP address')
    osint.add_argument('-s', action='store', dest='social', metavar='name', help='Search for people by name')
    osint.add_argument('-e', action='store', dest='email', metavar='email', help='Search for email addresses')
    osint.add_argument('-d', action='store', dest='domain', metavar='domain', help='Search for domain information')

    # Web Attacks
    web = parser.add_argument_group('Web Attacks')
    web.add_argument('-u', action='store', metavar='URL', dest='url', help='Target URL for scanning')
    web.add_argument('--xss', action='store_true', help='Scan for XSS vulnerabilities')
    web.add_argument('--sqli', action='store_true', help='Scan for SQL injection vulnerabilities')
    web.add_argument('--full', action='store_true', help='Perform full web vulnerability scan')

    # Wireless Pentesting
    wireless = parser.add_argument_group('Wireless Pentesting')
    wireless.add_argument('-w', '--wifi', action='store_true', help='Wi-Fi pentesting')
    wireless.add_argument('-b', '--bluetooth', action='store_true', help='Bluetooth pentesting')

    # Vulnerability Assessment
    vuln = parser.add_argument_group('Vulnerability Assessment')
    vuln.add_argument('--local', action='store_true', help='Scan for vulnerabilities on local machine')
    vuln.add_argument('--remote', action='store_true', help='Scan for vulnerabilities on remote machine')

    # CTF Mode
    ctf_mode = parser.add_argument_group('CTF Mode')
    ctf_mode.add_argument('--ctf', action='store', metavar='ip addr', help='Capture The Flag focused scanning')

    # Tool Installation
    tools_install = parser.add_argument_group('Tool Installation')
    tools_install.add_argument('-I', '--tools', action='store_true', help='Install the top 50 cybersecurity tools')

    # Wordlist Generation
    wordlist_gen = parser.add_argument_group('Wordlist Generation')
    wordlist_gen.add_argument('-W', '--wordlist', action='store_true', help='Generate a custom wordlist')

    #config
    other = parser.add_argument_group('other')
    other.add_argument('--config',action='store_true',dest='config',help='edit your config file')

    # Parse arguments
    args = parser.parse_args()


    # Check if no arguments were provided
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    else:
        # Print Logo
        print(logo_main)

    # Check network connection
    if not check_network():
        printt("[\033[31mError\033[0m] No network connection.")
        sys.exit(1)
    
    printt("Network connection is available.")
    os.system('clear')
    print(logo_main)


    # Information Gathering
    if args.port:
        scan(args.port)
    if args.recon:
        recon(args.recon)

    # OSINT
    handle_osint(args)

    # Web Attacks
    handle_web_scanning(args)

    # Wireless Pentesting
    handle_wireless(args)

    # Vulnerability Assessment
    handle_scanner(args)

    # CTF Mode
    handle_ctf(args)

    # Tool Installation
    handle_tools(args)

    # Wordlist Generation
    handle_wordlist(args)

    # Edit config file
    edit_config(args)

if __name__ == '__main__':
    # Check for updates
    repo_url = "mrsi13nt/VulneraX"
    check_for_updates(repo_url)
    
    # Run the main program
    main()
