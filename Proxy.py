class Proxy:
    def __init__(self, ip : str = None, port :str = None,
                 anon : str = None, country : str = None,iso : str = None):
        self.ip=str(ip)
        self.port=str(port)
        self.anon=str(anon)
        self.country=str(country)
        self.iso=str(iso)
        self.valid=''        
        self.delay=''
        self.ipport=f'{self.ip}:{self.port}'
        
    def __repr__(self):
        return('%-22s %-15s %-10.2s %-5s \n' % (
                self.ipport, self.country, self.delay, self.valid))
                
    def __eq__(self,other):        
        return (self.ip == other.ip and self.port == other.port)
        
    def __hash__(self):
        return hash(('ip',self.ip,'port',self.port))
        
##################################
# TESTAR A CLASSE
##################################        
if __name__ == '__main__':
    proxy = Proxy('10.1.3.2','8080','transparent','Brazil','')
    
    
