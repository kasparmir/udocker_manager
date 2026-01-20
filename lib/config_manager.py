"""Správa konfigurace v YAML formátu"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional

class ConfigManager:
    def __init__(self, config_dir: Path = None):
        if config_dir is None:
            config_dir = Path.home() / '.udocker_manager'
        
        self.config_dir = Path(config_dir)
        self.config_file = self.config_dir / 'config.yaml'
        self.config_dir.mkdir(exist_ok=True)
        
        if not self.config_file.exists():
            self._create_default_config()
    
    def _create_default_config(self):
        """Vytvoří výchozí konfigurační soubor."""
        self.save_config({'version': '1.0', 'containers': {}})
    
    def load_config(self) -> Dict[str, Any]:
        """Načte celou konfiguraci ze souboru."""
        try:
            if not self.config_file.exists():
                return {'version': '1.0', 'containers': {}}
            
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                
            # Ošetření pro prázdný soubor nebo poškozenou strukturu
            if not config or not isinstance(config, dict):
                return {'version': '1.0', 'containers': {}}
            
            if 'containers' not in config or config['containers'] is None:
                config['containers'] = {}
                
            return config
        except Exception as e:
            print(f"Chyba při načítání konfigurace: {e}")
            return {'version': '1.0', 'containers': {}}
    
    def save_config(self, config: Dict[str, Any]):
        """Uloží celou konfiguraci do souboru."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False, 
                         allow_unicode=True, sort_keys=False, indent=2)
        except Exception as e:
            print(f"Chyba při ukládání konfigurace: {e}")

    # --- Metody volané z container_manager.py ---

    def get_all_containers(self) -> Dict[str, Dict[str, Any]]:
        """Vrátí slovník všech kontejnerů pro get_all_containers_info."""
        config = self.load_config()
        containers = config.get('containers', {})
        # Zajištění, že vracíme vždy dict, i kdyby v yaml bylo None
        return containers if containers is not None else {}

    def get_container_config(self, container_id: str) -> Dict[str, Any]:
        """Vrátí konfiguraci konkrétního kontejneru pro start_container."""
        containers = self.get_all_containers()
        return containers.get(container_id, {})

    def save_container_config(self, container_id: str, container_config: Dict[str, Any]):
        """Uloží/Aktualizuje konfiguraci kontejneru (voláno při create a save_running)."""
        config = self.load_config()
        if 'containers' not in config:
            config['containers'] = {}
        
        config['containers'][container_id] = container_config
        self.save_config(config)

    def delete_container_config(self, container_id: str):
        """Smaže konfiguraci kontejneru (voláno při delete_container)."""
        config = self.load_config()
        containers = config.get('containers', {})
        
        if container_id in containers:
            del config['containers'][container_id]
            self.save_config(config)