#!/usr/bin/env python3
from concurrent.futures import ThreadPoolExecutor, wait, as_completed
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import requests
import json
import os
import sys
from pprint import pprint
import time
from Proxy import Proxy
from FoxyProxy import *

def truncate(number, decimals=0):
    multiplier = 10 ** decimals
    return int(number * multiplier) / multiplier       
        
def proxy_validate(proxy):
    proxy_address = 'http://' + proxy.ipport
    proxies = { 'http': proxy_address, 'https': proxy_address }    
    try:
        start = time.time()
        r = requests.get('https://ip.seeip.org/jsonip?', proxies=proxies, timeout=30)     
        response = r.text.strip()
        end = time.time()
        delay = truncate((end-start),2)
        if 'ip' in response:
            #print(f'Proxy {proxy.ipport} OK.')
            proxy.valid=True
            proxy.delay=delay
    except:              
        proxy.valid=False
        pass
        # print( e = sys.exc_info()[0])
        #print(f'Proxy {proxy.ipport} not working.')


def get_proxy_from_free_proxy(): 
    url = 'https://free-proxy-list.net/'
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    page = request = requests.get(url, headers=header)
    soup = BeautifulSoup(page.text, 'html.parser')
    table = soup.find('table')
    tbody = table.find('tbody')
    rows = tbody.find_all('tr')
    proxyset = set()  
    for row in rows:
        cols = row.find_all('td')
        ip  =cols[0].text
        port=cols[1].text
        code=cols[2].text
        country=cols[3].text
        anon=cols[4].text
        https=cols[6].text
        time=cols[7].text
        if https== 'no':
            proxy = Proxy(ip,port,anon,country,'')  # ip, port, anon, country, iso
            proxyset.add(proxy)
    return list(proxyset)     

def get_proxy_from_clarketm():
    try:
        url='https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt'
        txtlist = requests.get(url).text
    except:
        print('Não foi possível baixar lista de proxies do Clark...')
        exit()
    else:
        proxyset = set()
        lista = txtlist.split()
        for proxy in lista:
            ip = proxy.split(':')[0]
            port = proxy.split(':')[1]
            proxy = Proxy(ip,port,'','','')
            proxyset.add(proxy)
        return list(proxyset)   # set não tem indice, melhor converter em lista
        
def get_proxy_list():
    try: 
        url = 'https://www.proxy-list.download/api/v0/get?l=en&t=http'
        request = requests.get(url)
        json_lst = request.json()
    except: 
        print('Não foi possível baixar lista de proxies...')
        exit()
        
    #pprint(json)
    DICT      = json_lst[0]
    UPDATED   = DICT.get('UPDATED')
    UPDATEDAV = DICT.get('UPDATEDAV')
    TOTAL     = DICT.get('TOTAL')
    PAISES    = DICT.get('PAISES')
    LISTA     = DICT.get('LISTA')
        
    # CARREGA LISTA DE PROXIES
    # RETORNA UMA LISTA DE OBJETOS
    proxyset = set()
    for server in LISTA:
        proxy = Proxy(server.get('IP'),server.get('PORT'),
                      server.get('ANON'), server.get('COUNTRY'), server.get('ISO'))
        #print('adicionado=',proxy)s
        proxyset.add(proxy)  
    return list(proxyset)

#######################################
#             MAIN
#######################################
if __name__ == '__main__':

    # Busca lista de proxy da internet
    #proxylist = get_proxy_list()
    #proxylist = get_proxy_list_clarketm()
    proxylist = get_proxy_from_free_proxy()

    # TESTA OS PROXIES
    print('------------------------')
    print('Testando proxies...     ')  
    print('------------------------')    
    print('Total=',len(proxylist))

    # Cria um Pool de Threads para testar em paralelo
    futures = []
    pool = ThreadPoolExecutor(max_workers=50)
    for proxy in proxylist:
        futures.append(pool.submit(proxy_validate,proxy))
        
    completados=0
    for x in as_completed(futures):
        completados+=1
        total=len(futures)
        print('Completado: %3d %% \r' % (completados/total*100),end='')    
    print('------------------------------------------------------------------')  
    
    # Mostra todos proxy organizado por delay
    proxyvalid = [p for p in proxylist if p.valid == True]
    sortedbydelay = sorted(proxyvalid, key=lambda proxy: proxy.delay)  
    #print(sortedbydelay)
    
    for proxy in sortedbydelay:
        print('%-22s %-15s %6.2f ms   %-5s' % 
             (proxy.ipport, proxy.country, proxy.delay, proxy.anon))
    
    print('------------------------------------------------------------------')  
    print(f' PROXIES FUNCIONANDO: {len(proxyvalid)} / {len(proxylist)} ')
    
    file = open('proxylist.txt','w+')
    for proxy in sortedbydelay:
        file.write(f'{proxy.ipport} \n')    
    file.close()
    
    print('---------------------------------')
    print('  ARQUIVO SALVO: proxylist.txt   ')
    print('---------------------------------')
    
    foxyproxy = FoxyProxy()
    for proxy in sortedbydelay:
        proxyData = ProxyData()
        proxyData.title = proxy.ipport
        proxyData.address = proxy.ip
        proxyData.port = proxy.port
        foxyproxy.add_proxy(proxyData)
    foxyproxy.save()
    print('---------------------------------')
    print('  ARQUIVO SALVO: FoxyProxy.json  ')
    print('---------------------------------')

        
        
    
    
    
    
