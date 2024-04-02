import sys
import json
import socket
import time
import threading

boot_ip = '127.0.0.1:5000'

def make_req(req_type, data, req_code):
    req = {'type': req_type, 'data': data, 'seqn': req_code}
    return json.dumps(req)

def send_req(ip_port, req):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip_port.split(":")[0], int(ip_port.split(":")[1])))
        s.sendall(req.encode())

def handle_response(resp, **kwargs):
    resp_data = json.loads(resp)
    resp_type = resp_data['type']
    if resp_type == 'join_response':
        print("Joined Chord network successfully!")
    elif resp_type == 'insert_response':
        print("Insert operation response:", resp_data['data'])
    elif resp_type == 'query_response':
        print("Query operation response:", resp_data['data'])
    elif resp_type == 'delete_response':
        print("Delete operation response:", resp_data['data'])
    elif resp_type == 'set_neighboors_response':
        print("Set neighbors operation response:", resp_data['data'])
    elif resp_type == 'set_replicas_response':
        print("Set replicas operation response:", resp_data['data'])
    # Add more response handling logic as needed

def delayed_join(ip_port):
    time.sleep(20)
    req = make_req('join', {}, "0")
    send_req(ip_port, req)

def insert(ip_port, key, value):
    req = make_req('insert', {'key': key, 'value': value}, "2")
    send_req(ip_port, req)

def query(ip_port, key):
    req = make_req('query', {'key': key}, "3")
    send_req(ip_port, req)

def delete(ip_port, key):
    req = make_req('delete', {'key': key}, "4")
    send_req(ip_port, req)

def set_neighboors(ip_port, prev_ip_port, succ_ip_port):
    req = make_req('set_neighboors', {'prev_ip_port': prev_ip_port, 'succ_ip_port': succ_ip_port}, "5")
    send_req(ip_port, req)

def set_replicas(ip_port, replicas):
    req = make_req('set_replicas', {'replicas': replicas}, "6")
    send_req(ip_port, req)

if __name__ == '__main__':
    ip_port = sys.argv[1]
    boot_ip_port = sys.argv[2]
    
    thread = threading.Thread(target=delayed_join, args=(ip_port,))
    thread.start()
    
    # TCP client code to connect to the bootstrap node
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((boot_ip.split(":")[0], int(boot_ip.split(":")[1])))
        
        # Send join request to bootstrap node
        join_req = make_req('join', {'ip_port': ip_port}, "1")
        send_req(boot_ip_port, join_req)
        
        # Receive and handle response
        resp = s.recv(1024).decode()
        handle_response(resp)
        
        # Perform Chord operations
        # Example insert operation
        insert(ip_port, 'key1', 'value1')
        
        # Example query operation
        query(ip_port, 'key1')
        
        # Example delete operation
        delete(ip_port, 'key1')
        
        # Example set_neighboors operation
        set_neighboors(ip_port, 'prev_ip_port', 'succ_ip_port')
        
        # Example set_replicas operation
        set_replicas(ip_port, 3)
        
        # Perform other operations as needed
