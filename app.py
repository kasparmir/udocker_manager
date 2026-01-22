"""UDocker Web Manager - Hlavní soubor"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from flask import Flask
from lib.config_manager import ConfigManager
from lib.udocker_wrapper import UDockerWrapper
from lib.container_manager import ContainerManager

app = Flask(__name__)

# Inicializace managerů
config_manager = ConfigManager()
udocker = UDockerWrapper()
container_manager = ContainerManager(config_manager, udocker)

# Import routes
from routes import *

if __name__ == '__main__':
    print("=" * 70)
    print("🐋 UDocker Manager")
    print("=" * 70)
    
    if not udocker.check_installation():
        print("\n❌ udocker není nainstalován!")
        sys.exit(1)
    
    print(f"\n✓ Konfigurace: {config_manager.config_file}")
    print("\n🔄 Synchronizuji kontejnery...")
    container_manager.sync_running_containers()
    
    print("\n🚀 Autostart kontejnery...")
    results = container_manager.autostart_all()
    if results:
        for name, (success, msg) in results.items():
            print(f"  {'✓' if success else '✗'} {name}")
    else:
        print("  (žádné)")
    
    print("\n" + "=" * 70)
    print("🌐 Server: http://localhost:5000")
    print("=" * 70 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=False)