from io import BytesIO
from socket import error as SocketError
from collections import namedtuple

Error = namedtuple('Error',('message',))

class CommandError(Exception): pass;
class Disconnect(Exception): pass;

class ProtocolHandler:
    def __init__(self):
        self._handler = {
                '+':self.handle_simple_string,
                '-':self.handle_error,
                ':':self.handle_int,
                '$':self.handle_string,
                '*':self.handle_array,
                '%':self.handle_dict,
                }
    def handle_req(self,socketFile):
        fb = socketFile.read(1).decode('utf-8')
        if not fb:
            raise Disconnect()
        try:
            return self._handler[fb](socketFile)
        except KeyError:
            raise CommandError('Bad Request')

    def write_response(self,socketFile,data):
        buf = BytesIO()
        self._write(buf,data)
        buf.seek(0)
        socketFile.write(buf.getvalue())
        socketFile.flush()

    def _write(self,buf,data):
        if isinstance(data,(str,bytes)):
            serialized_data = bytes('$%s\r\n%s\r\n'%(len(data),data),'utf-8')
            buf.write(serialized_data)
        elif isinstance(data,int):
            serialized_data = bytes(':%s\r\n'%(data),'utf-8')
            buf.write(serialized_data)
        elif isinstance(data,(list,tuple)):
            serialized_data = bytes('*%s\r\n'%(len(data)),'utf-8')
            buf.write(serialized_data)
            for itm in data:
                self._write(buf,itm)
        elif isinstance(data,dict):
            serialized_data = bytes('%%s\r\n'%(len(data)),'utf-8')
            buf.write(serialized_data)
            for k,v in data:
                self._write(buf,k)
                self._write(buf,v)
        elif isinstance(data,Error):
            serialized_data = bytes('-%s\r\n'%(data.message),'utf-8')
            buf.write(serialized_data)
        elif data is None:
            buf.write(b'$-1\r\n')
        else:
            raise CommandError('Unrecognized Command : %s'% type(data))

    def handle_simple_string(self,socketFile):
        return socketFile.readline().decode('utf-8').rstrip('\r\n')

    def handle_int(self,socketFile):
        return int(socketFile.readline().decode('utf-8').rstrip('\r\n'))

    def handle_string(self,socketFile):
        sz = int(socketFile.readline().decode('utf-8').rstrip('\r\n'))
        if sz==-1:
            return None
        sz+=2
        return socketFile.read(sz).decode('utf-8')[:-2]

    def handle_array(self,socketFile):
        num_elm = int(socketFile.readline().decode('utf-8').rstrip('\r\n'))
        arr = []
        for _ in range(num_elm):
            x = self.handle_req(socketFile)
            arr.append(x)
        return arr
    def handle_dict(self,socketFile):
        num_elm = int(socketFile.readline().decode('utf-8').rstrip('\r\n'))
        arr = []
        for _ in range(num_elm*2):
            x= self.handle_req(socketFile)
            arr.append(x)
        return dict(zip(arr[::2],arr[1::2]))

    def handle_error(self,socketFile):
        return Error(socketFile.readline().decode('utf-8').rstrip('\r\n'))


