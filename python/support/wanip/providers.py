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

"""Wrap 'public providers for WANIP' in a data structure with convenience operations

It is really our interpretation that those be labelled thusly...
"""

import random

from support.lsattr import LsAttr

__all__ = [
    'Public_Providers',
]

class Providers(LsAttr):

    def __init__(self, *providers):
        """Store the providers in a tuple

        This feels more natural than, say, a list or a set; although we will resort to the former
        and emulate semantix of the latter below.
        """
        self.providers = tuple(providers)

    def __call__(self):
        """Gimme any one"""

        try:
            assert len(self.providers) >= 1
        except AssertionError as exc:
            raise ValueError('no element found in collection') from exc

        return random.choice(self.providers)

    def __add__(self, provider):
        """Augment the collection

        As tuples are immutable, we temporarily escape to lists.  We do not allow an element to be
        added more than once.

        We do not return a new instance, as this would wrap a tuple in a tuple.
        """
        try:
            assert provider not in self.providers
        except AssertionError as exc:
            raise ValueError(f'"{provider}" is already part of the collection') from exc

        _ = list(self.providers)
        _.append(provider)
        self.providers = tuple(_)
        return self

    def __sub__(self, provider):
        """Diminish the collection

        Again, we resort to lists while doing the job.

        And again, we do not return a new instance, as this would wrap a tuple in a tuple.
        """
        _ = list(self.providers)

        try:
            _.remove(provider)
        except ValueError as exc:
            raise ValueError(f'"{provider}" is not part of the collection') from exc

        self.providers = tuple(_)
        return self

    def __len__(self):
        """Tell the size of the collection"""

        return len(self.providers)

    def __contains__(self, provider):
        """Test for membership"""

        return provider in self.providers

    def __iter__(self):
        """Make the collection iterable/usable in generators"""

        for provider in self.providers:
            yield provider

# Export this
Public_Providers = Providers(*public_providers)

if __name__ ==  '__main__':
    """Self test code"""

    import pytest

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
    print('Here is a public provider:', Public_Providers(), end='\n\n')

    # Cannot remove non-existing element
    with pytest.raises(ValueError):
        Public_Providers = Public_Providers - 'non-existing element'

    # Cannot add an element more than once
    with pytest.raises(ValueError):
        Public_Providers = Public_Providers + 'an element' + 'an element'

    print('Here are all ', len(Public_Providers), ' current public providers:\n',
          '\n'.join(' ' * 4 + str(provider) for provider in Public_Providers), sep='')

    # Cannot obtain a provider from an empty collection
    Public_Providers = Providers()
    with pytest.raises(ValueError):
        print(Public_Providers())
