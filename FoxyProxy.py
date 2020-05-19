#!/usr/bin/env python3
from typing import List, Any
import json
#
#  CLASS CRIADA A PARTIR DO JSON https://app.quicktype.io/
#
class WhitePattern:
    title: str
    active: bool
    pattern: str
    type: int
    protocols: int

    def __init__(self, title: str = 'all URLs', active: bool = True, pattern: str = '*',
                 type: int =1, protocols: int =1) -> None:
        self.title = title
        self.active = active
        self.pattern = pattern
        self.type = type             # 1=Wildcard, 2=Regexp
        self.protocols = protocols   # 1=all, 2=http, 3=https
    
class BlackPattern:
    title: str
    pattern: str
    type: int
    protocols: int
    active: bool

    def __init__(self, title: str = 'LocalDirect', 
                 pattern : str ='127.0.0.1,192.168.*.*', 
                 type:int =1,         # 1=Wildcard, 2=Regexp
                 protocols: int=1,     # 1=all, 2=http, 3=https
                 active: bool =True ) -> None:
        self.title = title
        self.pattern = pattern
        self.type = type
        self.protocols = protocols
        self.active = active

class ProxyData:
    counter = 0
    type: int
    color: str
    title: str
    active: bool
    address: str
    port: int
    proxy_dns: bool
    username: str
    password: str
    whitePatterns: List[WhitePattern]
    blackPatterns: List[Any]
    pac_url: str
    index: int

    def __init__(self, type: int=1, color: str='#66cc66', title: str = '',  active: bool = True, address: str = '0.0.0.0', port: int = 3289, 
                 proxy_dns: bool = False, username: str = '', password: str = '', 
                 whitePatterns: List[WhitePattern] = None, blackPatterns: List[Any] = None, 
                 pac_url: str = '', index: int = 1 ) -> None:
        self.type   = type
        self.color  = color
        self.title  = title
        self.active = active
        self.address = address
        self.port = port
        self.proxy_dns = proxy_dns
        self.username  = username
        self.password  = password
        self.whitePatterns = list([WhitePattern()])
        self.blackPatterns = list([BlackPattern()])
        self.pac_url = pac_url
        ProxyData.counter+=1
        self._id=ProxyData.counter
        self.index=ProxyData.counter

class Logging:
    size: int
    active: bool

    def __init__(self, size: int = 100, active: bool = False):
        self.size = size
        self.active = active

class FoxyProxy:
#   proxy1: ProxyData   # Vai ser inserido dinamicamente
    logging: Logging
    mode: str
    browserVersion: str
    foxyProxyVersion: str
    foxyProxyEdition: str

    def __init__(self):
        #self.proxy1 = ProxyData()
        self.logging = Logging()
        self.mode = 'disabled'
        self.browserVersion = '77.0'
        self.foxyProxyVersion = '7.4.3'
        self.foxyProxyEdition = 'standard'
        
    def add_proxy(self, proxy_data : ProxyData):
        setattr(self, f'proxy{proxy_data._id}' , proxy_data)

    def __str__(self):
        def skip_private_fields(o):
            for attr in list(o.__dict__):
                if str(attr).startswith('_'):
                    del o.__dict__[str(attr)]
            return o.__dict__
        json_data = str(json.dumps(self, default=skip_private_fields, indent=4))
        return json_data
    
    def save(self):
        file = open('FoxyProxy.json','w+')
        file.write(self.__str__())
        file.close()

#########################################
#         TESTANDO A CLASSE             #
#########################################
if __name__ == '__main__':
    import json

    # Cria um FoxyProxy
    proxy1 = ProxyData()
    proxy1.title = "O MELHOR PROXY"
    proxy1.address = "149.28.44.208"
    proxy1.port = 8080

    proxy2 = ProxyData()
    proxy2.title = "RUIM!!!"
    proxy2.address = "1.2.3.4"
    proxy2.port = 80

    # ADICIONA OS PROXY 
    foxyproxy = FoxyProxy()
    foxyproxy.add_proxy(proxy1)
    foxyproxy.add_proxy(proxy2)

    # MOSTRA NA TELA, E SALVA NO ARQUIVO
    print(foxyproxy)
    foxyproxy.save()
    print('Arquivo salvo: FoxyProxy.json')


