"""Manažer pro správu kontejnerů"""

from typing import Dict, Tuple, Any
from lib.config_manager import ConfigManager
from lib.udocker_wrapper import UDockerWrapper

class ContainerManager:
    def __init__(self, config_manager: ConfigManager, udocker: UDockerWrapper):
        self.config = config_manager
        self.udocker = udocker
    
    def get_all_containers_info(self) -> Dict[str, Dict[str, Any]]:
        config_containers = self.config.get_all_containers()
        if config_containers is None:
            config_containers = {}
        
        running_containers = {c['id']: c for c in self.udocker.get_running_containers()}
        
        all_containers = {}
        
        for container_id, config in config_containers.items():
            all_containers[container_id] = {
                **config,
                'id': container_id,
                'running': container_id in running_containers,
                'managed': True
            }
        
        for container_id, container_info in running_containers.items():
            if container_id not in all_containers:
                all_containers[container_id] = {
                    'id': container_id,
                    'name': container_id,
                    'running': True,
                    'managed': False,
                    'autostart': False,
                    'image': 'unknown',
                    'ports': [],
                    'volumes': [],
                    'env': [],
                    'command': ''
                }
        
        return all_containers
    
    def create_and_start_container(self, container_config: Dict[str, Any]) -> Tuple[bool, str, str]:
        """Vytvoří kontejner, stáhne image pokud neexistuje, a spustí ho"""
        name = container_config['name']
        image = container_config['image']
        
        # Kontrola, zda image existuje
        if not self.udocker.image_exists(image):
            print(f"Image {image} neexistuje, stahuji...")
            success, message = self.udocker.pull_image(image)
            if not success:
                return False, f"Nelze stáhnout image: {message}", ""
        
        # Vytvoření kontejneru
        success, message = self.udocker.create_container(name, image)
        
        if not success:
            return False, message, ""
        
        # Uložení konfigurace
        self.config.save_container_config(name, container_config)
        
        # Automatické spuštění
        success, start_message = self.start_container(name)
        
        if success:
            return True, f"Kontejner {name} vytvořen a spuštěn", name
        else:
            return True, f"Kontejner {name} vytvořen, ale nepodařilo se spustit: {start_message}", name
    
    def start_container(self, container_id: str) -> Tuple[bool, str]:
        container_config = self.config.get_container_config(container_id)
        
        return self.udocker.run_container(
            container_id,
            volumes=container_config.get('volumes', []),
            ports=container_config.get('ports', []),
            env=container_config.get('env', []),
            command=container_config.get('command')
        )
    
    def stop_container(self, container_id: str) -> Tuple[bool, str]:
        return self.udocker.stop_container(container_id)
    
    def delete_container(self, container_id: str) -> Tuple[bool, str]:
        success, message = self.udocker.delete_container(container_id)
        
        if success:
            self.config.delete_container_config(container_id)
            return True, f"Kontejner {container_id} smazán"
        
        return False, message
    
    def save_running_container(self, container_id: str) -> Tuple[bool, str]:
        container_config = {
            'name': container_id,
            'image': 'unknown',
            'autostart': False,
            'ports': [],
            'volumes': [],
            'env': [],
            'command': ''
        }
        
        self.config.save_container_config(container_id, container_config)
        return True, f"Kontejner {container_id} uložen"
    
    def sync_running_containers(self):
        running = self.udocker.get_running_containers()
        config_containers = self.config.get_all_containers()
        
        for container in running:
            if container['id'] not in config_containers:
                print(f"  • Nalezen: {container['id']}")
    
    def autostart_all(self) -> Dict[str, Tuple[bool, str]]:
        results = {}
        containers = self.config.get_all_containers()
        if containers is None:
            return results
        
        for container_id, config in containers.items():
            if config.get('autostart'):
                success, message = self.start_container(container_id)
                results[config['name']] = (success, message)
        
        return results