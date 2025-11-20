# rpc_client_single.py
import xmlrpc.client
import sys

cid = sys.argv[1]  # get client ID
proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

print(f"\n==== CLIENT {cid} Running ====\n")

tasks = [
    ("add", [10, 5]),
    ("sort", [5, 3, 9, 1]),
    ("reverse", "client" + cid),
    ("uppercase", "hello rpc")
]

for t, data in tasks:
    print(f"[CLIENT {cid}] → Sending {t}: {data}")
    result = proxy.execute_task(t, data)
    print(f"[CLIENT {cid}] ← Result:", result)



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