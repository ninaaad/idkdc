import requests

BASE = "http://localhost:5000"

# Create a new key
print("\n--- CREATE KEY ---")
res = requests.post(BASE + "/create")
print(res.json())

# Get any available key
print("\n--- GET KEY ---")
res = requests.post(BASE + "/get")
data = res.json()
print(data)

if "key" in data:
    key = data["key"]

    # Keep alive
    print("\n--- KEEPALIVE ---")
    res = requests.post(BASE + f"/keepalive/{key}")
    print(res.json())

    # Unblock key
    print("\n--- UNBLOCK ---")
    res = requests.post(BASE + f"/unblock/{key}")
    print(res.json())


'''
sudo apt update
sudo apt install python3-venv -y
python3 -m venv venv
source venv/bin/activate

sudo apt install python3-pip -y
pip3 install flask requests

sudo apt update
sudo apt install curl -y
---------------------------------

server terminal : 
python -m pip install flask
python server.py


client terminal : 
python -m pip install requests
python client.py
'''