import os
from models.server import ServerModel

class ServerService:
    def __init__(self, port: int = 51820, subnet: str = '10.0.0.1/24'):
        self.model = ServerModel()
        self.port = port
        self.subnet = subnet

    def initialize_server(self):
        os.makedirs(os.path.dirname(self.model.config_path), exist_ok=True)
        
        if not os.path.exists(self.model.config_path):
            private_key, public_key = self.model.generate_keys()
            self._create_initial_config(private_key)
        else:
            private_key = self.model.get_private_key()
        
        return {
            'private_key': private_key,
            'subnet': self.subnet,
            'port': self.port
        }

    def _create_initial_config(self, private_key: str):
        config = f"""[Interface]
# Private key of the server
PrivateKey = {private_key}
# Listening port of the server
ListenPort = {self.model.port}
# Address and subnet of the WireGuard interface
Address = 10.66.66.1/24, fd42:42:42::1/64
# Post up script
PostUp = {self.model.post_up_script}
# Post down script
PostDown = {self.model.post_down_script}
"""
        with open(self.model.config_path, 'w') as f:
            f.write(config)
        os.chmod(self.model.config_path, 0o600)