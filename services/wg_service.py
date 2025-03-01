import subprocess
from config import Config

class WGService:
    def __init__(self):
        self.interface = Config.WG_INTERFACE
        self.config_path = f"{Config.WG_CONFIG_DIR}/{self.interface}.conf"

    def apply_config(self):
        try:
            subprocess.run(
                ['wg', 'syncconf', self.interface, self.config_path],
                check=True
            )
        except subprocess.CalledProcessError:
            self.restart()

    def restart(self):
        subprocess.run(['wg-quick', 'down', self.interface], check=True)
        subprocess.run(['wg-quick', 'up', self.interface], check=True)