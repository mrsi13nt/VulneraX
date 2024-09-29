import argparse
import socket
import os
import sys
from src.info_gather import recon,scan
from src.logo import logo,logo_main
from src.osint import lookup_domain,lookup_ip,search_email,social_media
from src.wordlist import wordlist
from src.configs import check_for_updates,conf
from src.web import *
from src.ctf import ctf
from src.wifi import wifi
from src.bluetooth import blue
from src.scanner import scanner_local,scanner_remote
from src.tools import tools
import subprocess


# check network
def check_network():
        try:
            # Try to resolve the hostname
            socket.gethostbyname("google.com")
            return True
        except socket.error:
            return False
        


# main file
def main():
    # args
    parser = argparse.ArgumentParser(prog='VulneraX',
                    description=logo,formatter_class=argparse.RawTextHelpFormatter,
                    epilog="",
                    usage='%(prog)s [options] arg')
    info = parser.add_argument_group('Information Gathering')
    info.add_argument('-p',action='store',metavar='ip addr', dest='port', help='port scanning only (like nmap)')
    info.add_argument('-r', action='store', metavar='website', dest='recon', help='Website recon (only accept wildcard for now..)')
    osint = parser.add_argument_group('OSINT')
    osint.add_argument('-ip', action='store', dest='ip', metavar='ip', help='search for ip address')
    osint.add_argument('-s', action='store', dest='social', metavar='name', help='search for people')
    osint.add_argument('-e', action='store', dest='email', metavar='email', help='search for emails')
    osint.add_argument('-d', action='store', dest='domain', metavar='domain', help='search for domains')
    wireless = parser.add_argument_group('Wireless Pentesting')
    wireless.add_argument('-w', action='store',metavar='1 or 2', dest='wireless', help='make a full pentest on wireless (1 => wifi, 2 => bluetooth)')
    assessment = parser.add_argument_group('Vulnerability Assessment')
    assessment.add_argument('-v', action='store_true', dest='local', help='make a full local system scan')
    assessment.add_argument('-v', action='store_true', dest='remote', help='make a full remote system scan')
    web = parser.add_argument_group('Web attacks')
    web.add_argument('-u', action='store', dest='url',metavar='url', help='enter the url you want to scan')
    web.add_argument('--xss', action='store_true', dest='xss', help='scan for XSS')
    web.add_argument('--sql', action='store_true', dest='sqli', help='scan for SQLi')
    web.add_argument('--full', action='store_true', dest='full', help='full web scanning includes (xss, sqli, api keys scanning, js leakes, and some other cool things)')
    others = parser.add_argument_group('Others')
    others.add_argument('--config', action='store_true', help='edit your config file, set API tokens')
    others.add_argument('--ctf', action='store', dest='ctf', metavar='ip addr', help='CTF mode, you can think clear from now!')
    others.add_argument('-I', action='store_true', dest='tools', help='install top 50 tools in cybersecurity')
    others.add_argument('-W', action='store_true', dest='wordlist', help='wordlist maker')

    args = parser.parse_args()

    print(logo_main)

    #check if it online or not
    if not check_network():
        printt("[\033[31mError\033[0m] No network connection. Please check your internet connection and try again.")
        sys.exit(1)
    printt("Network connection is available. Continuing with the program...")
    os.system('clear')

    print(logo_main)
    #port scanner
    if args.port:
        scan(args.port)
    # recon
    if args.recon:
        recon(args.recon)
    # OSINT
    if args.ip:
        lookup_ip(args.ip)
    if args.email:
        search_email(args.email)
    if args.social:
        social_media(args.social)
    if args.domain:
        lookup_domain(args.domain)
    # Web
    if args.xss:
        if not args.url:
            printt('[\033[31m!\033[0m] please enter url to scan for XSS by entering: -u URL --xss')
            sys.exit(1)
        else:
            xss(args.url)
    if args.sqli:
        if not args.url:
            printt('[\033[31m!\033[0m] please enter url to scan for SQLi by entering: -u URL --sql')
            sys.exit(1)
        else:
            check_sql_injection(args.url, parameters=None)
    if args.full:
        if not args.url:
            printt('[\033[31m!\033[0m] please enter url to scan for SQLi by entering: -u URL --sql')
            sys.exit(1)
        else:
            full(args.url)
    if args.url:
        printt('[\033[31m!\033[0m] please enter type of scanning (--xss or --sql or --full)')
        sys.exit(1)
    # vuln assessment
    if args.local:
        scanner_local()
    if args.remote:
        scanner_remote()
    # wireless
    if args.wireless == "1" or args.wireless == 1:
        wifi()
    elif args.wireless == "2" or args.wireless == 2:
        blue()
    elif args.wireless and args.wireless != ['1',1,'2',2]:
        printt("[\033[31m!\033[0m] wrong input for wireless pentest you should write for example : -w 1 \n")
    # config 
    if args.config:
        conf()
    # CTF mode
    if args.ctf:
        ctf(args.ctf)
    # Install tools
    if args.tools:
        tools()
    # wordlist maker
    if args.wordlist:
        wordlist()

if __name__ == '__main__':
    repo_url = "mrsi13nt/VulneraX"
    check_for_updates(repo_url)
    main()
