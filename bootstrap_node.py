import sys
import json
import socket
from threading import Thread
import hashlib

ip_port = sys.argv[1]
replicas = sys.argv[3]  # Number of replicas
rep_type = sys.argv[4]  # Replica type ("linearizability" || "eventual")
boot_ip_port = ip_port

# THIS IS HOST AND PORT FOR A NORMAL NODE
host_port = ip_port.split(":")
host = host_port[0]
port = int(host_port[1])

# Construct node
node = None

responses_dict = {}
# History of requests and responses for the corresponding sequence numbers
requests_list = []
responses_list = []
seqn = 0
# Nodes in Chord start from 1 (myself)
# When a node joins or leaves, this number changes accordingly
number_of_nodes = 1

def make_req(req_type, data, req_code):
    req = {'source': node.ip_port, 'type': req_type, 'data': data, 'seqn': str(req_code)}
    return req

def make_resp(receiver, resp_type, data, req_code):
    resp = {'receiver': receiver, 'type': resp_type, 'data': data, 'seqn': str(req_code)}
    return resp

def hash(text):
    hash_object = hashlib.sha1(text.encode())
    hash_code = hash_object.hexdigest()
    return hash_code

def handle_response(resp, **kwargs):
    receiver = resp['receiver']
    resp_type = resp['type']
    data = resp['data']
    seqn = resp['seqn']
    # Check if I am the correct receiver
    if node.ip_port == receiver:
        if resp_type == 'insert':
            msg = data['resp_text']
            c = kwargs.get('unhashed_key', None)
            msg = 'Key:' + c + ' ' + msg
        elif resp_type == 'query':
            msg = data['resp_text']
            c = kwargs.get('unhashed_key', None)
            msg = 'Key:' + c + ' ' + msg
        elif resp_type == 'delete':
            msg = data['resp_text']
            c = kwargs.get('unhashed_key', None)
            msg = 'Key:' + c + ' ' + msg
        elif resp_type == 'overlay':
            topology = data['topology']
            msg = topology
        elif resp_type == 'query_all':
            pairs = data['key-value pairs']
            msg = pairs

    return msg

def send_response(conn, resp):
    conn.sendall(json.dumps(resp).encode())

def send_request(ip_port, req):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip_port[0], int(ip_port[1])))
        s.sendall(json.dumps(req).encode())

def handle_client(conn, addr):
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            req_dict = json.loads(data.decode())
            handle_request(req_dict, conn)

def handle_request(req_dict, conn):
    source = req_dict['source']
    req_type = req_dict['type']
    data = req_dict['data']
    req_code = req_dict['seqn']

    if req_type == 'insert':
        handle_insert(source, req_code, data, conn)
    elif req_type == 'query':
        handle_query(source, req_code, data, conn)
    # Add more handlers for other request types

def handle_insert(source, req_code, data, conn):
    global seqn
    seqn = seqn + 1
    req_code = seqn

    # Your logic for handling insert request goes here

def handle_query(source, req_code, data, conn):
    global seqn
    seqn = seqn + 1
    req_code = seqn

    # Your logic for handling query request goes here

def start_tcp_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"TCP server listening on {host}:{port}")
        while True:
            conn, addr = s.accept()
            print(f"Connection from {addr}")
            client_thread = Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

def join():
    global seqn
    seqn = seqn + 1
    print("The Chord now starts...\n")

if __name__ == '__main__':
    join()
    start_tcp_server(host, port)
