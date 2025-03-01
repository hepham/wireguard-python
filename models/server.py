import os
import subprocess
from config import Config

class ServerModel:
    def __init__(self):
        self.interface = Config.WG_INTERFACE
        self.config_path = os.path.join(Config.WG_CONFIG_DIR, f'{self.interface}.conf')
        
    def generate_keys(self) -> tuple:
        private_key = subprocess.run(
            ['wg', 'genkey'], 
            capture_output=True, 
            text=True
        ).stdout.strip()
        
        public_key = subprocess.run(
            ['wg', 'pubkey'], 
            input=private_key, 
            capture_output=True, 
            text=True
        ).stdout.strip()
        
        return private_key, public_key

    def get_server_public_key(self) -> str:
        return subprocess.run(
            ['wg', 'pubkey'], 
            input=self.get_private_key(), 
            capture_output=True, 
            text=True
        ).stdout.strip()

    def get_private_key(self) -> str:
        with open(self.config_path, 'r') as f:
            for line in f:
                if 'PrivateKey' in line:
                    return line.split('=')[1].strip()
        raise ValueError("Private key not found")