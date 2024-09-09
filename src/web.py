import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
from src.configs import sql_payloads,xss_payloads,printt



# XSS


def is_vulnerable(response):
    """
    Checks if a given response contains an XSS payload.
    """
    for payload in xss_payloads:
        if payload in response.text:
            return True
    return False

def xss(url):
    """
    Scans a given URL for XSS vulnerabilities.
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all forms
        forms = soup.find_all("form")

        print(f"[\033[32m+\033[0m] Found {len(forms)} forms on {url}")

        for form in forms:
            action = form.get("action")
            method = form.get("method", "get").lower()
            form_url = urljoin(url, action)
            
            inputs = form.find_all("input")
            data = {}
            
            for input_tag in inputs:
                name = input_tag.get("name")
                if not name:
                    continue
                value = input_tag.get("value", "test")
                data[name] = value

            for payload in xss_payloads:
                for key in data.keys():
                    data[key] = payload
                    if method == "post":
                        res = requests.post(form_url, data=data)
                    else:
                        res = requests.get(form_url, params=data)
                    
                    if is_vulnerable(res):
                        print(f"[\033[32m+\033[0m] XSS vulnerability found on {form_url}")
                        print(f"Payload: {payload}")
                        break
                else:
                    continue
                break

    except requests.RequestException as e:
        print(f"[\033[31m!\033[0m] Error scanning {url}: {e}")


# SQLI


def check_sql_injection(url, parameters):
    """
    Check for SQL Injection vulnerabilities.
    
    :param url: URL of the web application to test
    :param parameters: Dictionary of parameters to test
    :return: None
    """
    
    for param in parameters:
        for payload in sql_payloads:
            test_params = parameters.copy()
            test_params[param] = payload
            
            try:
                response = requests.get(url, params=test_params)
                if "error" in response.text.lower() or "syntax" in response.text.lower():
                    print(f"[\033[32m+\033[0m] Potential SQL Injection vulnerability detected with payload '{payload}' in parameter '{param}'.")
                else:
                    print(f"Payload '{payload}' in parameter '{param}' seems safe.")
            except Exception as e:
                print(f"[\033[31m!\033[0m] Error testing payload '{payload}' in parameter '{param}': {e}")


    parameters = {}
    
    while True:
        param = input("Enter a parameter to test (or leave blank to finish): ")
        if not param:
            break
        value = input(f"Enter a value for parameter '{param}': ")
        parameters[param] = value
    


# API scanner

def get_js_files(url):
    """
    Get all JavaScript file URLs from a webpage.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    scripts = soup.find_all('script', src=True)
    js_files = [script['src'] for script in scripts if script['src'].endswith('.js')]
    return js_files

def scan_js_file(url, js_file):
    """
    Scan a JavaScript file for exposed API keys.
    """
    parsed_url = urljoin(url, js_file)
    response = requests.get(parsed_url)
    if response.status_code == 200:
        content = response.text
        # Simple regex pattern to identify potential API keys
        api_key_pattern = re.compile(r'(?i)([a-z0-9]{32,})')
        matches = api_key_pattern.findall(content)
        return matches
    else:
        print(f"[\033[31m!\033[0m] Failed to retrieve {parsed_url}")
        return []

def js_scan(url):
    js_files = get_js_files(url)
    print(f"Found {len(js_files)} JavaScript files.")
    for js_file in js_files:
        print(f"Scanning {js_file} for exposed API keys...")
        api_keys = scan_js_file(url, js_file)
        if api_keys:
            print(f"[\033[32m+\033[0m] Exposed API keys found in {js_file}: {api_keys}")
        else:
            print(f"[\033[31m!\033[0m] No exposed API keys found in {js_file}.")



# full scan


def full(url):
    printt('coming soon...')