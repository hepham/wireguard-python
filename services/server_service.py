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
Address = {self.subnet}
ListenPort = {self.port}
PrivateKey = {private_key}
"""
        with open(self.model.config_path, 'w') as f:
            f.write(config)
        os.chmod(self.model.config_path, 0o600)