
from django.conf import settings
import random


def random_number_between(min, max):
    return random.randint(min, max)

def get_random_proxy_port():
    num = random_number_between(0, 10)    
    
    # if num is 1 digit, add a 0 to the front
    if num < 10:
        num = "0" + str(num)
        
    return num

GEONODE_DNS = f"rotating-residential.geonode.com:90{get_random_proxy_port()}"

def get_proxy():
    return {"http":"http://{}:{}@{}".format("geonode_y52krAfiwj-country-US", "685d0e68-e072-473e-86c0-beae004f73e3", GEONODE_DNS)}
