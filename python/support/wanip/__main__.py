"""Self test code"""

import pytest

from . import Providers, Public_Providers

print('There are currently', len(Public_Providers), 'public providers')
print('"my machine" is in Public_Providers? ', "my machine" in Public_Providers)
print('This is what Public_Providers is internally:', repr(Public_Providers))
print('The public providers:'); print(Public_Providers)
print('Here is a public provider:', Public_Providers(), end='\n\n')

print('There are currently', len(Public_Providers), 'public providers')
print('"https://ifconfig.me/ip" is in Public_Providers? ', "https://ifconfig.me/ip" in Public_Providers)
print('This is what Public_Providers is internally:', repr(Public_Providers))
print('The public providers:'); print(Public_Providers)
print('Here is a public provider:', Public_Providers(), end='\n\n')

Public_Providers = Providers(1, 2, 3, 4, 5, 6)
print('There are currently', len(Public_Providers), 'public providers')
print('6 is in Public_Providers? ', 6 in Public_Providers)
print('This is what Public_Providers is internally:', repr(Public_Providers))
print('The public providers:'); print(Public_Providers)
print('Here is a public provider:', Public_Providers(), end='\n\n')

Public_Providers = Public_Providers + 42
print('There are currently', len(Public_Providers), 'public providers')
print('4 is in Public_Providers? ', 42 in Public_Providers)
print('This is what Public_Providers is internally:', repr(Public_Providers))
print('The public providers:'); print(Public_Providers)
print('Here is a public provider:', Public_Providers(), end='\n\n')

Public_Providers = Public_Providers + 'foo'
print('There are currently', len(Public_Providers), 'public providers')
print('\'foo\' is in Public_Providers? ', 'foo' in Public_Providers)
print('This is what Public_Providers is internally:', repr(Public_Providers))
print('The public providers:'); print(Public_Providers)
print('Here is a public provider:', Public_Providers(), end='\n\n')

Public_Providers = Public_Providers + "bar"
print('There are currently', len(Public_Providers), 'public providers')
print('"baz" is in Public_Providers? ', "baz" in Public_Providers)
print('This is what Public_Providers is internally:', repr(Public_Providers))
print('The public providers:'); print(Public_Providers)
print('Here is a public provider:', Public_Providers(), end='\n\n')

Public_Providers = Public_Providers + "zonk" + 'baz'
print('There are currently', len(Public_Providers), 'public providers')
print('"baz" is in Public_Providers? ', "baz" in Public_Providers)
print('This is what Public_Providers is internally:', repr(Public_Providers))
print('The public providers:'); print(Public_Providers)
print('Here is a public provider:', Public_Providers(), end='\n\n')

Public_Providers = Public_Providers - "zonk" - 3
print('There are currently', len(Public_Providers), 'public providers')
print('3 is in Public_Providers? ', 3 in Public_Providers)
print('This is what Public_Providers is internally:', repr(Public_Providers))
print('The public providers:'); print(Public_Providers)
print('Here is a public provider:', Public_Providers(), end='\n\n')

Public_Providers = Public_Providers - 4
print('There are currently', len(Public_Providers), 'public providers')
print('4 is in Public_Providers? ', 4 in Public_Providers)
print('This is what Public_Providers is internally:', repr(Public_Providers))
print('The public providers:'); print(Public_Providers)
print('Here is a public provider:', Public_Providers(), end='\n\n')

# Cannot remove non-existing element
with pytest.raises(ValueError):
    Public_Providers = Public_Providers - 'non-existing element'

# Cannot add an element more than once
with pytest.raises(ValueError):
    Public_Providers = Public_Providers + 'an element' + 'an element'

for _ in range(9):
    print(Public_Providers())
print('>8' * 4)
for _ in range(9):
    print(Public_Providers(use_cached=True))

# Cannot obtain a provider from an empty collection
Public_Providers = Providers()
with pytest.raises(ValueError):
    print(Public_Providers())

# Not even when asking for a cached one
Public_Providers = Providers()
with pytest.raises(ValueError):
    print(Public_Providers(use_cached=not False))

# Test the context manager protocol
with Providers('spam', 'eggs') as P:
    print(P())
with pytest.raises(ValueError):
    # We have left the context (of Providers(...), that is)
    print(P())
