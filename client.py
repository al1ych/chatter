import socket
import threading
import time

shutdown = False
join = False


def receiver(name, sock):
  while not shutdown:
    try:
      while True:
        data, addr = sock.recvfrom(1024)
        print(data.decode("utf-8"), end='\npostgres=# ')
        time.sleep(0.2)
    except:
      pass


# host = socket.gethostbyname(socket.gethostname())
host = socket.gethostbyname('localhost')
port = 0

server = (host, 9092)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(False)

alias = input("alias: ")

receivingThread = threading.Thread(target=receiver, args=("RecvThread", s))
receivingThread.start()

while not shutdown:
  if not join:
    s.sendto((alias + " joined").encode("utf-8"), server)
    join = True
  else:
    try:
      message = input('postgres=# ')
      if message != "":
        s.sendto(("" + alias + "::" + message).encode("utf-8"), server)
      time.sleep(0.2)
    except:
      s.sendto((alias + " left").encode("utf-8"), server)
      shutdown = True

receivingThread.join()
s.close()
