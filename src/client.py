from gevent import socket
from Protocol import ProtocolHandler,CommandError,Disconnect,Error

class Client:
    def __init__(self,host="127.0.0.1",port=4000):
        self._protocol = ProtocolHandler()
        self._socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self._socket.connect((host,port))
        self._fh = self._socket.makefile('rwb')


    def execute(self,*args):
        self._protocol.write_response(self._fh,args)
        resp = self._protocol.handle_req(self._fh)
        if isinstance(resp,Error):
            raise CommandError(resp.message)
        return resp
        
    def get(self,key):
        return self.execute('GET',key)


    def set(self,key,val):
        return self.execute('SET',key,val)

    def delete(self,key):
        return self.execute('DELETE',key)

    def flush(self):
        return self.execute('FLUSH')

    def mget(self,*keys):
        return self.execute('MGET',*keys)

    def mset(self,*items):
        return self.execute('MSET',*items)
