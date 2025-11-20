# rpc_client.py
import xmlrpc.client
from threading import Thread
import random
import time

def worker(cid):
    # Each thread has its own connection
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000/", allow_none=True)

    tasks = ["add", "sort", "reverse", "uppercase"]

    for _ in range(4):
        t = random.choice(tasks)

        if t == "add":
            data = [cid, random.randint(1, 10)]
        elif t == "sort":
            data = [random.randint(1, 50) for _ in range(5)]
        elif t == "reverse":
            data = "client" + str(cid)
        else:
            data = "hello rpc"

        print(f"[CLIENT {cid}] Sending {t}")
        result = proxy.execute_task(t, data)
        print(f"[CLIENT {cid}] Result:", result)

        time.sleep(0.2)

# Launch threads
threads = []
for i in range(1, 6):
    t = Thread(target=worker, args=(i,), daemon=False)
    t.start()
    threads.append(t)

# Wait for all threads to finish (program ends immediately after)
for t in threads:
    t.join()

print("\n✅ All client threads finished. Exiting cleanly.\n")


'''Rpc

Single server single client multiple threads
python rpc_server.py
Python rpc_client.py

Multiple terminals clients:
python rpc_server.py
python rpc_client_single.py 1
python rrpc_client_single.py 2



Grpc
pip install grpcio grpcio-tools

python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. Codeexec.proto\
After these 2 files will be generated - we only write proto , client and server files

Single server single client multiple threads
python grpc_server.py
Python grpc_client.py

Multiple terminals clients:
python grpc_server.py
python grpc_client_single.py 1
python grpc_client_single.py 2
'''