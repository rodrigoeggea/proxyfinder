#!/usr/bin/env python3
from concurrent.futures import ThreadPoolExecutor, wait, as_completed
import urllib.request
import urllib.parse
import requests
import json
import os
import sys
from pprint import pprint
import time

def truncate(number, decimals=0):
    multiplier = 10 ** decimals
    return int(number * multiplier) / multiplier
    
class Proxy:
    def __init__(self,ip,port,anon,country,iso):
        self.ip=ip
        self.port=str(port)
        self.anon=anon
        self.country=country
        self.iso=iso
        self.valid=''        
        self.delay=''
        self.ipport=f'{self.ip}:{self.port}'
        
    def __repr__(self):
        return('%-22s %-15s %-10.2s %-5s \n' % (
                self.ipport, self.country, self.delay, self.valid))
        
        
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

def get_proxy_list():
    try: 
        url = 'https://www.proxy-list.download/api/v0/get?l=en&t=http'
        r = requests.get(url)
        json_lst = r.json()
        #pprint(json)
        DICT      = json_lst[0]
        UPDATED   = DICT.get('UPDATED')
        UPDATEDAV = DICT.get('UPDATEDAV')
        TOTAL     = DICT.get('TOTAL')
        PAISES    = DICT.get('PAISES')
        LISTA     = DICT.get('LISTA')
        return LISTA
    except: 
        print('Não foi possível baixar lista de proxies...')
        exit()
#######################################
#  MAIN
#######################################

if __name__ == '__main__':
   
    # Busca lista de proxy da internet
    LISTA = get_proxy_list()  

    # CARREGA LISTA DE PROXIES
    proxylist = list()
    for server in LISTA:
        proxy = Proxy(
            server.get('IP'),
            server.get('PORT'),
            server.get('ANON'),
            server.get('COUNTRY'),
            server.get('ISO'))
        proxylist.append(proxy)
        
    # TESTA OS PROXIES
    print('------------------------')
    print(f'Testando proxies...    ')  
    print('------------------------')    
    
    futures = []
#    with ThreadPoolExecutor(max_workers=10) as pool:
#        for proxy in proxylist[0:10]:    
#            future.append(pool.submit(proxy_validate,proxy))
    
    pool = ThreadPoolExecutor(max_workers=20)
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
    print(f' TOTAL DE PROXIES:   {len(proxylist)}')
    print(f' PROXIES FUNCONANDO: {len(proxyvalid)}')
    
    file = open('proxylist.txt','w+')
    for proxy in sortedbydelay:
        file.write(f'{proxy.ipport} \n')    
    file.close()
    
    print('---------------------------------')
    print('  ARQUIVO SALVO: proxylist.txt   ')
    print('---------------------------------')