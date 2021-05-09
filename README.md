# Mini Redis

Redis Clone iplemented using python and gevent library. This goal of this project is to understand and implement Communication between client and server over socket. The main objective was to how to serialize and deserialize the  data and handle it in proper manner.


# To Run the code

1. Create a virtual environment `python -m venv myenv`
2. Activate the environment `source myenv/bin/activate`
3. Install all the packages `pip install -r requirement.txt`
4. Run the server `python server.py`
5. create a client program 

```py
#Client Program 

from client import Client

host = "127.0.0.1"
port = 4000
cl = Client(host,port)
cl.set("name","Robbin Hood")
cl.get("name")
cl.flush()

```

# Tips To Debug

To debug serialization you can start a local server using netcat `nc -l 4000` this will start a server on port 4000 now using your client you can send the data. The serialized data will be shown on your stdin. This helped me debug my serialization.