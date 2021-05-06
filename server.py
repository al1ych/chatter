import socket
import time
import os

host = socket.gethostbyname(socket.gethostname())
# port = 9092
port = os.environ.get("PORT", 9092)
port = int(port)

clients = []

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, port))

quitCondition = False
print("[ Server Started ]")

while not quitCondition:
  try:
    data, addr = sock.recvfrom(1024)

    if addr not in clients:
      clients.append(addr)

    currentTime = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())

    print("[" + addr[0] + "]=[" + str(addr[1]) + "]=[" + currentTime + "]/", end="")
    print(data.decode("utf-8"))

    for client in clients:
      if addr != client:
        sock.sendto(data, client)
  except:
    print("\n[ Server Stopped ]")
    quitCondition = True

sock.close()
