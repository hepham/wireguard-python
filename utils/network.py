import socket
import subprocess
import requests
from config import Config

def get_public_ip() -> str:
    """Lấy địa chỉ IP public của server"""
    try:
        # Thử dùng API trước
        response = requests.get(Config.PUBLIC_IP_PROVIDER, timeout=3)
        if response.status_code == 200:
            return response.text.strip()
    except:
        pass
    
    # Fallback dùng lệnh curl
    try:
        return subprocess.run(
            ['curl', '-s', 'ifconfig.me'],
            capture_output=True,
            text=True
        ).stdout.strip()
    except:
        return '<SERVER_PUBLIC_IP>'

def validate_ip(ip: str) -> bool:
    """Validate địa chỉ IPv4"""
    try:
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        for part in parts:
            if not 0 <= int(part) <= 255:
                return False
        return True
    except:
        return False

def check_port_open(port: int) -> bool:
    """Kiểm tra port có đang được mở không"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            return s.connect_ex(('localhost', port)) == 0
    except:
        return False