import argparse
import socket
import sys
import datetime
from src.portscanner import *
from src.logo import *
from src.osint import *
from src.wordlist import *
from src.configs import *
from src.web import *
from src.ctf import *
from src.wifi import *
from src.bluetooth import *
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
    usage = 'usage: vulnerax [options] arg'
    parser = argparse.ArgumentParser(prog='VulneraX',
                    description=logo,formatter_class=argparse.RawTextHelpFormatter,
                    epilog="",
                    usage='%(prog)s [options] arg')
    info = parser.add_argument_group('Information Gathering')
    info.add_argument('-p',action='store',metavar='ip addr', dest='port', help='port scanning only')
    osint = parser.add_argument_group('OSINT')
    osint.add_argument('-ip', action='store', dest='ip', metavar='ip', help='search for ip address')
    osint.add_argument('-s', action='store', dest='social', metavar='name', help='search for people')
    osint.add_argument('-e', action='store', dest='email', metavar='email', help='search for emails')
    osint.add_argument('-d', action='store', dest='domain', metavar='domain', help='search for domains')
    wireless = parser.add_argument_group('Wireless Pentesting')
    wireless.add_argument('-w', action='store', dest='wireless', help='make a full pentest on wireless (1 => wifi, 2 => bluetooth)')
    assessment = parser.add_argument_group('Vulnerability Assessment')
    assessment.add_argument('-r', action='store_true', dest='assess', help='make a sorted report contains all your scanning results\nonly in web and OSINT and info gathering and wireless pentest')
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


    # check if it online or not
    # if not check_network():
    #     print("[\033[31mError\033[0m] No network connection. Please check your internet connection and try again.")
    #     sys.exit(1)
    # print("Network connection is available. Continuing with the program...")

        

    # port scanner
    if args.port:
        scan()
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
            print('please enter url to scan for XSS by entering: -u URL --xss')
            sys.exit(1)
        else:
            xss(args.url)
    if args.sqli:
        if not args.url:
            print('please enter url to scan for SQLi by entering: -u URL --sql')
            sys.exit(1)
        else:
            check_sql_injection(args.url, parameters=None)
    if args.full:
        if not args.url:
            print('please enter url to scan for SQLi by entering: -u URL --sql')
            sys.exit(1)
        else:
            full(args.url)
    if args.url:
        print('please enter type of scanning (--xss or --sql or --full)')
        sys.exit(1)
    # wireless
    if args.wireless == "1" or args.wireless == 1:
        wifi()
    elif args.wireless == "2" or args.wireless == 2:
        blue()
    elif args.wireless and args.wireless != ['1',1,'2',2]:
        print("wrong input for wireless pentest you should write for example : -w 1 \n")
    # config 
    if args.config:
        conf()
    # CTF mode
    if args.ctf:
        ctf(args.ctf)
    # Install tools
    if args.tools:
        subprocess.run('bash src/tools.sh',shell=True)
    # wordlist maker
    if args.wordlist:
        wordlist()


if __name__ == '__main__':
    main()
