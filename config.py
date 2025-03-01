import os

class Config:
    # Flask
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # WireGuard
    WG_INTERFACE = 'wg0'
    WG_PORT = 51820
    WG_SUBNET = '10.0.0.1/24'
    WG_CONFIG_DIR = '/etc/wireguard'
    WG_DNS = '1.1.1.1'
    
    # Clients
    CLIENT_DATA_FILE = 'clients.json'
    
    # API Security
    API_KEYS = {
        'admin': os.getenv('ADMIN_API_KEY', 'super-secret-admin-key'),
        'readonly': os.getenv('READONLY_API_KEY', 'readonly-key-123')
    }
    
    # Network
    PUBLIC_IP_PROVIDER = 'https://api.ipify.org'

class ProductionConfig(Config):
    DEBUG = False
    WG_CONFIG_DIR = '/etc/wireguard/prod'

class DevelopmentConfig(Config):
    DEBUG = True
    CLIENT_DATA_FILE = 'dev_clients.json'