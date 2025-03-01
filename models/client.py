import json
from ipaddress import IPv4Network
from config import Config

class ClientModel:
    def __init__(self):
        self.data_file = Config.CLIENT_DATA_FILE

    def load_clients(self) -> list:
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_clients(self, clients: list):
        with open(self.data_file, 'w') as f:
            json.dump(clients, f, indent=2)

    def get_next_ip(self, used_ips: list) -> str:
        network = IPv4Network(Config.WG_SUBNET, strict=False)
        for host in network.hosts():
            ip = str(host)
            if ip == str(network.network_address):
                continue
            if ip not in used_ips:
                return f"{ip}/{network.prefixlen}"
        raise ValueError("No available IP addresses")