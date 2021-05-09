from gevent.pool import Pool
from gevent.server import StreamServer
from Protocol import ProtocolHandler,CommandError,Disconnect,Error


class Server:
    def __init__(self,host='127.0.0.1',port=4000,max_clients=64):
        self._pool = Pool(max_clients)
        self._server = StreamServer((host,port),self.connection_handler,spawn=self._pool)
        self._protocol = ProtocolHandler()
        self._kv = {}
        self._commands = self.get_commands()

    def run(self):
        self._server.serve_forever()

    def get_commands(self):

        return {
                'GET':self.get,
                'SET':self.set,
                'DELETE':self.delete,
                'FLUSH':self.flush,
                'MGET':self.mget,
                'MSET':self.mset
                }

    def connection_handler(self,conn,address):
        socketFile = conn.makefile('rwb')

        while True:
            try:
                data = self._protocol.handle_req(socketFile)
            except Disconnect:
                break

            try:
                res = self.get_response(data)
            except CommandError as exe:
                res = Error(exe.args(0))


            self._protocol.write_response(socketFile,res)

    def get_response(self,data):
        if not isinstance(data,list):
            try:
                data = data.split()
            except:
                raise CommandError('Request must be list or string')
        if not data:
            raise CommandError('Missing Command')

        cmd = data[0].upper()
        if cmd not in self._commands:
            raise CommandError(f'Invlaid Command: {cmd}')
            
        return self._commands[cmd](*data[1:])

    def get(self,key):
        return self._kv.get(key)

    def set(self,key,val):
        self._kv[key]=val
        return 1

    def delete(self,key):
        if key in self._kv:
            del self._kv[key]
            return 1
        return 0

    def flush(self):
        sz = len(self._kv)
        self._kv.clear()
        return sz

    def mget(self,*keys):
        return [self._kv[k] for k in keys]

    def mset(self,*items):
        data = zip(items[::2],items[1::2])
        for k,v in data:
            self._kv[k]=v
        return len(data)


if __name__ == '__main__':
    from gevent import monkey
    monkey.patch_all()
    port = 4000
    Server(port=port).run()
    print(f"Server Started on Port: {port}")
