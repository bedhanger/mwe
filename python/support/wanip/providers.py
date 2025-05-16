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

    def __init__(self, *pargs):
        self.providers = tuple(pargs)

    def __call__(self):
        return random.choice(self.providers)

    def __add__(self, another):
        _ = list(self.providers)
        _.append(another)
        self.providers = tuple(_)
        return self

    def __sub__(self, one):
        _ = list(self.providers)
        _.remove(one)
        self.providers = tuple(_)
        return self

    def __len__(self):
        return len(self.providers)

    def __contains__(self, provider):
        return provider in self.providers

Public_Providers = Providers(*public_providers)

if __name__ ==  '__main__':

    print('There are currently', len(Public_Providers), 'public providers')
    print('"my machine" is in Public_Providers? ', "my machine" in Public_Providers)
    print('This is what Public_Providers is internally:', Public_Providers)
    print('Here is a public provider:', Public_Providers(), end='\n\n')

    print('There are currently', len(Public_Providers), 'public providers')
    print('"https://ifconfig.me/ip" is in Public_Providers? ', "https://ifconfig.me/ip" in Public_Providers)
    print('This is what Public_Providers is internally:', Public_Providers)
    print('Here is a public provider:', Public_Providers(), end='\n\n')

    Public_Providers = Providers(1, 2, 3, 4, 5, 6)
    print('There are currently', len(Public_Providers), 'public providers')
    print('6 is in Public_Providers? ', 6 in Public_Providers)
    print('This is what Public_Providers is internally:', Public_Providers)
    print('Here is a public provider:', Public_Providers(), end='\n\n')

    Public_Providers = Public_Providers + 42
    print('There are currently', len(Public_Providers), 'public providers')
    print('4 is in Public_Providers? ', 42 in Public_Providers)
    print('This is what Public_Providers is internally:', Public_Providers)
    print('Here is a public provider:', Public_Providers(), end='\n\n')

    Public_Providers = Public_Providers + 'foo'
    print('There are currently', len(Public_Providers), 'public providers')
    print('\'foo\' is in Public_Providers? ', 'foo' in Public_Providers)
    print('This is what Public_Providers is internally:', Public_Providers)
    print('Here is a public provider:', Public_Providers(), end='\n\n')

    Public_Providers = Public_Providers + "bar"
    print('There are currently', len(Public_Providers), 'public providers')
    print('"baz" is in Public_Providers? ', "baz" in Public_Providers)
    print('This is what Public_Providers is internally:', Public_Providers)
    print('Here is a public provider:', Public_Providers(), end='\n\n')

    Public_Providers = Public_Providers + "zonk" + 'baz'
    print('There are currently', len(Public_Providers), 'public providers')
    print('"baz" is in Public_Providers? ', "baz" in Public_Providers)
    print('This is what Public_Providers is internally:', Public_Providers)
    print('Here is a public provider:', Public_Providers(), end='\n\n')

    Public_Providers = Public_Providers - "zonk" - 3
    print('There are currently', len(Public_Providers), 'public providers')
    print('3 is in Public_Providers? ', 3 in Public_Providers)
    print('This is what Public_Providers is internally:', Public_Providers)
    print('Here is a public provider:', Public_Providers(), end='\n\n')

    Public_Providers = Public_Providers - 4
    print('There are currently', len(Public_Providers), 'public providers')
    print('4 is in Public_Providers? ', 4 in Public_Providers)
    print('This is what Public_Providers is internally:', Public_Providers)
    print('Here is a public provider:', Public_Providers())
