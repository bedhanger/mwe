public_providers = [
    'https://ifconfig.me/ip',
    'https://my.ip.fi',
    'https://icanhazip.com',
    'https://ifconfig.co',
    'https://ipecho.net/plain',
    'https://ipinfo.io/ip',
    'https://ident.me',
    'https://iprs.fly.dev',
    'https://l2.io/ip',
    'https://ipapi.co/ip',
    'https://wgetip.com',
    'https://whatismyip.akamai.com',
    'https://eth0.me/',
    'https://api.ipify.org',
    'https://ip.me',
    'https://checkip.amazonaws.com',
    'https://www.trackip.net/ip',
]

import random

from support.lsattr import LsAttr

class Providers(LsAttr):

    def __init__(self, public_providers=public_providers):
        self.public_providers = public_providers

    def __call__(self) -> str:
        return random.choice(self.public_providers)

Public_Providers = Providers()

if __name__ ==  '__main__':

    print(Public_Providers)

    print(Public_Providers())
