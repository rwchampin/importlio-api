import requests, random


# custom proxy manager class to manage proxy rotation
class ProxyManager:
    def __init__(self):
        self.username = "geonode_y52krAfiwj-country-US"
        self.password = "685d0e68-e072-473e-86c0-beae004f73e3"
        self.geonode_dns = f"rotating-residential.geonode.com:{self.get_random_port()}"
        self.create_proxy()

    def create_proxy(self):
        proxy = "http://{}:{}@{}".format(self.username, self.password, self.geonode_dns)
        proxies = {
            "http": proxy,
            "https": proxy
        }
        response=requests.get("http://httpbin.org/ip", proxies=proxies)

        if response.status_code == 200:
            return proxies
        else:
            return False
    
    def get_random_port(self):
        return random.randint(9000, 9010)