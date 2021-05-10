![](logo.png)

# Mini Redis

Redis Clone implemented using python and gevent library. This goal of this project is to understand and implement Communication between client and server over socket. The main objective was to how to serialize and deserialize the  data and handle it in proper manner over socket.



### What is Gevent?

Synchronous programming can only do one thing at a time. So while a database query is running, everyone else (say pulling up a webpage via a web framework) has to wait for that to finish. 

Gevent makes it Asynchronous by using context switching and events. What does this mean? Think of it like this. You have a queue with stuff waiting for things to happen, meanwhile gevent says, ok you can wait, I am going to move to the next task and start doing stuff while I am waiting for you to finish (like a database read, or waiting for user input) and when you are done, when I go back through my queue and you say you're ready for the next step, I focus on that for you. 

In this way, though still single threaded, the application can be switching between jobs super fast, constantly checking the status to see if it deserves focus or not, meanwhile, other things can get done while it waits for you. 

As opposed to multiple threads, that are handled by the OS and heavy, they require their own resources and are expensive to switch between. 

Gevent makes converting stuff that would normally use threading to greenlets easy.

[source: https://stackoverflow.com/questions/49669212/what-is-greenlet](https://stackoverflow.com/questions/49669212/what-is-greenlet)



### How are greenlets different from threads?

Threads (in theory) are preemptive and parallel [1](https://greenlet.readthedocs.io/en/latest/#f1), meaning that multiple threads can be processing work at the same time, and it’s impossible to say in what order different threads will proceed or see the effects of other threads. This necessitates careful programming using [`locks`](https://docs.python.org/3/library/threading.html#threading.Lock), [`queues`](https://docs.python.org/3/library/queue.html#queue.Queue), or other approaches to avoid [race conditions](https://en.wikipedia.org/wiki/Race_condition), [deadlocks](https://docs.microsoft.com/en-us/troubleshoot/dotnet/visual-basic/race-conditions-deadlocks#when-deadlocks-occur), or other bugs.

In contrast, greenlets are cooperative and sequential. **This means that when one greenlet is running, no other greenlet can be running;** the programmer is fully in control of when execution switches between greenlets. This can eliminate race conditions and greatly simplify the programming task.

Also, threads require resources from the operating system (the thread stack, and bookkeeping in the kernel). Because greenlets are implemented entirely without involving the operating system, they can require fewer resources; it is often practical to have many more greenlets than it is threads.

[source :https://greenlet.readthedocs.io/en/latest/](https://greenlet.readthedocs.io/en/latest/)



### What is StreamServer?

StreamServer is generic TCP server.

Accepts connections on a listening socket and spawns user-provided *handle* function for each connection with 2 arguments: the `client socket` and the `client address`.

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