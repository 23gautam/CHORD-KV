class Node:
    def __init__(self, ip_port, boot_ip, k=1, reptype="None", is_bootstrap=False):
        self.ip_port = ip_port
        self.boot_ip_port = boot_ip
        self.prev_ip_port = ip_port
        self.succ_ip_port = ip_port
        self.id = self.make_id()
        self.keys_vals = []
        self.replicas = k
        self.rep_type = reptype
        self.is_in_chord = False
        if is_bootstrap:
            for _ in range(int(k)):
                self.keys_vals.append({})

    def get_rep_type(self):
        return self.rep_type

    def get_replicas(self):
        return int(self.replicas)

    def get_is_in_chord(self):
        return self.is_in_chord

    def hash(self, text):
        hash_object = hashlib.sha1(text.encode())
        return hash_object.hexdigest()

    def make_id(self):
        return self.hash(self.ip_port)

    def has_key(self, key):
        for data_dict in self.keys_vals:
            if data_dict.get(key, "None") == "None":
                continue
            else:
                return True
        return False

    def insert(self, key, val, repn):
        msg = ""
        if self.keys_vals[int(repn)].get(key, "None") == "None":
            msg += "inserted"
        else:
            msg += "updated"
        self.keys_vals[int(repn)].update({key: val})
        return msg

    def query(self, key):
        x = "None"
        for data_dict in self.keys_vals:
            x = data_dict.get(key, "None")
            if x == "None":
                continue
            else:
                return x
        return x

    def delete(self, key):
        for data_dict in self.keys_vals:
            x = data_dict.pop(key, "None")
            if x == "None":
                continue
            else:
                return "deleted"
        return "doesn't exist hence can't be deleted"

    def is_next(self, source_ip_port):
        return self.prev_ip_port == source_ip_port

    def is_prev(self, source_ip_port):
        return self.succ_ip_port == source_ip_port

    def set_neighbors(self, prev_ip_port, succ_ip_port):
        if prev_ip_port != "None":
            self.prev_ip_port = prev_ip_port
        if succ_ip_port != "None":
            self.succ_ip_port = succ_ip_port

    def join_set_vars(self, repn, rep_type):
        self.replicas = repn
        self.rep_type = rep_type
        self.is_in_chord = True
        for _ in range(int(repn)):
            self.keys_vals.append({})

    def get_same_new_keys(self, key):
        same_keys = {}
        new_keys = {}
        id1 = key
        id2 = self.id
        if id1 > id2:
            for k, v in self.keys_vals[0].items():
                if k > id1 or k <= id2:
                    same_keys[k] = v
                else:
                    new_keys[k] = v
        else:
            for k, v in self.keys_vals[0].items():
                if k > id1 and k <= id2:
                    same_keys[k] = v
                else:
                    new_keys[k] = v
        return same_keys, new_keys

    def push_down(self, index):
        index = int(index)
        k = self.get_replicas()
        if 0 < index < k:
            temp = self.keys_vals[index - 1]
            for i in range(index, k):
                temp2 = self.keys_vals[i]
                self.keys_vals[i] = temp
                temp = temp2

    def push_up(self, index):
        index = int(index)
        k = self.get_replicas()
        if 0 <= index < k - 1:
            for i in range(index + 1, k):
                self.keys_vals[i - 1] = self.keys_vals[i]

    def is_alone(self):
        return self.prev_ip_port == self.succ_ip_port == self.ip_port

    def is_duo(self):
        return not self.is_alone() and self.succ_ip_port == self.prev_ip_port

    def init_state(self):
        self.prev_ip_port = self.ip_port
        self.succ_ip_port = self.ip_port
        self.keys_vals = []
        self.replicas = 1
        self.rep_type = "None"
        self.is_in_chord = False

    def return_node_stats(self):
        hashtable = ""
        for i in range(len(self.keys_vals)):
            data_dict = self.keys_vals[i]
            l = []
            for k, v in data_dict.items():
                l.append(v)
            hashtable += str(l) + "\n"

        msg = f"\nIP:{self.ip_port}\n  Prev_IP:{ self.prev_ip_port}\n Next_IP:{ self.succ_ip_port}\n Boot_IP:{self.boot_ip_port}\n Hashtable:\n" + hashtable + "\n"
        return msg
