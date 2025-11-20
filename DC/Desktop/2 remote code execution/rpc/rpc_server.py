# rpc_server.py
from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn
import threading

class ThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

print("🚀 RPC Remote Code Execution Server running on port 8000...")

server = ThreadedXMLRPCServer(("localhost", 8000), allow_none=True)

# --------------------------------------
# REMOTE EXECUTION FUNCTION (WITH THREAD PRINTS)
# --------------------------------------
def execute_task(task_type, data):

    # Print current thread handling request
    print(f"[THREAD {threading.get_ident()}] Handling task: {task_type}")

    if task_type == "add":
        x, y = data
        return x + y

    elif task_type == "sort":
        return sorted(data)

    elif task_type == "reverse":
        return data[::-1]

    elif task_type == "uppercase":
        return data.upper()

    else:
        return "❌ Unknown task"

server.register_function(execute_task, "execute_task")

try:
    server.serve_forever()
except KeyboardInterrupt:
    print("\n🛑 Server stopping (Ctrl+C pressed)…")
    server.server_close()
    print("✅ Server closed cleanly.")



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