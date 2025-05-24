import requests 
import socket
import urllib3


def hostname_resolves(domain):
    try:
        socket.gethostbyname(domain)
        return 1
    except: 
        return 0

def get_site_status(domain, protocol, verify=True): 
    """Request the site

    verfiy -> We need this for example when we whant to prevent ssl errors

    """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    try:
        req = requests.get(f"{protocol}://{domain}", verify=verify) # Verify False is used to prevent errors from untrused certificates 
        return req.status_code
    except:
        return None


def check_domains(domain_list):
    for domain_entry in domain_list: 
        print(f"\nChecking {domain_entry}")

        if hostname_resolves(domain_entry):


            ## Check HTTP 
            try: # I use "try" because sites that do not allow a redirect from http to https may throw a error" 
                http_status = get_site_status(domain_entry, "http")
                if http_status == None: ## Error (e.g. SSL Verification fails)  
                    http_status = get_site_status(domain_entry, protocol="http", verify=False)

                print(f"\t{domain_entry} -> http -> Status: {http_status}")

            except: 
                print(f"\t{domain_entry} -> http -> not possible")


            # Check HTTPs 
            try:
                https_status = get_site_status(domain_entry, "https")

                if https_status == None: # e.g (SSL error)  
                    https_status = get_site_status(domain_entry, "https", verify=False)

                print(f"\t{domain_entry} -> https -> Status: {https_status}")
            except: 
                print(f"\t{domain_entry} -> https -> possible")
                
        else: 
            print(f"\t{domain_entry} does not resolve")


def build_domain_list(base_domain, subdomains):
    full_domains = []
    for domain in subdomains: 
        full_domains.append(f"{domain}.{base_domain}")

    return full_domains




if __name__ == '__main__':
    print("Welcome to Netwolf") 
    

    with open ('./wordlists/subdomains.txt') as file: 
        subdomains = file.read().splitlines()


    domain_list = build_domain_list("kaufbeuren.de", subdomains)
        
    check_domains(domain_list)



