# CHORD-KV

This application is a file sharing application with a distributed nodes DHT.
Every node can interact with Chord either as a server, or as a client. The
nodes keep information in key-value pairs, where the key is the title of each
song saved in the Chord and the value is the node that has this song.
Replication is supported with two types of consistency, linearizability (chain
replication) and eventual.







### Fire up Bootstrap Node

```python3 Bootstrap_node.py bootstrap_ip:port bootstrap_ip:port number_of_replicas type_of_consistency```

For example:

```python 3 Bootstrap_node.py 127.0.0.1:5000 127.0.0.1:5000 3 eventual```

Will fire up bootstrap node in host server1 and port 5000. Chord will keep 3 replicas and the consistency type will be eventual.

### Fire up Nodes

```python3 Normal_node.py node_ip:port bootstrap_ip:port```

For example:

```python3 Normal_node.py 127.0.0.1:5001 127.0.0.1:5000```

Will fire up a normal node in host server2 port 5000, that communicates with boostrap in host server1 port 5000.

### Cli usage

```python3 cli.py --help```






Test Insert, Query, and Delete Operations:

python3 cli.py insert --key "song1" --value "artist1" 127.0.0.1:5001
python3 cli.py insert --key "song2" --value "artist2" 127.0.0.1:5002
python3 cli.py query --key "song1" 127.0.0.1:5001
python3 cli.py query --key "song2" 127.0.0.1:5002
python3 cli.py delete --key "song1" 127.0.0.1:5001

Depart a Node:
python3 cli.py depart 127.0.0.1:5001

View Chord Overlay:
python3 cli.py overlay 127.0.0.1:5000


Send Requests with Input from a File:
python3 cli.py file file1.txt --request_type insert
python3 cli.py file file1.txt --request_type query
python3 cli.py file file1.txt --request_type mix



