#!/usr/bin/env python3
import urllib.request
import urllib.request
import urllib.parse
import requests
import json
import _thread
import concurrent.futures
import os
import sys
from pprint import pprint
from collections import namedtuple
import time
from types import SimpleNamespace as Namespace
from tabulate import tabulate

def truncate(number, decimals=0):
    multiplier = 10 ** decimals
    return int(number * multiplier) / multiplier
    
class MeuLog:
    __instance = None
    @staticmethod
    def getInstance(filename):
        if MeuLog.__instance == None:
            MeuLog(filename)
        return MeuLog.__instance
    def __init__(self,filename):
        self.f=''
        if MeuLog.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            if not self.f: 
                self.f = open(filename, 'w+')
            MeuLog.__instance = self
    def write(self,string):
        self.f.write(string)
    def __self__(self):
        self.f.close()
        
def proxy_test(ip,port,proxylist):
    proxy_address = 'http://' + ip + ':' + str(port)
    proxies = { 'http': proxy_address, 'https': proxy_address}    
    try:
        start = time.time()        
        r = requests.get('https://ip.seeip.org/jsonip?', proxies=proxies, timeout=10)        
        response = r.text.strip()
        end = time.time()
        delay = truncate((end-start),2)
        if 'ip' in response:
            print(f'{ip}:{port}\t{delay}')
            proxylist.append(f'{ip}:{port}     {delay}ms')
            return True
        else:
            return False
    except:       
        #print( e = sys.exc_info()[0])
        # print('Erro')
        return False

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
        exit
        return None


#######################################
#  MAIN
#######################################

if __name__ == '__main__':
   
    LISTA = get_proxy_list()  
    print('------------------------')
    print(f'Testando proxies...')  
    print('------------------------')
        
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        proxylist = list()
        for server in LISTA:
            IP      = server.get('IP')
            PORT    = server.get('PORT')
            ANON    = server.get('ANON') 
            COUNTRY = server.get('COUNTRY') 
            ISO     = server.get('ISO')
            TYPE    = server.get('TYPE')
            executor.submit(proxy_test,IP,PORT,proxylist)
    # Aguarda terminar os processos
    executor.shutdown(wait=True)
    
    print('---------------------------------')
    print(f' TOTAL DE PROXIES= {len(LISTA)}')
    print(f' PROXIES OK= {len(proxylist)}')
    with open('proxylist.txt', mode='wt', encoding='utf-8') as myfile:
        myfile.write('\n'.join(proxylist))
    print('---------------------------------')
    print('  ARQUIVO SALVO: proxylist.txt   ')
    print('---------------------------------')

    

