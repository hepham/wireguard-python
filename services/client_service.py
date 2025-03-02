import subprocess
from services.wg_service import WGService
from models.client import ClientModel
from models.server import ServerModel
from utils.network import get_public_ip
from config import Config
from utils.exceptions import InvalidRequestError, InternalServerError

class ClientService:
    def __init__(self):
        self.client_model = ClientModel()
        self.server_model = ServerModel()
        self.wg_service = WGService()

    def create_client(self, name: str) -> dict:
        try:
            clients = self.client_model.load_clients()
            
            if any(c['name'] == name for c in clients):
                raise InvalidRequestError(f"Client {name} already exists")

            # Generate keys
            private_key = subprocess.check_output(['wg', 'genkey'], text=True).strip()
            print("private_key:",private_key)
            public_key = subprocess.check_output(
                ['wg', 'pubkey'], 
                input=private_key, 
                text=True
            ).strip()
            print("public_key:",public_key)
            preshared_key = subprocess.check_output(['wg', 'genpsk'], text=True).strip()
            print("preshared_key:",preshared_key)
            # Assign IP
            used_ips = [c['ip'].split('/')[0] for c in clients]
            ip = self.client_model.get_next_ip(used_ips)
            print("ip:",ip)
            # Add to server config
            self._add_peer_to_config(public_key, preshared_key, ip)

            # Save client
            client = {
                'name': name,
                'public_key': public_key,
                'private_key': private_key,
                'preshared_key': preshared_key,
                'ip': ip
            }
            clients.append(client)
            self.client_model.save_clients(clients)
            
            self.wg_service.apply_config()
            return client
        except subprocess.CalledProcessError as e:
            raise InternalServerError(f"Failed to generate WireGuard keys: {str(e)}")
        except Exception as e:
            raise InternalServerError(f"Failed to create client: {str(e)}")

    def _add_peer_to_config(self, public_key: str, psk: str, ip: str):
        peer_config = f"\n[Peer]\nPublicKey = {public_key}\n"
        peer_config += f"PresharedKey = {psk}\n"
        peer_config += f"AllowedIPs = {ip.split('/')[0]}/32\n"
        
        with open(self.server_model.config_path, 'a') as f:
            f.write(peer_config)

    def generate_client_config(self, client: dict) -> str:
        return f"""[Interface]
PrivateKey = {client['private_key']}
Address = {client['ip']}
DNS = {Config.WG_DNS}

[Peer]
PublicKey = {self.server_model.get_server_public_key()}
PresharedKey = {client['preshared_key']}
AllowedIPs = 0.0.0.0/0
Endpoint = {get_public_ip()}:{Config.WG_PORT}
PersistentKeepalive = 25
"""