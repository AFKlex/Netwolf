import socket
import requests
import urllib3


class Domain: 
    def __init__(self, domain:str, status_code=None) -> None:
        """
        Create a domain object.
        """
        self.domain = domain 
        self.subdomains = []
        self.directories = []
        self.status_code = status_code

    def add_subdomain(self, domain:str, status_code:int) -> None:
        """
        Add the subdomain to the directory of valid subdomains
        """
        domain = domain.strip()

        self.subdomains.append(Domain(domain, status_code))



    def get_domain(self) -> str:
        return self.domain

    def resolve_hostname(self, domain) -> bool:
        try:
            socket.gethostbyname(domain)
            return True 
        except: 
            return False 

    def get_site_status(self, domain, protocol,verify=True) ->int:     
        """Request the site

        verfiy -> We need this for example when we whant to prevent ssl errors

        Returns:
            int: HTTP status code if request is successful, -1 otherwise.

        """
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        try:
            req = requests.get(f"{protocol}://{domain}", verify=verify) # Verify False is used to prevent errors from untrused certificates 
            return req.status_code
        except:
            return -1


    def fuzz_subdomains(self, sub_domain_list:list) -> None:
        """
        Fuzz the domains and add each found domain to the subdomain list 
        """
        for subdomain in sub_domain_list: 
            subdomain = f"{subdomain}.{self.get_domain()}"
            print(f"\nChecking {subdomain}")

            if self.resolve_hostname(subdomain):
                http_status = None 
                https_status = None 

                ## Check HTTP 
                try: # I use "try" because sites that do not allow a redirect from http to https may throw a error" 
                    http_status = self.get_site_status(subdomain, "http")
                    if http_status == -1: ## Error (e.g. SSL Verification fails)  
                        http_status = self.get_site_status(subdomain, protocol="http", verify=False)


                    print(f"\t{subdomain} -> http -> Status: {http_status}")

                except: 
                    print(f"\t{subdomain} -> http -> not possible")


                # Check HTTPs 
                try:
                    https_status = self.get_site_status(subdomain, "https")

                    if https_status == -1: # e.g (SSL error)  
                        https_status = self.get_site_status(subdomain, "https", verify=False)


                    print(f"\t{subdomain} -> https -> Status: {https_status}")
                except: 
                    print(f"\t{subdomain} -> https -> possible")

                if http_status != -1: # If one connection succees add to subdomains 
                    self.add_subdomain(subdomain,http_status)
                    continue

                if https_status != -1: 
                    self.add_subdomain(subdomain,https_status)
                    continue
                    
                    
            else: 
                print(f"\t{subdomain} does not resolve")



