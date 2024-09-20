import whois
import requests
from src.configs import keys,platforms,key
from src.configs import printt

def lookup_domain(domain):
    try:
        domain_info = whois.whois(domain)
        print(f"[\033[32m+\033[0m] Domain: {domain}")
        print(f"[\033[32m+\033[0m] Registrar: {domain_info.registrar}")
        print(f"[\033[32m+\033[0m] Creation Date: {domain_info.creation_date}")
        print(f"[\033[32m+\033[0m] Expiration Date: {domain_info.expiration_date}")
        print(f"[\033[32m+\033[0m] Nameservers: {domain_info.name_servers}")
    except Exception as e:
        print(f"[\033[31m!\033[0m] Error: {e}")

def social_media(username):
    print(f"Searching for social media accounts with the name: {username}")
    for platform in platforms:
        try:
            if keys.get('socialsearch') == '':
                printt('[\033[31m!\033[0m] No socialsearch API key entered\nsorry we can\'t scan, go to edit your config file (--config) and add the API key')
            else:
                # Example search URL for each platform (replace with actual API or scraping logic)
                # Replace 'your_api_key_here' with actual keys if required.
                url = f"https://api.socialsearch.com/search?name={username}&platform={platform}&apikey={key.get('socialsearch')}"
                response = requests.get(url)

                if response.status_code == 200:
                    results = response.json()
                    print(f"Top 6 results on {platform}:")
                    for account in results['accounts'][:6]:  # Top 6 results
                        print(f"[\033[32m+\033[0m] Name: {account['name']}, URL: {account['profile_url']}")
                else:
                    printt(f"[\033[31m!\033[0m] Error on {platform}: Status code {response.status_code}")
        except Exception as e:
            printt(f"[\033[31m!\033[0m] Error occurred while searching on {platform}: {e}")

def search_email(email):
    print(f"Searching for email: {email}")
    
    # Hunter.io Email Finder API
    if keys.get('hunter') == '':
        printt("[\033[31m!\033[0m] No Hunter.io API key entered")
    else:
        try:
            response = requests.get(f"https://api.hunter.io/v2/email-finder?email={email}&api_key={keys.get('hunter')}")
            if response.status_code == 200:
                print("Hunter.io Results:")
                print(response.json())
            else:
                printt(f"[\033[31m!\033[0m] Hunter.io Error: {response.status_code}")
        except Exception as e:
            printt(f"[\033[31m!\033[0m] Hunter.io error: {e}")

    # Shodan API (email search in some cases requires enterprise access)
    if keys.get('shodan') == '':
        printt("[\033[31m!\033[0m] No Shodan API key entered")
    else:
        try:
            response = requests.get(f"https://api.shodan.io/shodan/host/search?query={email}&key={keys.get('shodan')}")
            if response.status_code == 200:
                print("Shodan Results:")
                print(response.json())
            else:
                printt(f"[\033[31m!\033[0m] Shodan Error: {response.status_code}")
        except Exception as e:
            printt(f"[\033[31m!\033[0m] Shodan error: {e}")
    
    # HaveIBeenPwned (HIBP) API
    if keys.get('pwnd') == '':
        printt("[\033[31m!\033[0m] No HaveIBeenPwned API key entered")
    else:
        try:
            headers = {
                'hibp-api-key': keys.get('pwnd'),
                'User-Agent': 'Your Tool'
            }
            response = requests.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}", headers=headers)
            if response.status_code == 200:
                print("HaveIBeenPwned Results:")
                print(response.json())
            else:
                printt(f"[\033[31m!\033[0m] HaveIBeenPwned Error: {response.status_code}")
        except Exception as e:
            printt(f"[\033[31m!\033[0m] HaveIBeenPwned error: {e}")

    # EmailRep.io API (email reputation)
    if keys.get('emailrep') == '':
        printt("[\033[31m!\033[0m] No EmailRep API key entered")
    else:
        try:
            response = requests.get(f"https://emailrep.io/{email}", headers={'Key': keys.get('emailrep')})
            if response.status_code == 200:
                print("EmailRep Results:")
                print(response.json())
            else:
                printt(f"[\033[31m!\033[0m] EmailRep Error: {response.status_code}")
        except Exception as e:
            printt(f"[\033[31m!\033[0m] EmailRep error: {e}")

    # Pipl API (deep people search, including email addresses)
    if keys.get('pipl') == '':
        printt("[\033[31m!\033[0m] No Pipl API key entered")
    else:
        try:
            response = requests.get(f"https://api.pipl.com/search/?email={email}&key={keys.get('pipl')}")
            if response.status_code == 200:
                print("Pipl Results:")
                print(response.json())
            else:
                printt(f"[\033[31m!\033[0m] Pipl Error: {response.status_code}")
        except Exception as e:
            printt(f"[\033[31m!\033[0m] Pipl error: {e}")

    # Clearbit API (email enrichment and search)
    if keys.get('clearbit') == '':
        printt("[\033[31m!\033[0m] No Clearbit API key entered")
    else:
        try:
            response = requests.get(f"https://person.clearbit.com/v2/combined/find?email={email}", headers={'Authorization': f"Bearer {keys.get('clearbit')}"})
            if response.status_code == 200:
                print("Clearbit Results:")
                print(response.json())
            else:
                printt(f"[\033[31m!\033[0m] Clearbit Error: {response.status_code}")
        except Exception as e:
            printt(f"[\033[31m!\033[0m] Clearbit error: {e}")
    if key.get(all) == '':
        printt('\n[\033[31m!\033[0m] sorry you didn\'t enter any API key in config file, to edit it use --config')

def lookup_ip(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        data = response.json()
        print(f"[\033[32m+\033[0m] IP Address: {ip}")
        print(f"[\033[32m+\033[0m] Location: {data.get('city')}, {data.get('region')}, {data.get('country')}")
        print(f"[\033[32m+\033[0m] ISP: {data.get('org')}")
        print(f"[\033[32m+\033[0m] Coordinates: {data.get('loc')}")
    except Exception as e:
        printt(f"[\033[31m!\033[0m] Error: {e}")